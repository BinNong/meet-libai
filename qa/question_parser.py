# -*- coding: utf-8 -*-
# @Time    : 2024/2/18 12:17
# @Author  : nongbin
# @FileName: question_parser.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
from enum import Enum
from typing import List

from icecream import ic

from lang_chain.zhipu_chat import chat_with_ai
from model.graph_entity.search_model import _Value
from model.graph_entity.search_service import search
from qa.prompt_templates import get_question_parser_prompt
from qa.question_type import QuestionType, QUESTION_MAP


def parse_question(question: str) -> QuestionType:
    """
    问题意图识别，目前识别为七类
    :param question:
    :return:
    """
    # 由于大模型分类准确率还不够，这里暂时打个补丁，用于判别文献检索增强的情况
    if "文献" in question[:20] and "参考" in question[:20]:
        return QuestionType.DOCUMENT

    prompt = get_question_parser_prompt(question)
    parse_result = chat_with_ai(prompt)
    question_type = QUESTION_MAP[parse_result]
    ic(question_type)

    return question_type


def check_entity(question: str) -> List[_Value] | None:
    """
    检查问题中是否包含实体
    :param question:
    :return:
    """
    code, msg, results = search(question)
    if code == 0:
        return results

    else:
        return None
