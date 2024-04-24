# -*- coding: utf-8 -*-
# @Time    : 2024/3/13 22:10
# @Author  : nongbin
# @FileName: fake_openai.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
from langchain_openai import ChatOpenAI

from config.config import Config

__port = int(Config.get_instance().get_with_nested_params("server", "port"))
__inference_server_url = f"http://localhost:{__port}/v1"

_chat = ChatOpenAI(
    model="glm-4",
    openai_api_key="EMPTY",
    openai_api_base=__inference_server_url,
    max_tokens=1024,
    temperature=0.95,
    stream=True,
)


def get_openai_chat_model() -> ChatOpenAI:
    return _chat
