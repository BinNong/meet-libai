# -*- coding: utf-8 -*-
# @Time    : 2024/4/13 11:50
# @Author  : nongbin
# @FileName: chinese_text_for_poetry_retriever.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn

from typing import List, Dict


from lang_chain.client.client_factory import ClientFactory
from qa.question_type import QuestionType

__CHINESE2POETRY_PROMPT_ = "请从上述对话中帮我提取出以白话文搜古文对应的文本内容，不要解释，不要多余的信息，只需要提取出原文中对应的内容。"
__POETRY2POETRY_PROMPT_ = "请从上述对话中帮我提取出以古文搜古文对应的文本内容，不要解释，不要多余的信息，只需要提取出原文中对应的内容。"


def __construct_messages(question: str,
                         question_type: QuestionType,
                         history: List[List | None]) -> List[Dict[str, str]]:
    messages = [
        {"role": "system",
         "content": "你现在扮演信息抽取的角色，要求根据用户输入和AI的回答，正确提取出信息，无需包含提示文字"}]

    for user_input, ai_response in history:
        messages.append({"role": "user", "content": user_input})
        messages.append(
            {"role": "assistant", "content": repr(ai_response)})

    messages.append({"role": "user", "content": question})
    messages.append({"role": "user",
                     "content": __CHINESE2POETRY_PROMPT_ if question_type == QuestionType.CHINESE2POETRY
                     else __POETRY2POETRY_PROMPT_})

    return messages


def extract_text(question: str,
                 question_type: QuestionType,
                 history: List[List | None] | None = None,
                 ) -> str:
    messages = __construct_messages(question, question_type, history or [])
    result = ClientFactory().get_client().chat_using_messages(messages)

    return result
