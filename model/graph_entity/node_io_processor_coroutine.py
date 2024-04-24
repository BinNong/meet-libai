# -*- coding: utf-8 -*-
# @Time    : 2024/1/31 10:23
# @Author  : nongbin
# @FileName: node_io_processor_coroutine.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
import asyncio

from icecream import ic
from py2neo import Node

from dao.graph.graph_dao import GraphDao
from model.graph_entity.file_utils import get_cache_file_writer


class NodeIOProcessor:
    """
    节点IO处理器,使用协程实现异步IO操作
    """

    def __init__(self):
        self._queue = asyncio.Queue()
        self._dao = GraphDao()
        self._writer = None

    @property
    def writer(self):
        return self._writer

    async def producer(self):
        nodes = self._dao.query_node('人物')
        for node in nodes:
            await self._queue.put(node)
            ic(f"Produced {node}")
        await self._queue.put(Node("Done"))

    async def consumer(self):
        # 先获取版本号
        version = self._dao.query_data_version()
        # 获取写入类
        self._writer = get_cache_file_writer(version)
        while True:
            node: Node = await self._queue.get()
            if "Done" in node.labels:
                break
            ic(f"Consumed {node}")
            self._writer.write(node)
            self._queue.task_done()

    async def main(self):
        producer_coroutine = self.producer()
        consumer_coroutine = self.consumer()
        await asyncio.gather(producer_coroutine, consumer_coroutine)
