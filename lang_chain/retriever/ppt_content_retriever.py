# -*- coding: utf-8 -*-
# @Time    : 2024/5/12 15:22
# @Author  : nongbin
# @FileName: ppt_content_retriever.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
import json
from typing import List, Dict

from lang_chain.client import get_ai_client

# 输出格式
__output_format = json.dumps({
    "title": "example title",
    "pages": [
        {
            "title": "title for page 1",
            "content": [
                {
                    "title": "title for paragraph 1",
                    "description": "detail for paragraph 1",
                },
                {
                    "title": "title for paragraph 2",
                    "description": "detail for paragraph 2",
                },
            ],
        },
        {
            "title": "title for page 2",
            "content": [
                {
                    "title": "title for paragraph 1",
                    "description": "detail for paragraph 1",
                },
                {
                    "title": "title for paragraph 2",
                    "description": "detail for paragraph 2",
                },
                {
                    "title": "title for paragraph 3",
                    "description": "detail for paragraph 3",
                },
            ],
        },
    ],
}, ensure_ascii=True)

_GENERATE_PPT_PROMPT_ = f'''请你根据用户要求生成ppt的详细内容，不要省略。按这个JSON格式输出{__output_format}，只能返回JSON，且JSON不要用```包裹，不要返回markdown格式'''


def __construct_messages(question: str, history: List[List | None]) -> List[Dict[str, str]]:
    messages = [
        {"role": "system",
         "content": "你现在扮演信息抽取的角色，要求根据用户输入和AI的回答，正确提取出信息。"}]

    for user_input, ai_response in history:
        messages.append({"role": "user", "content": user_input})
        messages.append(
            {"role": "assistant", "content": repr(ai_response)})

    messages.append({"role": "user", "content": question})
    messages.append({"role": "user", "content": _GENERATE_PPT_PROMPT_})

    return messages


def generate_ppt_content(question: str,
                         history: List[List | None] | None = None) -> str:
    response = get_ai_client().chat.completions.create(
        model="glm-4",
        messages=__construct_messages(question, history),
        top_p=0.7,
        temperature=0.95,
        max_tokens=1024,
    )

    return response.choices[0].message.content
