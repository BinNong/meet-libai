# -*- coding: utf-8 -*-
# @Time    : 2024/3/31 21:11
# @Author  : nongbin
# @FileName: schedule.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
from apscheduler.schedulers.background import BackgroundScheduler

__scheduler = BackgroundScheduler()


def get_scheduler() -> BackgroundScheduler:
    return __scheduler
