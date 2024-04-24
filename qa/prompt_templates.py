# -*- coding: utf-8 -*-
# @Time    : 2024/2/18 15:25
# @Author  : nongbin
# @FileName: prompt_templates.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
import os

from qa.question_type import QUESTION_MAP
organization_name = os.environ.get('PY_DEBUG')
QUESTION_PARSE_TEMPLATE = (f"你扮演文本分类的工具助手，类别有{len(QUESTION_MAP)}种，"
                           f"分别为：人物关系，图片生成，视频生成，音频生成，问候语，以白话文搜古诗文，以古文搜古文，其他。"
                           f"下面给出一些例子："
                           f"'李白和杜甫是什么关系'，文本分类结果是人物关系；"
                           # f"'某某是谁'，文本分类结果是诗人简历；"
                           f"'请生成李白在江边喝酒的图片'，文本分类结果是图片生成；"
                           f"'你可以生成一段关于春天的视频吗'，文本分类结果是视频生成；"
                           f"'请将上述文本转换成语音'，文本分类结果是音频生成；"
                           f"'请将这首诗转成语音'，文本分类结果是音频生成；"
                           f"'请朗读这首诗'，文本分类结果是音频生成；"
                           # f"'请根据相关文献，回答这个问题'，文本分类结果是检索增强；"
                           f"'您好！你是谁？'，文本分类结果是问候语；"
                           f"'请根据以下白话文来搜索古文，...'，文本分类结果是以白话文搜古诗文；"
                           f"'请根据以下古文来搜索古文,...'，文本分类结果是以古文搜古文；"
                           f"如果以上内容没有对应的类别，文本分类结果是其他。"
                           f"请参考上面例子，直接给出一种分类结果，不要解释，不要多余的内容，不要多余的符号，不要多余的空格，不要多余的空行，不要多余的换行，不要多余的标点符号，不要多余的括号。"
                           f"请你对以下内容进行文本分类：")

HELLO_ANSWER_TEMPLATE = f"""你是一位高级文案创作者，可以适当增加调皮的风格，请你帮我润色以下内容：\n我是[🍶遇见李白]，一个基于超级知识图谱的智能聊天机器人，旨在回答与李白相关的问题。由[{organization_name}]自主研发。🏫😊\n"""

LLM_HINT = "你是一位高级文案创作者，要求正式，请你帮我润色以下内容:\n <u>本地知识图谱信息有限，下面结合大模型给出答案：</u>\n"


def get_question_parser_prompt(text: str) -> str:
    """
    根据输入的文本生成prompt
    :param text: 输入的文本
    :return: prompt
    """

    return f"{QUESTION_PARSE_TEMPLATE}\n{text}"
