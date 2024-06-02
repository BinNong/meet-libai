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

import edge_tts

from env import get_app_root
from logger import Logger
from utils.file_util import clear_files_by_timediff
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
    try:
        clear_files_by_timediff(_OUTPUT_DIR, datetime.timedelta(minutes=10).seconds)
    except Exception as e:
        _logger.error(f"clear_audio_cache error: {e}")


get_scheduler().add_job(clear_audio_cache, "interval", seconds=10, id="clear_audio_cache")
