# -*- coding: utf-8 -*-
# @Time    : 2024/2/25 13:12
# @Author  : nongbin
# @FileName: sora_video.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
import requests

from env import get_env_value
from lang_chain.client.client_factory import ClientFactory

_SORA_API_URL = "https://fake-sora-api.sorawebui.com/v1/video/generations"


def generate(prompt):
    # Define the URL

    # Define the headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {get_env_value('OPENAI_API_KEY')}"  # 目前是假的api
    }
    # 将prompt翻译成英文，因为目前仅支持英文
    en_prompt =  ClientFactory().get_client().chat_with_ai(prompt=f"将以下中文翻译成英文（要求只返回翻译的部分，不要包含提示信息）：{prompt}")
    # Define the data to be sent in the request body
    data = {
        "model": "sora-1.0-turbo",
        "prompt": en_prompt,
        "size": "1920x1080"
    }

    # Send the POST request
    response = requests.post(_SORA_API_URL, headers=headers, json=data)
    _video_url = None
    if response.status_code == 200:
        _video_url = response.json()["data"][0]["url"]
    else:
        print("Error:", response.status_code, response.text)

    return _video_url
