# -*- coding: utf-8 -*-
# @Time    : 2024/1/30 14:47
# @Author  : nongbin
# @FileName: node_io_processor_thread.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
import queue
import threading

from icecream import ic
from py2neo import Node

from dao.graph.graph_dao import GraphDao

from model.graph_entity.file_utils import get_cache_file_writer


class NodeIOProcessor:
    def __init__(self):
        self._queue = queue.Queue()
        self._dao = GraphDao()
        self._writer = None

    @property
    def writer(self):
        return self._writer

    def producer(self):
        nodes = self._dao.query_node('人物')
        for node in nodes:
            node["labels"] = "-".join(list(node.labels))  # 这里要独立添加labels标签作为key，因为Node类型没有这个key
            self._queue.put(node)
            # ic(f"Produced {node}")
        self._queue.put(Node("Done"))

    def consumer(self):
        # 先获取版本号
        version = self._dao.query_data_version()
        # 获取写入类
        self._writer = get_cache_file_writer(version)

        while True:
            node: Node = self._queue.get()
            if "Done" in node.labels:
                break
            # print(f"Consumed {node}")
            self._writer.write(node)
            self._queue.task_done()

    def run(self):
        producer_thread = threading.Thread(target=self.producer, args=())
        consumer_thread = threading.Thread(target=self.consumer, args=())

        producer_thread.start()
        consumer_thread.start()

        producer_thread.join()
        consumer_thread.join()
