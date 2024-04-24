# -*- coding: utf-8 -*-
# @Time    : 2024/1/30 10:51
# @Author  : nongbin
# @FileName: data_utils.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
from dataclasses import dataclass, field
from pathlib import Path

from py2neo import Node

from dao.graph.graph_dao import GraphDao
from model.graph_entity.accelerate import NODE_ASYNC_IO
from model.graph_entity.file_utils import check_cache_file, FIELD_NAMES, get_cache_file_writer


@dataclass
class NodeEntities(object):
    """
    节点实体缓存类
    """
    dao: GraphDao = field(default_factory=lambda: GraphDao(), init=True, compare=False)

    # 类属性,一般以下划线开头
    ...

    @staticmethod
    def _read_cache_file(cache_file_path: Path):
        with cache_file_path.open('r', encoding='utf-8') as f:
            # 读取第一行表头, 获取各个字段的名称
            field_names = next(f).strip().split(",")
            # 读取各行
            for line in f:
                row = line.strip().split(",")
                yield Row(**dict(zip(field_names, row)))

    def get_entities_iterator(self) -> Node:
        # 先找本地缓存文件
        cache_file, version = check_cache_file()
        if cache_file and version == self.dao.query_data_version():  # ⚠️这里要判断版本号，确保缓存文件与数据库中的数据版本一致
            yield from self._read_cache_file(Path(cache_file))

        # 本地没有缓存文件或者版本号过低，则从数据库中读取，同时也将缓存文件写入本地
        else:
            # 写入元数据
            meta_node = self.dao.query_meta_node()
            if not meta_node:
                raise ValueError("没有找到元数据节点，请先创建元数据节点")

            meta_writer = get_cache_file_writer(None)
            meta_writer.write(meta_node)
            # 写入节点数据
            # 为了提高读写效率，采用异步方式读取数据库和写入缓存，生产者和消费者模式
            NODE_ASYNC_IO.run()

            # 程序运行到这里，已经存在缓存文件了，可以再次调用自己
            yield from self.get_entities_iterator()

    def __call__(self, *args, **kwargs):
        return self.get_entities_iterator()


class Row:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return ",".join([f"{name}:{self.__dict__[name]}" for name in FIELD_NAMES])

    def __str__(self):
        return self.__repr__()

    def __getitem__(self, item):
        if item not in self.__dict__:
            raise KeyError(f"{item} not found in row")
        return self.__dict__[item]
