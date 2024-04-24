# -*- coding: utf-8 -*-
# @Time    : 2024/2/17 12:23
# @Author  : nongbin
# @FileName: manage.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
import threading
from typing import Annotated, Dict

from fastapi import FastAPI, Query

from model.graph_entity.search_model import INSTANCE as GRAPH_ENTITY_SEARCHER
from model.model_error import ModelLoadError, ModelBuildError, ModelError, ModelDisplayError
from model.rag.retriever_model import INSTANCE as RAG_RETRIEVER
from model.model_base import ModelBase, ModelStatus

__MODEL_INSTANCE: Dict[str, ModelBase] = {
    GRAPH_ENTITY_SEARCHER.name: GRAPH_ENTITY_SEARCHER,
    RAG_RETRIEVER.name: RAG_RETRIEVER,
}


def __model_adapter(model_name: str) -> ModelBase:
    if model_name not in __MODEL_INSTANCE:
        raise ModelError(f"{model_name} is not a valid model name")
    return __MODEL_INSTANCE[model_name]


def register_routes(app: FastAPI):
    @app.put('/manage/model/reload',
             description="模型加载",
             tags=["! reload model"])
    async def reload(
            model_name: Annotated[str, Query(example="graph_entity_searcher,rag_retriever")],
            version: Annotated[int | None, Query(gt=0)] = None,
    ):
        try:
            model = __model_adapter(model_name)
            model.reload(version)
        except ModelLoadError as e:
            return {
                "code": e.code,
                "message": e.__repr__()
            }

        except ModelError as e:
            return {
                "code": e.code,
                "message": e.__repr__()
            }

        return {
            "code": 0,
            "message": "success"
        }

    @app.put('/manage/model/build',
             description="模型构建",
             tags=["! build model"])
    async def build(
            model_name: Annotated[str, Query(example="graph_entity_searcher,rag_retriever")],
            description: Annotated[str, Query(max_length=200, description="descript why you build this model")] = "",
    ):

        try:
            model = __model_adapter(model_name)
        except ModelBuildError as e:
            return {
                "code": e.code,
                "message": e.__repr__()
            }
        except ModelError as e:
            return {
                "code": e.code,
                "message": e.__repr__()
            }

        # 在这里启动一个新的线程，用于模型构建
        threading.Thread(
            target=model.build,
            kwargs={"description": description}
        ).start()

        return {
            "code": 0,
            "message": "model is building"
        }

    @app.put('/manage/model/display',
             description="指定模型展示",
             tags=["! displaying model"])
    async def display(
            model_name: Annotated[str, Query(example="graph_entity_searcher,rag_retriever")],
            version: Annotated[int, Query(example=1, gt=0, description="version of model")] = None,
    ):
        try:
            model = __model_adapter(model_name)
            model_info = model.display(version)

        except ModelDisplayError as e:
            return {
                "code": e.code,
                "message": e.__repr__()
            }
        except ModelError as e:
            return {
                "code": e.code,
                "message": e.__repr__()
            }

        return {
            "code": 0,
            "message": "model display success",
            "data": model_info
        }

    @app.put('/manage/model/display/all',
             description="所有模型展示",
             tags=["! displaying all model"])
    async def display_all(

    ):
        model_infos = []
        try:
            for model in __MODEL_INSTANCE.values():
                if model.model_status != ModelStatus.READY:
                    continue

                model_info = model.display()
                model_infos.append(model_info)

        except ModelDisplayError as e:
            return {
                "code": e.code,
                "message": e.__repr__()
            }
        except ModelError as e:
            return {
                "code": e.code,
                "message": e.__repr__()
            }

        return {
            "code": 0,
            "message": f"there are/is {len(model_infos)} models valid",
            "data": model_infos
        }
