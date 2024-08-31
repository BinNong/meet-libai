# -*- coding: utf-8 -*-
# @Time    : 2024/8/21 17:59
# @Author  : nongbin
# @FileName: interaction.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
import inspect
from typing import List, Optional

from lang_chain.client.client_factory import ClientFactory
from qa.supported_tool_calling.tools import get_tools
from qa.supported_tool_calling.utils import ChatResponse


def chat_libai(question: str, history: List[Optional[List]] | None):
    tool = get_tools(question, history)

    if tool is None:
        response = ClientFactory().get_client().chat_with_ai_stream(question, history)
        yield from ChatResponse(response)()

    else:
        function, kwargs = tool

        if "history" in inspect.signature(function).parameters:
            kwargs["history"] = history

        tool_result = function(**kwargs)

        if isinstance(tool_result, ChatResponse):
            yield from tool_result()
        elif isinstance(tool_result, tuple):
            yield tool_result
        else:
            raise ValueError("Invalid result type")
