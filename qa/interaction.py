# -*- coding: utf-8 -*-
# @Time    : 2024/2/23 19:33
# @Author  : nongbin
# @FileName: interaction.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
import time

from icecream import ic

from qa.answer import get_answer
from qa.question_type import QuestionType


def chat_libai(message, history):
    ic(history)
    ic(message)
    answers = get_answer(message, history)

    if (answers[-1] == QuestionType.BASIC_INFO or
            answers[-1] == QuestionType.RELATION):
        for i in range(len(answers[0])):
            time.sleep(0.05)
            yield answers[0][: i + 1]

    elif (answers[-1] == QuestionType.CHINESE2POETRY or
          answers[-1]==QuestionType.POETRY2POETRY):
        yield answers[0]

    elif (answers[-1] == QuestionType.HELLO or
          answers[-1] == QuestionType.UNKNOWN):

        partial_message = answers[0][0]

        for chunk in answers[0][1]:
            partial_message = partial_message + chunk.choices[0].delta.content
            yield partial_message

    elif (answers[-1] == QuestionType.IMAGES or
          answers[-1] == QuestionType.AUDIO or
          answers[-1] == QuestionType.VIDEOS):  # 返回图片、音频或视频
        yield answers[0]

    elif answers[-1] == QuestionType.DOCUMENT:

        partial_message = ""

        for chunk in answers[0][1]:
            partial_message += chunk.choices[0].delta.content
            yield partial_message

        partial_message += answers[0][0]
        yield partial_message
