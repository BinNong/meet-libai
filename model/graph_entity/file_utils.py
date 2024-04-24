# -*- coding: utf-8 -*-
# @Time    : 2024/1/31 15:10
# @Author  : nongbin
# @FileName: file_utils.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
import json
import os
from functools import singledispatch
from types import NoneType
from typing import Optional, Tuple

from py2neo import Node

from config.config import Config
from env import get_app_root

FIELD_NAMES = list(Config.get_instance().get_with_nested_params("cache", "node", "fields"))
CACHE_DIR = os.path.join(get_app_root(), "data/cache/node_entity")
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)


def generate_md5_file_name():
    """
    利用md5生成随机文件名
    :return:
    """
    import hashlib
    import random
    import string
    # 生成一个随机的文件名
    random_file_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    # 计算MD5哈希值
    md5_hash = hashlib.md5(random_file_name.encode()).hexdigest()
    return md5_hash


def check_cache_file() -> Tuple[Optional[str], int]:
    """
    根据版本号检查缓存文件是否存在, 如果存在返回缓存文件路径，如果不存在返回None
    :return:
    """
    version = 0
    # 第一步，提取版本号
    for file in os.listdir(CACHE_DIR):
        if file.endswith('.json'):
            with open(os.path.join(CACHE_DIR, file), 'r', encoding='utf-8') as f:
                meta_info = json.load(f)
                version = int(meta_info['version'])
                break
    # 第二步，检查缓存文件是否存在
    for file in os.listdir(CACHE_DIR):
        if file.startswith("entities") and int(file.split('-')[1]) == version:
            return os.path.join(CACHE_DIR, file), version
    return None, version


def get_version() -> int:
    """
    获取缓存文件的版本号
    :return:
    """

    _, version = check_cache_file()

    return version


@singledispatch
def get_cache_file_writer(version):
    """
    如果version为空，表示缓存元节点，为整数，表示缓存实体节点
    这里使用了单分派函数，根据形参的类型来决定调用哪个函数，也就是函数的重载，singledispatch仅支持包含一个形参的函数重载
    如果要想支持多参数重载，可以使用multipledispatch，第三方包pip install multipledispatch
    python函数重载的最佳理解：https://martinheinz.dev/blog/50
    :param version:
    :return:
    """
    pass


@get_cache_file_writer.register
def _(version: NoneType):
    # 返回缓存元节点的写入对象
    class Writer:
        def __init__(self):
            ...

        @staticmethod
        def write(meta_node: Node):
            cache_meta_path = os.path.join(CACHE_DIR, f"meta.json")
            with open(cache_meta_path, 'w', encoding='utf-8') as f:
                if meta_node['timestamp']:
                    meta_node['timestamp'] = str(meta_node['timestamp'])
                json.dump(meta_node, f, ensure_ascii=False, indent=4)

    return Writer()


@get_cache_file_writer.register
def _(version: int):
    # 返回缓存数据节点的写入对象
    cache_node_path = os.path.join(CACHE_DIR, f"entities-{version}-{generate_md5_file_name()}.csv")
    # 第一行写入列名
    with open(cache_node_path, 'w', encoding='utf-8') as f:
        f.write(",".join(FIELD_NAMES))
        f.write("\n")

    class Writer:
        def __init__(self):
            self.file_handle = open(cache_node_path, 'a', encoding='utf-8')

        @property
        def cache_file(self):
            return cache_node_path

        def write(self, data_node: Node):
            row = [str(data_node[field]).replace("\n", " ").strip() for field in FIELD_NAMES]
            line = ",".join(row)
            self.file_handle.write(line + "\n")

        def __del__(self):
            self.file_handle.flush()
            self.file_handle.close()

    return Writer()
