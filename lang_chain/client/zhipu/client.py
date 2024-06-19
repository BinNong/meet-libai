# -*- coding: utf-8 -*-
# @Time    : 2024/6/17 10:02
# @Author  : nongbin
# @FileName: client.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
from lang_chain.client.llm_client_generic import LLMClientGeneric


class ZhipuClient(LLMClientGeneric):
    """
    Zhipu AI Client
    """

    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
