# -*- coding: utf-8 -*-
# @Time    : 2024/8/21 15:40
# @Author  : nongbin
# @FileName: tools.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
import json
from typing import List, Dict, Tuple, Callable, Any

from dao.graph.graph_dao import GraphDao
from lang_chain import rag_chain
from lang_chain.client.client_factory import ClientFactory
from lang_chain.edge_audio import generate as generate_audio
from lang_chain.poetry_search import search_by_chinese, search_by_poetry
from lang_chain.retriever.audio_text_retriever import get_tts_model_name
from lang_chain.retriever.chinese_text_for_poetry_retriever import extract_text
from lang_chain.retriever.ppt_content_retriever import generate_ppt_content
from lang_chain.sora_video import generate as _generate_video
from lang_chain.digital_men import generate as _generate_digital_men
from logger import Logger
from qa.custom_tool_calling.prompt_templates import HELLO_ANSWER_TEMPLATE
from qa.custom_tool_calling.question_parser import check_entity
from qa.supported_tool_calling.tools_description import GET_PERSONAL_PROFILE, GET_RELATION_INFO, GET_HELLO_INFO, \
    GENERATE_IMAGES, GENERATE_SPEECH, GENERATE_VIDEO, SEARCH_DOCUMENTS, GENERATE_PPT, SEARCH_POETRY_BY_CHINESE, \
    SEARCH_POETRY_BY_POETRY, GENERATE_DIGITAL_MEN
from qa.supported_tool_calling.utils import ChatResponse
from lang_chain.ppt_generation import generate as _generate_ppt

_dao = GraphDao()
_logger: Logger = Logger("tool_calling")


def get_personal_profile(name: str) -> ChatResponse:
    result = check_entity(name)
    if not result:
        return ChatResponse()
    node_match = _dao.query_node("人物", name=name)
    if node_match:
        node = node_match.first()
        info = f"{name}, 生于{node['DynastyBirth']}。{node['DynastyDeath']}时期文人。" + "下面以json格式给出这个人的完整基本信息：" + node.__repr__()

        return ChatResponse(None, info)


def get_relation_info(first_entity_name, second_entity_name) -> ChatResponse:
    relationship_match = _dao.query_relationship_by_2person_name(first_entity_name, second_entity_name)
    rel = relationship_match[0]['type(r)']
    if first_entity_name not in rel:
        start_name = first_entity_name
    else:
        start_name = second_entity_name
    info = f"关系如下：{start_name}{rel}，详见:{relationship_match[0]['r']['Notes']}"

    return ChatResponse(None, info)


def get_hello_info(question: str) -> ChatResponse:
    response = ClientFactory().get_client().chat_with_ai_stream(HELLO_ANSWER_TEMPLATE)
    return ChatResponse(response)


def generate_images(text: str) -> Tuple[str, str]:
    image_url = ClientFactory().get_client().generate_image(text)
    return image_url, "图片链接"


def generate_speech(text: str, language: str = '无', gender: str = '无') -> Tuple[str, str]:
    model_name = get_tts_model_name(lang=language, gender=gender)
    audio_file = generate_audio(text, model_name)

    return audio_file, "语音链接"


def generate_video(text: str) -> Tuple[str, str]:
    video_url = _generate_video(text)
    return video_url, "视频链接"


def generate_digital_men(transcript: str) -> Tuple[str, str] | ChatResponse:
    digital_men_url = _generate_digital_men(transcript)
    if digital_men_url is None:
        return ChatResponse(None, "数字人生成失败")
    return digital_men_url, "数字人链接"


def generate_ppt(text: str, history: List[List[str]] | None = None) -> Tuple[str, str]:
    raw_text: str = generate_ppt_content(text, history)
    ppt_content = json.loads(raw_text)
    ppt_file: str = _generate_ppt(ppt_content)
    return ppt_file, "ppt链接"


def search_documents(question: str, history: List[List[str]] | None = None) -> ChatResponse:
    reference, response = rag_chain.invoke(question, history)
    return ChatResponse(response, reference)


def search_poetry_by_chinese(question: str, history: List[List[str]] | None = None) -> ChatResponse:
    text = extract_text(question,
                        "chinese2poetry",
                        history)
    table = search_by_chinese(text)
    return ChatResponse(None, table)


def search_poetry_by_poetry(
        question: str,
        history: List[List[str] | None] = None
) -> ChatResponse:
    text = extract_text(question,
                        "poetry2poetry",
                        history)
    table = search_by_poetry(text)
    return ChatResponse(None, table)


tools = [
    GET_PERSONAL_PROFILE,
    GET_RELATION_INFO,
    GET_HELLO_INFO,
    GENERATE_IMAGES,
    GENERATE_SPEECH,
    GENERATE_VIDEO,
    GENERATE_DIGITAL_MEN,
    SEARCH_DOCUMENTS,
    GENERATE_PPT,
    SEARCH_POETRY_BY_CHINESE,
    SEARCH_POETRY_BY_POETRY,
]

tools_mapping: Dict[str, Callable] = {
    "get_personal_profile": get_personal_profile,
    "get_relation_info": get_relation_info,
    "get_hello_info": get_hello_info,
    "generate_images": generate_images,
    "generate_speech": generate_speech,
    "generate_video": generate_video,
    "generate_digital_men": generate_digital_men,
    "search_documents": search_documents,
    "generate_ppt": generate_ppt,
    "search_poetry_by_chinese": search_poetry_by_chinese,
    "search_poetry_by_poetry": search_poetry_by_poetry,
}


def get_tools(question: str, history: List[List] | None) -> tuple[Callable[..., Any], dict] | None:
    result = ClientFactory().get_client().chat_on_tools(question, tools, history)

    if not result:
        return None

    function_name, args = result

    if function_name not in tools_mapping:
        _logger.warning(f"Function {function_name} not found")
        return None
    return tools_mapping[function_name], args
