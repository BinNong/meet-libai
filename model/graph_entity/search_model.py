# -*- coding: utf-8 -*-
# @Time    : 2024/1/28 17:36
# @Author  : nongbin
# @FileName: search_model.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
import json
import os
import pickle
from collections import namedtuple
from typing import List, Tuple, Optional

import ahocorasick as pyahocorasick
from multipledispatch import dispatch

from config.config import Config
from dao.graph.graph_dao import GraphDao
from env import get_app_root
from logger import Logger
from model.graph_entity.data_utils import NodeEntities
from model.graph_entity.file_utils import FIELD_NAMES, get_version
from model.model_base import ModelBase, ModelStatus
from model.model_error import ModelLoadError

_Value = namedtuple("_Value", (fn for fn in FIELD_NAMES))


class EntitySearcher(ModelBase):
    """
    使用ac自动机匹配关键词
    """
    _name = "graph_entity_searcher"
    _model_path_base = os.path.join(get_app_root(), f"data/model/{_name}")
    _logger: Logger = Logger(_name)
    _search_key = Config.get_instance().get_with_nested_params("model", "graph-entity", "search-key")

    def __init__(self, *args, **kwargs):
        super().__init__(name=self._name)
        self._model = None
        self._model_info = {}
        self._dao = GraphDao()
        self._node_entities = NodeEntities()

    def build(self, *args, **kwargs):
        self._logger.info("building entity searcher")
        self._model_status = ModelStatus.BUILDING

        try:
            self._build_model()
        except Exception as e:
            self._logger.error(f"failed to build entity searcher: {e}")
            self._model_status = ModelStatus.FAILED
            return

        self._model_status = ModelStatus.READY
        self._model_info.update(kwargs)
        self._logger.logger.opt(colors=True).info("successfully <blue>built</blue> entity searcher")

        self.dump()

    def dump(self, **kwargs):
        self._logger.info("dumping entity searcher")

        self._remove_obsolete_versions()

        self._dump_model()
        self._dump_model_info(**kwargs)

        self._logger.logger.opt(colors=True).info("successfully <blue>dumped</blue> entity searcher")

    def reload(self, version: Optional[int] = None):
        if not version:
            version = self._version = get_version()

        self._logger.logger.opt(colors=True).info(f"<red>loading</red> entity searcher [version:{version}]")

        self._load_model_info(version)
        if self._model_status == ModelStatus.READY:

            self._load_model(version)
            self._logger.info(f"successfully <blue>loaded</blue> entity searcher [version:{version}]")

        else:
            version = self.get_history_versions().pop()
            if version:
                self.reload(version)
            else:
                self._logger.logger.opt(colors=True).error("<red>failed to load entity searcher</red>")
                self._model_status = ModelStatus.FAILED
                raise ModelLoadError("not found any version of entity searcher")

    def _build_model(self):
        automaton = pyahocorasick.Automaton()

        for i, entity in enumerate(self._node_entities()):
            value = _Value(*(entity[fn] for fn in FIELD_NAMES))
            automaton.add_word(entity[self._search_key], (i, value))

        automaton.make_automaton()

        self._model = automaton
        self._version = get_version()

    def _dump_model(self):
        """
        dump automaton to file
        """
        if not self._model:
            raise ValueError("automaton is empty, please build first")

        with open(self.get_model_path(self.version, create=True), 'wb') as f:
            pickle.dump(self._model, f)

    def _load_model(self, version: int):
        """
        load automaton from file
        """
        if not os.path.exists(self.get_model_path(version)):
            self._model_status = ModelStatus.FAILED
            raise ValueError("automaton file not found")

        with open(self.get_model_path(version), 'rb') as f:
            self._model = pickle.load(f)



    @dispatch(list)
    def search(self, words) -> Tuple[Optional[bool], Optional[ModelStatus]]:
        """
        to check whether the given words are in automaton or not
        :param words:
        :return:
        """
        if self._model_status == ModelStatus.READY:
            for word in words:
                if word not in self._model:
                    return False, None

            return True, None

        elif self.model_status == ModelStatus.INITIAL:
            INSTANCE.reload()
            self.search(words)

        else:
            return None, self._model_status

    @dispatch(str)
    def search(self, query: str) -> Tuple[Optional[List[_Value]], Optional[ModelStatus]]:
        """
        search value by  query
        :param query:
        :return:
        """

        if self._model_status == ModelStatus.READY:
            results = []
            for end_index, (insert_order, original_value) in self._model.iter(query):
                results.append(original_value)

            return results, None

        elif self._model_status == ModelStatus.INITIAL:
            INSTANCE.reload()
            return self.search(query)

        else:
            return None, self._model_status


INSTANCE = EntitySearcher()
