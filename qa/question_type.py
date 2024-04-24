# -*- coding: utf-8 -*-
# @Time    : 2024/2/24 21:28
# @Author  : nongbin
# @FileName: question_type.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
from enum import Enum


class QuestionType(Enum):
    """
    问题类型
    """
    UNKNOWN = 0
    BASIC_INFO = 1
    RELATION = 2
    IMAGES = 3
    VIDEOS = 4
    AUDIO = 5
    DOCUMENT = 6
    HELLO = 7
    CHINESE2POETRY = 8
    POETRY2POETRY = 9


QUESTION_MAP = {
    # "诗人简历": QuestionType.BASIC_INFO,
    "人物关系": QuestionType.RELATION,
    "其他": QuestionType.UNKNOWN,
    "图片生成": QuestionType.IMAGES,
    "视频生成": QuestionType.VIDEOS,
    "音频生成": QuestionType.AUDIO,
    # "检索增强": QuestionType.DOCUMENT,
    "问候语": QuestionType.HELLO,
    "以古文搜古文":QuestionType.POETRY2POETRY,
    "以白话文搜古诗文": QuestionType.CHINESE2POETRY,
}
