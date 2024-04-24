# -*- coding: utf-8 -*-
# @Time    : 2024/2/24 20:33
# @Author  : nongbin
# @FileName: edge_audio.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn

# !/usr/bin/env python3

"""
Basic example of edge_tts usage.
"""

import asyncio
import datetime
import hashlib
import os.path
from pathlib import Path

from apscheduler.schedulers.background import BackgroundScheduler
import edge_tts

from env import get_app_root
from logger import Logger
from utils.schedule import get_scheduler

_logger: Logger = Logger(Path(__file__).name)

_OUTPUT_DIR = os.path.join(get_app_root(), "data/cache/audio")

# 如果文件夹路径不存在，先创建
if not os.path.exists(_OUTPUT_DIR):
    os.makedirs(_OUTPUT_DIR)


def get_file_path(text):
    file_name = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return os.path.join(_OUTPUT_DIR, f"{file_name}.mp3")


def generate(text: str, model_name: str) -> str:
    _output_file = get_file_path(text)

    async def _generating() -> None:
        communicate = edge_tts.Communicate(text, model_name)
        await communicate.save(_output_file)

    asyncio.run(_generating())

    return _output_file


def clear_audio_cache():
    for file in os.listdir(_OUTPUT_DIR):
        file_path = os.path.join(_OUTPUT_DIR, file)

        creation_time = os.path.getctime(file_path)
        current_time = datetime.datetime.now().timestamp()

        if current_time - creation_time > 600:
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                _logger.error(f"删除文件时出错：{e}")


get_scheduler().add_job(clear_audio_cache, "interval", seconds=10, id="clear_audio_cache")
