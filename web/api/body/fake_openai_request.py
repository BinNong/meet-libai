# -*- coding: utf-8 -*-
# @Time    : 2024/3/13 22:17
# @Author  : nongbin
# @FileName: fake_openai_request.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
from typing import Optional, List, Union

from pydantic import BaseModel, Field


class Message(BaseModel):
    role: str = Field(..., exclude=False)
    content: str = Field(..., exclude=False)


class ResponseFormat(BaseModel):
    type_: str


class ToolChoice(BaseModel):
    type_: str
    function: Optional[dict]


class ChatRequest(BaseModel):
    messages: List[Message]
    model: str
    frequency_penalty: Optional[float] = 0
    logit_bias: Optional[dict] = None
    logprobs: Optional[Union[bool, None]] = False
    top_logprobs: Optional[Union[int, None]] = None
    max_tokens: Optional[Union[int, None]] = None
    n: Optional[Union[int, None]] = 1
    presence_penalty: Optional[float] = 0
    response_format: Optional[ResponseFormat] = None
    seed: Optional[Union[int, None]] = None
    stop: Optional[Union[str, List[str], None]] = None
    stream: Optional[Union[bool, None]] = False
    temperature: Optional[float] = 0.95
    top_p: Optional[float] = 1
    tools: Optional[List[str]] = None
    tool_choice: Optional[Union[str, ToolChoice]] = None
    user: Optional[str] = None
