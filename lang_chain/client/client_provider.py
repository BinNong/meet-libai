# -*- coding: utf-8 -*-
# @Time    : 2024/6/17 13:02
# @Author  : nongbin
# @FileName: client_provider.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
from enum import Enum


class ClientProvider(Enum):
    """
    used to distinguish the client provider
    """

    UNKNOWN = None
    ZHIPU = "zhipu"
    BAICHUAN = "baichuan"
    QWEN = "qwen"
    MOONSHOT = "moonshot"
    LINGYIWANWU = "lingyiwanwu"
    DEEPSEEK = "deepseek"
    OLLAMA = "ollama"
