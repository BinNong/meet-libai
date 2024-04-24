# -*- coding: utf-8 -*-
# @Time    : 2024/3/24 21:47
# @Author  : nongbin
# @FileName: rag_chain.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
import os
from typing import List, Tuple

from langchain_core.documents import Document
from zhipuai.core._sse_client import StreamResponse

from lang_chain.retriever.document_retriever import create_history_aware_query, retrieve_docs
from lang_chain.zhipu_chat import chat_with_ai_stream


def analyze_reference(docs: List[Document]) -> str:
    doc_names_pages = []

    for doc in docs:
        file_path = doc.metadata["source"]

        # 从文件路径中提取文件名
        name = ".".join(os.path.basename(file_path).split(".")[:-1])

        doc_names_pages.append(f">  {name} [第{doc.metadata['page']}页]")

    return "参考文献如下：\n```" + "\n".join(doc_names_pages) + "```\n"


def invoke(query: str, history: List[List[str]]) -> Tuple[str, StreamResponse]:
    new_query = create_history_aware_query(history, query)
    _context, docs = retrieve_docs(new_query)

    _prompt = f"""请基于提供的上下文回答下面的问题:
    {_context}
    问题: {query}"""

    response = chat_with_ai_stream(_prompt)
    doc_info = analyze_reference(docs)

    return doc_info, response
