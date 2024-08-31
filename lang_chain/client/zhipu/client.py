# -*- coding: utf-8 -*-
# @Time    : 2024/6/17 10:02
# @Author  : nongbin
# @FileName: client.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
from overrides import override

from lang_chain.client.llm_client_generic import LLMClientGeneric


class ZhipuClient(LLMClientGeneric):
    """
    Zhipu AI Client
    """

    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @override
    def generate_image(self, prompt: str):
        response = self.client.images.generate(
            model="cogview-3",  # 填写需要调用的模型名称
            prompt=prompt,
        )

        return response.data[0].url
