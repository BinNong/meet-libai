# -*- coding: utf-8 -*-
# @Time    : 2024/6/17 10:06
# @Author  : nongbin
# @FileName: client.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
from lang_chain.client.llm_client_generic import LLMClientGeneric


class QwenClient(LLMClientGeneric):
    """
    Qwen AI Client
    """
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

