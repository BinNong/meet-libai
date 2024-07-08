# -*- coding: utf-8 -*-
# @Time    : 2024/7/8 20:45
# @Author  : nongbin
# @FileName: client.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
from lang_chain.client.llm_client_generic import LLMClientGeneric


class DoubaoClient(LLMClientGeneric):
    """
    豆包 AI Client
    """
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
