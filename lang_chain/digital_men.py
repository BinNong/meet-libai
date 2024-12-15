# -*- coding: utf-8 -*-
# @Time    : 2024/9/27 11:36
# @Author  : nongbin
# @FileName: digital_men.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
from typing import Optional

import requests

from config.config import Config


# 生成数字人，函数的返回类型为URL
def generate(transcript: str) -> Optional[str]:
    url = Config.get_instance().get_with_nested_params("model", "digital-men")

    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "text": transcript
    }

    response = requests.post(url, headers=headers, json=data)

    try:
        video_link = response.json()["download_url"]
    except Exception as e:
        print("Error: {}".format(e))
        print("Failed to generate digital men")
        return None

    return video_link
