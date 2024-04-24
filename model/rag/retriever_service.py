# -*- coding: utf-8 -*-
# @Time    : 2024/3/6 22:00
# @Author  : nongbin
# @FileName: retriever_service.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
from typing import List, Any

from langchain_core.documents import Document

from model.rag.retriever_model import INSTANCE


def retrieve(query: str) -> List[Document]:
    docs = INSTANCE.retriever.invoke(query)

    return docs


def search(query: str, search_type: str, **kwargs: Any) -> List[Document]:
    docs = INSTANCE.vector_db.search(query, search_type, **kwargs)
    return docs
