# -*- coding: utf-8 -*-
# @Time    : 2024/3/8 23:04
# @Author  : nongbin
# @FileName: similarity_request.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn

from pydantic import BaseModel, Field


class SimilarityRetrieveQuery(BaseModel):
    message: str = Field(..., title="your query string", description="this is can be any length")
    search_type: str = Field(default="similarity", title="define how to search",
                             description="Optional['similarity', 'mmr']")
