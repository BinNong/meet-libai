# -*- coding: utf-8 -*-
# @Time    : 2024/2/23 16:59
# @Author  : nongbin
# @FileName: zhipu_images.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn

from zhipuai import ZhipuAI

from env import get_env_value

__client = ZhipuAI(api_key=get_env_value("ZHIPUAI_API_KEY"))


def generate(text):
    response = __client.images.generations(
        model="cogview-3",  # 填写需要调用的模型名称
        prompt=text,
    )

    return response.data[0].url
