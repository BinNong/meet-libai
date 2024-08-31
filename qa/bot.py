# -*- coding: utf-8 -*-
# @Time    : 2024/8/21 17:56
# @Author  : nongbin
# @FileName: bot.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
from typing import Literal, TypeAlias, List

from config.config import Config
from qa.custom_tool_calling.interaction import chat_libai as chat_libai_by_custom_agent
from qa.supported_tool_calling.interaction import chat_libai as chat_libai_by_supported_agent
from utils.singleton import Singleton

Parser: TypeAlias = Literal['custom', 'tool_calling']


class ChatBot(object, metaclass=Singleton):
    """
    聊天机器人,供gradio调用
    """

    def __init__(self):
        self.question_parser: Parser = (
            Config.get_instance().get_with_nested_params("lang-chain", "question_parse"))

    def chat(self,
             message: str,
             history: List[List[str] | None] | None = None):
        if self.question_parser == 'custom':
            yield from chat_libai_by_custom_agent(message, history)
        elif self.question_parser == 'tool_calling':
            yield from chat_libai_by_supported_agent(message, history)
        else:
            raise ValueError(f"{self.question_parser} is not supported for question parser")
