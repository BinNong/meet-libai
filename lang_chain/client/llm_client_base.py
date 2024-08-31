# -*- coding: utf-8 -*-
# @Time    : 2024/6/17 09:29
# @Author  : nongbin
# @FileName: llm_client_base.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
from abc import abstractmethod, ABCMeta, ABC
from typing import List, Dict, Tuple

from openai import OpenAI, Stream
from openai.types.chat import ChatCompletion, ChatCompletionChunk

from env import get_env_value
from utils.singleton import Singleton


class LLMClientBase(object):
    def __init__(self):
        self.__client = OpenAI(
            api_key=get_env_value("LLM_API_KEY"),
            base_url=get_env_value("LLM_BASE_URL"),
        )
        self.__model_name = get_env_value("MODEL_NAME")

    @property
    def client(self) -> OpenAI:
        return self.__client

    @property
    def model_name(self) -> str:
        return self.__model_name

    @abstractmethod
    def chat_with_ai(self, prompt: str) -> str | None:
        raise NotImplementedError()

    @staticmethod
    def construct_messages(prompt: str, history: List[List | None]) -> List[Dict[str, str]]:
        pass

    @abstractmethod
    def chat_with_ai_stream(self, prompt: str,
                            history: List[List[str]] | None = None) -> ChatCompletion | Stream[ChatCompletionChunk]:
        raise NotImplementedError()

    @abstractmethod
    def chat_using_messages(self, messages: List[Dict]) -> str | None:
        raise NotImplementedError()

    @abstractmethod
    def chat_on_tools(self, prompt: str, tools: List[Dict], history: List[List[str]] | None = None) -> (
            Tuple[str, Dict] | None):
        raise NotImplementedError()
