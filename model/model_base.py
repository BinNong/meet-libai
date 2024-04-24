# -*- coding: utf-8 -*-
# @Time    : 2024/1/31 12:37
# @Author  : nongbin
# @FileName: model_base.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
import json
import os
import shutil
import time
from abc import abstractmethod
from datetime import datetime
from enum import Enum
from typing import List, Optional

from model.model_error import ModelDisplayError, ModelLoadError


class ModelStatus(str, Enum):
    """
    模型状态枚举类型
    这里为什么使用多继承，原因是解决json序列化问题
    参考：https://stackoverflow.com/questions/24481852/serialising-an-enum-member-to-json
    """
    INITIAL = "initial"
    BUILDING = "building"
    READY = "ready"
    FAILED = "failed"
    INVALID = "invalid"
    DELETED = "deleted"
    UNKNOWN = "unknown"


class ModelBase(object):
    """
    模型基类，用于定义模型的基本属性和方法
    """
    _model_path_base = None
    _max_history_versions = 5
    _model_info = dict()

    def __init__(self
                 , name=None
                 , *
                 , version=0
                 , history_versions: Optional[List[int]] = None
                 , description=""
                 , created_time=""
                 , updated_time=""
                 , creator=""
                 , model_type=""
                 , model_status: ModelStatus = ModelStatus.INITIAL
                 , **kwargs):
        self._name: str = name
        self._version: int = version
        self._history_versions: List[int] = history_versions or []
        self._description: str = description
        self._created_time: str = created_time
        self._updated_time: str = updated_time
        self._creator: str = creator
        self._model_type: str = model_type
        self._model_status: ModelStatus = model_status
        self.__kwargs = kwargs
        self._post_init_(**kwargs)

    def _post_init_(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, f"_{key}", value)

    @property
    def name(self):
        return self._name

    @property
    def version(self):
        return self._version

    @property
    def description(self):
        return self._description

    @property
    def created_time(self):
        return self._created_time

    @property
    def updated_time(self):
        return self._updated_time

    @property
    def creator(self):
        return self._creator

    @property
    def model_type(self):
        return self._model_type

    @property
    def model_status(self):
        return self._model_status

    # 如果找不到属性就进入这个魔法函数
    def __getattr__(self, item):
        return self.__dict__[f"_{item}"]

    @abstractmethod
    def build(self, *args, **kwargs):
        """
        构建模型
        """
        pass

    def dump(self, *args, **kwargs):
        """
        模型落地
        :return:
        """
        pass

    def reload(self, version: Optional[int]):
        """
        加载模型
        """
        pass

    def _to_dict(self, **kwargs):
        """
        将模型属性转换为字典
        """
        dict_ = {
            "name": self._name,
            "version": self._version,
            "description": self._description,
            "created_time": self._created_time,
            "updated_time": self._updated_time,
            "creator": self._creator,
            "model_type": self._model_type,
            "model_status": self._model_status,
        }
        dict_.update(self.__kwargs)
        dict_.update(kwargs)

        return dict_

    def _from_dict(self, data):
        """
        从字典中加载模型属性
        """
        self._name = data.get("name")
        self._version = data.get("version")
        self._description = data.get("description")
        self._created_time = data.get("created_time")
        self._updated_time = data.get("updated_time")
        self._creator = data.get("creator")
        self._model_type = data.get("model_type")
        self._model_status = data.get("model_status")

        return self

    def _dump_model_info(self, **kwargs):
        """
        dump model info to file
        """

        self._model_info.update(self._to_dict(
            created_time=datetime.now().strftime("%Y-%m-%d, %H:%M:%S"),
            **kwargs))

        if not self._model_info:
            raise ValueError("model info is empty, please build first")

        with open(self.get_model_info_path(self.version, create=True), 'w', encoding="utf-8") as f:
            json.dump(self._model_info, f, ensure_ascii=False, indent=4)

    def _dump_model(self):
        ...

    def _load_model_info(self, version: int):
        """
        load model info from file
        """
        if not os.path.exists(self.get_model_info_path(version)):
            self._model_status = ModelStatus.FAILED
            raise ModelLoadError("model info file not found")

        with open(self.get_model_info_path(version), 'r', encoding="utf-8") as f:
            self._model_info = json.load(f)

        self._from_dict(self._model_info)

    @abstractmethod
    def _load_model(self, version: int):
        ...

    def get_history_versions(self):
        """
        获取模型的历史版本
        :return:
        """

        versions_ = []
        if not os.path.exists(self._model_path_base):
            return versions_

        for version in os.listdir(self._model_path_base):
            if not version.isdigit():
                continue

            versions_.append(int(version))

        versions_ = sorted(versions_)

        return versions_

    def _remove_obsolete_versions(self):
        """
        删除过时的模型
        :return:
        """

        versions_ = self.get_history_versions()

        if len(versions_) >= self._max_history_versions:
            obsolete_versions = set(versions_) - set(versions_[-self._max_history_versions + 1:])

            for version in obsolete_versions:
                path_ = os.path.join(self._model_path_base, str(version))
                shutil.rmtree(path_)

                self._logger.info(f"Removed obsolete model version {version}")

    def get_model_path(self, version: int, create: bool = False):
        if not os.path.exists(self._model_path_base):
            os.makedirs(self._model_path_base)

        path_ = os.path.join(self._model_path_base, str(version), "model")
        dir_ = os.path.dirname(path_)

        if not os.path.exists(dir_) and create:
            os.makedirs(dir_)

        return path_

    def get_model_info_path(self, version: int, create: bool = False):
        if not os.path.exists(self._model_path_base):
            os.makedirs(self._model_path_base)

        path_ = os.path.join(self._model_path_base, str(version), "model_info.json")
        dir_ = os.path.dirname(path_)

        if not os.path.exists(dir_) and create:
            os.makedirs(dir_)

        return path_

    def get_latest_model_version(self):

        versions = self.get_history_versions()

        if len(versions) == 0:
            return 0
        else:
            return versions[-1]

    def display(self, version: int = None):
        if version is None:
            return self._model_info

        model_info_path = self.get_model_info_path(version)
        if not os.path.exists(model_info_path):
            raise ModelDisplayError("Could not find model info file")

        with open(model_info_path, 'r', encoding="utf-8") as f:
            return json.load(f)
