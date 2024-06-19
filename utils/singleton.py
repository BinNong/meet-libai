# -*- coding: utf-8 -*-
# @Time    : 2024/6/16 22:13
# @Author  : nongbin
# @FileName: singleton.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
import threading


class Singleton(type):
    """
    单例模式
    """
    _instances = {}
    _lock = threading.Lock()  # 添加一个锁来确保线程安全

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:  # 使用锁来保护下面的代码块
                if cls not in cls._instances:  # 双重检查锁定
                    cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
