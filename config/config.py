# -*- coding: utf-8 -*-
# @Time    : 2023/11/18 10:41
# @Author  : nongbin
# @FileName: config.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
import threading
from functools import lru_cache

import yaml
import os

from env import get_app_root


class Config(object):
    __instance = None
    __lock = threading.Lock()

    def __init__(self):
        self._config = None

    @classmethod
    def get_instance(cls):
        with cls.__lock:
            if cls.__instance is None:
                cls.__instance = cls._load_config()
            return cls.__instance

    @classmethod
    def _load_config(cls):
        instance = Config()
        root = get_app_root()
        env = os.environ.get("PY_ENVIRONMENT")
        with open(os.path.join(root, "config", f"config-{env}.yaml"), "r", encoding="utf-8") as f:
            setattr(instance, "_config", yaml.load(f, Loader=yaml.FullLoader))

        return instance

    @lru_cache(maxsize=128)
    def get_with_nested_params(self, *params):
        assert self._config is not None, "please load config first"
        conf = self._config
        for param in params:
            if param in conf:
                conf = conf[param]
            else:
                raise KeyError(f"{param} not found in config")

        return conf


if __name__ == "__main__":
    print(get_app_root())
