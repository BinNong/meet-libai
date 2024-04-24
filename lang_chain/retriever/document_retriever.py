# -*- coding: utf-8 -*-
# @Time    : 2024/3/13 19:35
# @Author  : nongbin
# @FileName: document_retriever.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
from typing import List, Tuple

from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, \
    MessagesPlaceholder
from langchain_core.runnables import Runnable

from lang_chain.fake_openai import get_openai_chat_model
from lang_chain.zhipu_chat import chat_using_messages
from model.rag.retriever_service import retrieve


def create_history_aware_query(history: List[List], query: str) -> str | None:
    messages = []

    for user_input, ai_response in history:
        messages.append({"role": "user", "content": user_input})
        messages.append(
            {"role": "assistant", "content": ai_response.__repr__()})

    messages.append({"role": "user", "content": query})
    messages.append({"role": "user", "content": "根据以上的历史对话，请生成一个更加全面准确而且适合于大模型回答的问题。"})

    new_query = chat_using_messages(messages)
    return new_query


def create_context(docs: List[Document]):
    return "\n\n".join([doc.page_content for doc in docs])


def retrieve_docs(question: str) -> Tuple[str, List[Document]]:
    docs = retrieve(question)
    _context = create_context(docs)
    return _context, docs


# def get_rag_chain() -> Runnable:
#     prompt = ChatPromptTemplate.from_messages([
#         MessagesPlaceholder(variable_name="chat_history"),
#         ("user", "{input}"),
#         ("user", "根据以上的历史对话，请生成一个更加适合于搜索查询的问题。")
#     ])
#     better_query_retriever = create_history_aware_retriever(
#         get_openai_chat_model(),
#         rag_retriever.retriever,
#         prompt)
#
#     prompt = ChatPromptTemplate.from_messages([
#         ("system", "基于下面的上下文回答问题\n\n：{context}"),
#         MessagesPlaceholder(variable_name="chat_history"),
#         ("user", "{input}"),
#     ])
#
#     document_chain = create_stuff_documents_chain(get_openai_chat_model(), prompt)
#     retrieval_chain = create_retrieval_chain(better_query_retriever, document_chain)
#
#     return retrieval_chain


def wrap_chat_history(chats_history: List[List | None]):
    chat_history = []
    for human_message, ai_message in chats_history:
        chat_history.append(HumanMessage(content=human_message))
        chat_history.append(AIMessage(content=ai_message))

    return chat_history
