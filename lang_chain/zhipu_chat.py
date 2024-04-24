# -*- coding: utf-8 -*-
# @Time    : 2024/1/26 21:52
# @Author  : nongbin
# @FileName: zhipu_chat.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
from typing import List, Dict

from zhipuai.core._sse_client import StreamResponse

from lang_chain.client import get_ai_client

__client = get_ai_client()


def chat_with_ai(prompt):
    response = __client.chat.completions.create(
        model="glm-4",
        messages=[
            {"role": "user", "content": prompt},
        ],
        top_p=0.7,
        temperature=0.95,
        max_tokens=1024,
    )

    return response.choices[0].message.content


def construct_messages(prompt: str, history: List[List | None]) -> List[Dict[str, str]]:
    messages = [
        {"role": "system", "content": "你是一个乐于解答各种问题的助手，你的任务是为用户提供专业、准确、有见地的回答。"}]

    for user_input, ai_response in history:
        messages.append({"role": "user", "content": user_input})
        messages.append(
            {"role": "assistant", "content": ai_response.__repr__()})

    messages.append({"role": "user", "content": prompt})
    return messages


def chat_with_ai_stream(prompt: str,
                        history: List[List[str]] | None = None) -> StreamResponse:
    response = __client.chat.completions.create(
        model="glm-4",
        messages=construct_messages(prompt, history if history else []),
        top_p=0.7,
        temperature=0.95,
        max_tokens=1024,
        stream=True,
    )

    return response


def chat_using_messages(messages: List[Dict]) -> str | None:
    response = __client.chat.completions.create(
        model="glm-4",
        messages=messages,
        top_p=0.7,
        temperature=0.95,
        max_tokens=1024,
    )

    return response.choices[0].message.content
