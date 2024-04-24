# -*- coding: utf-8 -*-
# @Time    : 2024/2/1 10:53
# @Author  : nongbin
# @FileName: search_service.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
import threading
from typing import List, Any, Tuple, Optional

from model.graph_entity.search_model import INSTANCE, _Value


def search(query: str) -> Tuple[int, Optional[str], List[_Value] | None]:
    results, msg = INSTANCE.search(query)
    if results is not None:
        return 0, None, results
    else:
        return -1, f"model is not working: <{msg}>", None


def check(words: List[str]):
    result, msg = INSTANCE.search(words)
    if msg is None:
        return 0, None, result

    else:
        return -1, f"model is not working: <{msg}>", None
