# -*- coding: utf-8 -*-
# @Time    : 2024/3/2 15:30
# @Author  : nongbin
# @FileName: modelscope_embedding.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
from langchain_community.embeddings import ModelScopeEmbeddings

from config.config import Config
from model.model_base import ModelBase


class ModelScopeEmbedding(ModelBase):

    def __init__(self, model_name_or_path=None, device=None, **kwargs):
        super().__init__(**kwargs)
        self._vector_db = None
        if not model_name_or_path:
            model_name_or_path = Config.get_instance().get_with_nested_params("model", "embedding", "model-name")
        self._embedding = ModelScopeEmbeddings(model_id=model_name_or_path)

        if device:
            self._device = device
        else:
            self._device = Config.get_instance().get_with_nested_params("model", "embedding", "device")

    @property
    def embedding(self):
        return self._embedding
