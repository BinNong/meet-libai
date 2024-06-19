# -*- coding: utf-8 -*-
# @Time    : 2024/2/15 07:37
# @Author  : nongbin
# @FileName: api.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
import json
from typing import Annotated

from fastapi import Query, Request, Body
from fastapi.applications import FastAPI

from lang_chain.client.client_factory import ClientFactory
from lang_chain.retriever.knowledge_graph_retriever import generate_graph_info
from model.graph_entity.search_service import search
from model.rag.retriever_service import search as retriever_search
from web.api.body.fake_openai_request import ChatRequest
from web.api.body.kg_info_retrieve_request import KgInfoRetrieveRequest
from web.api.body.similarity_request import SimilarityRetrieveQuery
from web.api.examples import similarity_retrieve_query


def register_routes(app: FastAPI):
    @app.get('/api/echo', description="用于测试http接口通信是否正常", tags=["hello"])
    async def echo(
            say: Annotated[str, Query(example="hello")],
            do: Annotated[str, Query(example="just do it")],
            request: Request,
    ):
        return {say: do, "access host": request.client.host}

    @app.get('/api/graph/entity/search', description="搜索实体", tags=["graph-search"],
             response_model=None)
    async def graph_entity_search(
            query: Annotated[str, Query(example="李白和杜甫的关系是什么", max_length=128, min_length=2,
                                        description="问题的输入，该输入可能包含很多关系实体", )],
    ):
        code, msg, result = search(query)
        return {
            "code": code,
            "msg": msg,
            "data": result
        }

    @app.post('/api/rag/search', description="rag检索知识库", tags=["rag-search"])
    async def rag_search(
            request_item: Annotated[SimilarityRetrieveQuery, Body(
                examples=[similarity_retrieve_query]
            )],
            request: Request,
    ):
        query = request_item.message
        search_type = request_item.search_type
        docs = retriever_search(query, search_type)

        return {
            "code": 200,
            "msg": "success",
            "data": [doc.page_content for doc in docs]
        }

    @app.post("/v1/chat/completions")
    def generate_text(chat_request: Annotated[ChatRequest, Body()]):
        response =  ClientFactory().get_client().client.chat.completions.create(
            model=chat_request.model,
            messages=[m.model_dump() for m in chat_request.messages],
            top_p=0.7,
            temperature=chat_request.temperature,
            max_tokens=chat_request.max_tokens,
            stream=chat_request.stream,
        )
        """
        返回示例
        {
          "created": 1703487403,
          "id": "8239375684858666781",
          "model": "glm-4",
          "request_id": "8239375684858666781",
          "choices": [
              {
                  "finish_reason": "stop",
                  "index": 0,
                  "message": {
                      "content": "智绘蓝图，AI驱动 —— 智谱AI，让每一刻创新成为可能。",
                      "role": "assistant"
                  }
              }
          ],
          "usage": {
              "completion_tokens": 217,
              "prompt_tokens": 31,
              "total_tokens": 248
          }
        }
        """
        return response.dict()

    @app.post("/update_graph")
    def update_graph(graph_request: Annotated[KgInfoRetrieveRequest, Body()]):

        try:
            result = generate_graph_info(graph_request.text)
            clean_response = result.replace('```', '').strip()
            graph_data = json.loads(clean_response)
            return graph_data
        except Exception as e:
            return {'error': f"Error parsing graph data: {str(e)}"}
