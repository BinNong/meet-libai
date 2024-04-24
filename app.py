# -*- coding: utf-8 -*-
# @Time    : 2024/3/31 20:46
# @Author  : nongbin
# @FileName: app.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn

# run api_backend and web_ui in different thread
import threading

from api_backend import run_api
from utils.schedule import get_scheduler
from webui import run_webui


def create_app():
    # 创建并启动API后端线程
    api_backend_thread = threading.Thread(target=run_api)
    api_backend_thread.start()

    get_scheduler().start()

    # 创建并启动Web UI线程
    # web_ui_thread = threading.Thread(target=run_webui)
    # web_ui_thread.start()
    run_webui()


if __name__ == '__main__':
    # create_app.serve(name="libai")
    create_app()
