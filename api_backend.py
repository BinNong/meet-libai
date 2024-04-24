# -*- coding: utf-8 -*-
# @Time    : 2024/1/24 21:07
# @Author  : nongbin
# @FileName: api_backend.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn

import os

import uvicorn
from fastapi import FastAPI

from config.config import Config
from web.api.api import register_routes as api_register_routes
from web.api.manage import register_routes as manage_register_routes

IS_DEV_ENV = os.environ.get('PY_ENVIRONMENT') == "dev"
IS_DEBUG = os.environ.get('PY_DEBUG') == "true"

def run_api():
    app = FastAPI(title=Config.get_instance().get_with_nested_params("api", "title"),
                  description=Config.get_instance().get_with_nested_params("api", "description"),
                  debug=IS_DEBUG)

    api_register_routes(app)
    manage_register_routes(app)

    uvicorn.run(app,
                host="0.0.0.0",
                port=int(Config.get_instance().get_with_nested_params("server", "port")),
                # root_path="/ml-backend",
                log_level="info" if IS_DEV_ENV else "warning"
                )


if __name__ == '__main__':
    run_api()
