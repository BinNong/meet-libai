# -*- coding: utf-8 -*-
# @Time    : 2024/2/24 22:03
# @Author  : nongbin
# @FileName: client.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
from zhipuai import ZhipuAI

from env import get_env_value

__client = ZhipuAI(api_key=get_env_value("ZHIPUAI_API_KEY"))


def get_ai_client() -> ZhipuAI:
    return __client
