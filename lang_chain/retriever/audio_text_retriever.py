# -*- coding: utf-8 -*-
# @Time    : 2024/2/24 21:43
# @Author  : nongbin
# @FileName: audio_text_retriever.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
from typing import List, Dict

from config.config import Config
from lang_chain.client import get_ai_client

_GENERATE_AUDIO_PROMPT_ = "请从上述对话中帮我提取出即将要转成语音的文本"
__client = get_ai_client()


def __construct_messages(question: str, history: List[List | None]) -> List[Dict[str, str]]:
    messages = [
        {"role": "system",
         "content": "你现在扮演信息抽取的角色，要求根据用户输入和AI的回答，正确提取出信息，无需包含提示文字"}]

    for user_input, ai_response in history:
        messages.append({"role": "user", "content": user_input})
        messages.append(
            {"role": "assistant", "content": repr(ai_response)})

    messages.append({"role": "user", "content": question})
    messages.append({"role": "user", "content": _GENERATE_AUDIO_PROMPT_})

    return messages


def extract_text(question: str,
                 history: List[List | None] | None = None) -> str:
    response = __client.chat.completions.create(
        model="glm-4",
        messages=__construct_messages(question, history),
        top_p=0.7,
        temperature=0.95,
        max_tokens=1024,
    )

    return response.choices[0].message.content


def extract_language(text: str) -> str:
    response = __client.chat.completions.create(
        model="glm-4",
        messages=[
            {"role": "system",
             "content": "你现在扮演信息抽取的角色，要求根据用户输入和AI的回答，正确提取出信息，不要复述，无需包含提示文字"},
            {"role": "user",
             "content": f"请从如下文本中提取出文本转语音的语种，提取结果只有4种可能（陕西话，东北话，粤语，台湾话），"
                        f"如果如下文本不包含这4语种信息，直接返回一个字：无。"
                        f"（注意：结果中不要包含任何符号和提示信息）：\n{text}"}],
        top_p=0.7,
        temperature=0.95,
        max_tokens=1024,
    )

    lang_text = response.choices[0].message.content
    return lang_text


def get_tts_model_name(lang: str, gender: str) -> str:
    if lang == "无" and (gender == "无" or gender == "男声"):
        return (Config.get_instance().
                get_with_nested_params("lang-chain"
                                       , "audio"
                                       , "voice"
                                       , "NORMAL-MALE"))

    if lang == "无" and gender == "女声":
        return (Config.get_instance().
                get_with_nested_params("lang-chain"
                                       , "audio"
                                       , "voice"
                                       , "NORMAL-FEMALE"))

    if lang == "陕西话" and (gender == "女声" or gender=="无"):
        return (Config.get_instance().
                get_with_nested_params("lang-chain"
                                       , "audio"
                                       , "voice"
                                       , "SHANXI-FEMALE"))

    if lang == "东北话" and (gender == "女声" or gender=="无"):
        return (Config.get_instance().
                get_with_nested_params("lang-chain"
                                       , "audio"
                                       , "voice"
                                       , "DONGBEI-FEMALE"))

    if lang == "粤语" and gender == "女声":
        return (Config.get_instance().
                get_with_nested_params("lang-chain"
                                       , "audio"
                                       , "voice"
                                       , "HK-FEMALE"))

    if lang == "粤语" and (gender == "男声" or gender=="无"):
        return (Config.get_instance().
                get_with_nested_params("lang-chain"
                                       , "audio"
                                       , "voice"
                                       , "HK-MALE"))

    if lang == "台湾话" and gender == "男声":
        return (Config.get_instance().
                get_with_nested_params("lang-chain"
                                       , "audio"
                                       , "voice"
                                       , "TW-MALE"))

    if lang == "台湾话" and (gender == "女声" or gender=="无"):
        return (Config.get_instance().
                get_with_nested_params("lang-chain"
                                       , "audio"
                                       , "voice"
                                       , "TW-FEMALE"))


def extract_gender(text: str) -> str:
    response = __client.chat.completions.create(
        model="glm-4",
        messages=[
            {"role": "system",
             "content": "你现在扮演信息抽取的角色，要求根据用户输入和AI的回答，正确提取出信息，不要复述，无需包含提示文字"},
            {"role": "user",
             "content": f"请从如下文本中提取出文本转语音的声音性别，提取的结果只有两种可能，男声和女声，如果如下文本不包含声音性别，"
                        f"直接返回一个字：无。（注意：结果中不要包含任何符号和提示信息）：\n{text}"}],
        top_p=0.7,
        temperature=0.95,
        max_tokens=1024,
    )

    return response.choices[0].message.content
