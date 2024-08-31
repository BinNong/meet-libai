# -*- coding: utf-8 -*-
# @Time    : 2024/6/17 09:38
# @Author  : nongbin
# @FileName: llm_client_generic.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
import json
from typing import List, Dict, Tuple

from openai import Stream
from openai.types.chat import ChatCompletion, ChatCompletionChunk
from overrides import override

from env import get_env_value
from lang_chain.client.llm_client_base import LLMClientBase
from utils.singleton import Singleton


class LLMClientGeneric(LLMClientBase, metaclass=Singleton):
    """
    LLMClientGeneric is a generic LLM client that can be used to interact with any language model. But if you want to
    specify the model name, you can extend LLMClientBase.
    """

    def __init__(self, *args, **kwargs):
        super().__init__()

    @override
    def chat_with_ai(self, prompt: str) -> str | None:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "user", "content": prompt},
            ],
            top_p=0.7,
            temperature=0.95,
            max_tokens=1024,
        )

        return response.choices[0].message.content

    @staticmethod
    def construct_messages(prompt: str, history: List[List | None]) -> List[Dict[str, str]]:
        messages = [
            {"role": "system", "content": "你是一个乐于解答各种问题的助手，你的任务是为用户提供专业、准确、有见地的回答。"}]

        for user_input, ai_response in history:
            messages.append({"role": "user", "content": user_input})
            messages.append(
                {"role": "assistant", "content": ai_response.__repr__()})

        messages.append({"role": "user", "content": prompt})
        return messages

    @override
    def chat_with_ai_stream(self, prompt: str, history: List[List[str]] | None = None) -> ChatCompletion | Stream[
        ChatCompletionChunk]:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=self.construct_messages(prompt, history if history else []),
            top_p=0.7,
            temperature=0.95,
            max_tokens=1024,
            stream=True,
        )

        return response

    @override
    def chat_using_messages(self, messages: List[Dict]) -> str | None:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            top_p=0.7,
            temperature=0.95,
            max_tokens=1024,
        )

        return response.choices[0].message.content

    @override
    def chat_on_tools(self, prompt: str, tools: List[Dict], history: List[List[str]] | None = None) -> (
            Tuple[str, Dict] | None):
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=self.construct_messages(prompt, history or []),
            tools=tools,
            tool_choice="auto"
        )
        if response.choices[0].message.tool_calls is None:
            return None
        function_name: str = response.choices[0].message.tool_calls[0].function.name
        function_args: Dict = json.loads(response.choices[0].message.tool_calls[0].function.arguments)

        return function_name, function_args

    def generate_image(self, prompt: str):
        raise NotImplementedError