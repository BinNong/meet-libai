# -*- coding: utf-8 -*-
# @Time    : 2024/4/20 10:34
# @Author  : nongbin
# @FileName: function_tool.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
from typing import List, Tuple, Callable

from zhipuai.core._sse_client import StreamResponse

from dao.graph.graph_dao import GraphDao
from qa.question_type import QuestionType
from model.graph_entity.search_model import _Value
from lang_chain.retriever.image_text_retriever import extract_text as extract_image_text
from lang_chain.zhipu_images import generate as generate_image
from lang_chain.edge_audio import generate as generate_audio
from lang_chain.retriever.audio_text_retriever import extract_text as extract_audio_text, extract_language, \
    get_tts_model_name, extract_gender
from lang_chain.retriever.video_text_retriever import extract_text as extract_video_text
from lang_chain.sora_video import generate as generate_video
from lang_chain import rag_chain
from lang_chain.poetry_search import search_by_chinese, search_by_poetry
from lang_chain.retriever.chinese_text_for_poetry_retriever import extract_text
from lang_chain.zhipu_chat import chat_with_ai_stream, chat_with_ai
from qa.prompt_templates import HELLO_ANSWER_TEMPLATE, LLM_HINT

_dao = GraphDao()


def basic_info_tool(entities: List[_Value] | None) -> Tuple[str, QuestionType] | None:
    """人物基本信息"""
    if not entities:
        return None
    node_match = _dao.query_node("人物", name=entities[0].name)
    if node_match:
        node = node_match.first()
        return (
            f"{entities[0].name}, 生于{node['DynastyBirth']}。{node['DynastyDeath']}时期文人。" + "下面以json格式给出这个人的完整基本信息：" + node.__repr__(),
            QuestionType.BASIC_INFO)


def relation_tool(entities: List[_Value] | None) -> Tuple[str, QuestionType] | None:
    """人物关系"""
    if not entities or len(entities) < 2:
        return None
    relationship_match = _dao.query_relationship_by_2person_name(entities[0].name, entities[1].name)
    if relationship_match:

        rel = relationship_match[0]['type(r)']
        if entities[0].name not in rel:
            start_name = entities[0].name
        else:
            start_name = entities[1].name
        return f"关系如下：{start_name}{rel}，详见:{relationship_match[0]['r']['Notes']}", QuestionType.RELATION


def hello_tool() -> Tuple[Tuple[str, StreamResponse], QuestionType]:
    """打招呼"""
    response = chat_with_ai_stream(HELLO_ANSWER_TEMPLATE)
    return ("谢谢你的问候😊\n", response), QuestionType.HELLO


def images_generation_tool(
        question: str,
        history: List[List[str] | None] = None
) -> Tuple[Tuple[str, str], QuestionType]:
    text = extract_image_text(question, history)
    image_url = generate_image(text)
    return (image_url, "图片"), QuestionType.IMAGES


def audio_generation_tool(
        question: str,
        history: List[List[str] | None] = None
) -> Tuple[Tuple[str, str], QuestionType]:
    text = extract_audio_text(question, history)
    lang = extract_language(question)
    gender = extract_gender(question)
    model_name = get_tts_model_name(lang=lang, gender=gender)
    audio_file = generate_audio(text, model_name)
    return (audio_file, "语音"), QuestionType.AUDIO


def video_generation_tool(
        question: str,
        history: List[List[str] | None] = None
) -> Tuple[
    Tuple[str, str], QuestionType]:
    text = extract_video_text(question, history)
    video_url = generate_video(text)
    return (video_url, "视频"), QuestionType.VIDEOS


def document_search_tool(
        question: str,
        history: List[List[str] | None] = None
) -> Tuple[Tuple[str, StreamResponse], QuestionType]:
    reference, response = rag_chain.invoke(question, history)
    return (reference, response), QuestionType.DOCUMENT


def search_poetry_by_chinese_tool(
        question_type: QuestionType,
        question: str,
        history: List[List[str] | None] = None
) -> Tuple[str, QuestionType]:
    text = extract_text(question, question_type, history)
    table = search_by_chinese(text)
    return table, QuestionType.CHINESE2POETRY


def search_poetry_by_poetry_tool(
        question_type: QuestionType,
        question: str,
        history: List[List[str] | None] = None
) -> Tuple[str, QuestionType]:
    text = extract_text(question, question_type, history)
    table = search_by_poetry(text)
    return table, QuestionType.CHINESE2POETRY


def process_unknown_question_tool(
        question: str,
        history: List[List[str] | None] = None,
) -> Tuple[Tuple[str, StreamResponse], QuestionType]:
    head_: str = chat_with_ai(LLM_HINT)
    response = chat_with_ai_stream(question, history[-5:])
    return (head_, response), QuestionType.UNKNOWN


TOOLS_MAPPING = {
    QuestionType.BASIC_INFO: basic_info_tool,
    QuestionType.RELATION: relation_tool,
    QuestionType.HELLO: hello_tool,
    QuestionType.IMAGES: images_generation_tool,
    QuestionType.AUDIO: audio_generation_tool,
    QuestionType.VIDEOS: video_generation_tool,
    QuestionType.DOCUMENT: document_search_tool,
    QuestionType.CHINESE2POETRY: search_poetry_by_chinese_tool,
    QuestionType.POETRY2POETRY: search_poetry_by_poetry_tool,
    QuestionType.UNKNOWN: process_unknown_question_tool
}


def map_question_to_function(
        question_type: QuestionType,
) -> Callable:
    if question_type in TOOLS_MAPPING:
        return TOOLS_MAPPING[question_type]
    else:
        raise ValueError(f"No tool found for question type: {question_type}")


FUNCTION_ARGS_MAPPING = {
    QuestionType.BASIC_INFO: lambda args: args[-1:],
    QuestionType.RELATION: lambda args: args[-1:],
    QuestionType.HELLO: lambda args: [],
    QuestionType.IMAGES: lambda args: args[1:3],
    QuestionType.AUDIO: lambda args: args[1:3],
    QuestionType.VIDEOS: lambda args: args[1:3],
    QuestionType.DOCUMENT: lambda args: args[1:3],
    QuestionType.CHINESE2POETRY: lambda args: args[:3],
    QuestionType.POETRY2POETRY: lambda args: args[:3],
    QuestionType.UNKNOWN: lambda args: args[1:3]
}


def map_question_to_function_args(
        question_type: QuestionType,
) -> Callable[[List], List]:
    if question_type in FUNCTION_ARGS_MAPPING:
        return FUNCTION_ARGS_MAPPING[question_type]
    else:
        raise ValueError(f"No tool found for question type: {question_type}")
