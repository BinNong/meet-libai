# -*- coding: utf-8 -*-
# @Time    : 2024/6/8 15:33
# @Author  : nongbin
# @FileName: knowledge_graph_retriever.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
from lang_chain.client.client_factory import ClientFactory

json_example = {'edges': [{'data': {'color': '#FFA07A',
                                    'label': 'label 1',
                                    'source': 'source 1',
                                    'target': 'target 1'}},
                          {'data': {'color': '#FFA07A',
                                    'label': 'label 2',
                                    'source': 'source 2',
                                    'target': 'target 2'}}
                          ],
                'nodes': [{'data': {'color': '#FFC0CB', 'id': 'id 1', 'label': 'label 1'}},
                          {'data': {'color': '#90EE90', 'id': 'id 2', 'label': 'label 2'}},
                          {'data': {'color': '#87CEEB', 'id': 'id 3', 'label': 'label 3'}}]}

__retriever_prompt = f"""
                  You are an AI expert specializing in knowledge graph creation with the goal of capturing relationships based on a given input or request.
                  Based on the user input in various forms such as paragraph, email, text files, and more.
                  Your task is to create a knowledge graph based on the input.
                  Nodes must have a label parameter. where the label is a direct word or phrase from the input.
                  Edges must also have a label parameter, where the label is a direct word or phrase from the input.
                  Response only with JSON in a format where we can jsonify in python and feed directly into  cy.add(data), include 'color' property, to display a graph on the front-end.
                  you can reference the given example: {json_example}.
                  Make sure the target and source of edges match an existing node.
                  Do not include the markdown triple quotes above and below the JSON, jump straight into it with a curly bracket.
                """


def generate_graph_info(raw_text: str) -> str | None:
    """
    generate graph info from raw text
    :param raw_text:
    :return:
    """
    messages = [
        {"role": "system", "content": "你现在扮演信息抽取的角色，要求根据用户输入和AI的回答，正确提取出信息。"},
        {"role": "user", "content": raw_text},
        {"role": "user", "content": __retriever_prompt}
    ]

    graph_info_result = ClientFactory().get_client().chat_using_messages(messages)

    return graph_info_result
