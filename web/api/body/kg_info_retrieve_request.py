# -*- coding: utf-8 -*-
# @Time    : 2024/6/8 15:46
# @Author  : nongbin
# @FileName: kg_info_retrieve_request.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
from pydantic import BaseModel


class KgInfoRetrieveRequest(BaseModel):
    text: str