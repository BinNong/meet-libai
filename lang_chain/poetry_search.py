# -*- coding: utf-8 -*-
# @Time    : 2024/4/12 22:26
# @Author  : nongbin
# @FileName: poetry_search.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
import json
from typing import List

import requests
from icecream import ic

from logger import Logger

__logger = Logger(__name__)


def __table2markdown(table: List[List]) -> str:
    # the first row is the header
    header = table[0]
    # the rest are the rows
    rows = table[1:]

    # create a Markdown table
    markdown_table = "| " + " | ".join(header) + " |\n| " + " | ".join(["---"] * len(header)) + " |"

    # add rows
    for row in rows:
        markdown_table += "\n| " + " | ".join(row) + " |"

    return markdown_table


def search_by_chinese(chinese_sentence: str) -> str:
    """
    白话文搜古文
    :param chinese_sentence:
    :return:
    """
    data = {
        "text": chinese_sentence,
        "conf_key": "chinese-poetry",
        "group": "default",
        "size": 6,
        "searcher": 1
    }
    ic(data)
    resp = requests.post("http://172.16.67.154:18880/api/search/nl", data=json.dumps(data))
    # if status_code is not 200, log the warning information and return empty list
    if resp.status_code != 200:
        __logger.error(f"search by chinese failed, status_code: {resp.status_code}")
        return "无法检索，可能是网络出问题了"

    data_resp = [["著作名", "篇章名", "正文", "译文"]]
    for item in resp.json()["values"]:
        row = item['value'].split("##@##")
        # row.append(item['score'])
        data_resp.append(row)

    markdown_table = __table2markdown(data_resp)

    return markdown_table


def search_by_poetry(chinese_sentence: str) -> str:
    """
    古文搜古文
    :param chinese_sentence:
    :return:
    """
    data = {
        "text": chinese_sentence,
        "conf_key": "chinese-classical",
        "group": "default",
        "size": 10,
        "searcher": 3
    }
    ic(data)
    resp = requests.post("http://172.16.67.154:18880/api/search/nl", data=json.dumps(data))
    # if status_code is not 200, log the warning information and return empty list
    if resp.status_code != 200:
        __logger.error(f"search by chinese failed, status_code: {resp.status_code}")
        return "无法检索，可能是网络出问题了"

    data_resp = [["作者", "完整诗篇", "篇名", "关键词"]]
    for item in resp.json()["values"]:
        row = item['value'].replace("|", "，").split("##@##")[1:]
        # row.append(item['score'])
        data_resp.append(row)

    markdown_table = __table2markdown(data_resp)

    return markdown_table
