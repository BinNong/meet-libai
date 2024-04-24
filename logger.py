# -*- coding: utf-8 -*-
# @Time    : 2024/1/31 17:57
# @Author  : nongbin
# @FileName: logger.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
import os.path
from typing import Optional

from loguru import logger

from env import get_app_root

if not os.path.exists(os.path.join(get_app_root(), "logs")):
    os.makedirs(os.path.join(get_app_root(), "logs"))

class Logger:
    """
    定义一个全局日志工具类，设置好路径、rotation等信息
    """

    def __init__(self, name: Optional[str] = None):
        """
        初始化日志工具类
        """
        # 设置日志文件路径
        self.logger = logger
        self.logger.add(os.path.join(get_app_root(), "logs", f"{name if name else 'file_{time}'}.log")
                        , rotation='10 MB'
                        , retention='30 days')

    def info(self, message):
        """
        输出INFO级别的日志
        :param message: 日志信息
        """
        self.logger.info(message)

    def debug(self, message):
        """
        输出DEBUG级别的日志
        :param message: 日志信息
        """
        self.logger.debug(message)

    def warning(self, message):
        """
        输出WARNING级别的日志
        :param message: 日志信息
        """
        self.logger.warning(message)

    def error(self, message):
        """
        输出ERROR级别的日志
        :param message: 日志信息
        """
        self.logger.error(message)
