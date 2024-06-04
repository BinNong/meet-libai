# -*- coding: utf-8 -*-
# @Time    : 2024/5/12 15:58
# @Author  : nongbin
# @FileName: file_util.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
import datetime
import os


def clear_files_by_timediff(root_dir, time_interval: int):
    """
    根据文件创建时间删除指定时间间隔之外的文件
    :param root_dir: 指定要删除文件的根目录
    :param time_interval: 文件创建时间与当前时间的时间间隔,单位秒
    :return:
    """
    for file in os.listdir(root_dir):
        file_path = os.path.join(root_dir, file)

        creation_time = os.path.getctime(file_path)
        current_time = datetime.datetime.now().timestamp()

        if current_time - creation_time > time_interval:

            if os.path.isfile(file_path):
                os.unlink(file_path)
