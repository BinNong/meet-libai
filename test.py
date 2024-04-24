# -*- coding: utf-8 -*-
# @Time    : 2024/1/26 21:56
# @Author  : nongbin
# @FileName: test.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
# 单元测试
import asyncio
import json
import os
import time
import unittest

from icecream import ic

from dao.graph.graph_dao import GraphDao
from lang_chain.edge_audio import generate as generate_audio
from lang_chain.poetry_search import search_by_chinese
from lang_chain.retriever.audio_text_retriever import extract_language, extract_gender, get_tts_model_name
from lang_chain.retriever.document_retriever import create_history_aware_query, retrieve_docs
from lang_chain.retriever.image_text_retriever import extract_text as extract_image_text
from lang_chain.sora_video import generate as generate_video
from lang_chain.zhipu_chat import chat_with_ai, chat_with_ai_stream
from model.graph_entity.data_utils import NodeEntities
from model.graph_entity.file_utils import generate_md5_file_name
from model.graph_entity.node_io_processor_coroutine import NodeIOProcessor as NodeIOProcessorCoroutine
from model.graph_entity.node_io_processor_thread import NodeIOProcessor as NodeIOProcessorThread
from model.graph_entity.search_model import INSTANCE
from qa.answer import get_answer
from qa.question_parser import parse_question, QuestionType


class TestLangChain(unittest.TestCase):

    def test_zhipuai(self):
        prompt = "你知道王安石和苏洵是什么关系吗？"
        prompt_template = f"{prompt}\n请你对以上内容进行文本分类，类别有三种，分别为：人物关系，人物基本信息，其他. 比如：李白和杜甫是什么关系，文本分类结果是人物关系，张三是谁，文本分类结果是人物基本信息。请直接给出分类结果，不要解释，不要多余的内容，不要多余的符号，不要多余的空格，不要多余的空行，不要多余的换行，不要多余的标点符号，不要多余的括号。"
        print(chat_with_ai(prompt_template))

    def test_zhipuai_md(self):
        prompt = "用python写冒泡排序？"
        print(chat_with_ai(prompt))

    def test_stream(self):
        prompt = "你是谁"
        result = chat_with_ai_stream(prompt)
        ic(result)

    def test_generate_audio(self):
        generate_audio("床前明月光，疑是地上霜。举头望明月，低头思故乡。")

    def test_question_parser(self):
        question_type = parse_question("请根据以上内容帮我生成一段语音")
        self.assertEqual(question_type, QuestionType.AUDIO)

        prompt = "请根据参考文献回答下面问题"
        question_type = parse_question(prompt)
        self.assertEqual(question_type, QuestionType.DOCUMENT)

        question_type = parse_question("请根据以下白话文来搜索相应的古文，朋友应该怎么相处")
        self.assertEqual(question_type, QuestionType.CHINESE2POETRY)

    def test_poetry_search(self):
        result = search_by_chinese("如何孝敬父母")
        json.dump(result, open("poetry.json", "w", encoding="utf-8"))
        print(result)

    def test_extract_image_text(self):
        text = extract_image_text("请帮我生成李白在江边垂钓的图片")
        print(text)

    def test_extract_language(self):
        text = extract_language("请帮我把这首诗用陕西话转成语音")
        self.assertEqual("陕西话", text)
        text = extract_language("请用粤语念一下这段话")
        self.assertEqual("粤语", text)
        text = extract_language("请帮我把这首诗转成语音")
        self.assertEqual("无", text)
        text_ = extract_gender("请帮我把这首诗转成女声语音")
        self.assertEqual("女声", text_)

    def test_doc_retriever(self):
        history = [
            ["李白是谁", "李白是唐代诗人"],
        ]
        query = "李白是哪里人"
        new_query = create_history_aware_query(history, query)
        docs = retrieve_docs(new_query)
        print(docs)

    def test_extract_gender(self):
        text_ = extract_gender("请帮我把这首诗用陕西话转成语音")
        self.assertEqual("无", text_)
        text_ = extract_gender("请用粤语念一下这段话")
        self.assertEqual("无", text_)
        text_ = extract_gender("请帮我把这首诗转成语音")
        self.assertEqual("无", text_)
        text_ = extract_gender("请用男声念一下这段话")
        self.assertEqual("男声", text_)
        text_ = extract_gender("请帮我把这首诗转成女声语音")
        self.assertEqual("女声", text_)

    def test_get_tts_model_name(self):
        name = get_tts_model_name(lang="陕西话", gender="女声")
        print(name)


class TestGraphDao(unittest.TestCase):

    def test_query_node_libai(self):
        nodes = GraphDao().query_node("人物", name="李白")
        iterator = iter(nodes)
        while True:
            try:
                name = next(iterator)["name"]
                self.assertEqual(name, "李白")
                ic(name)
            except StopIteration:
                break

    def test_query_nodes(self):
        nodes = GraphDao().query_node("人物")
        for node in nodes:
            ic(node)

    def test_create_meta_node(self):
        meta_node = GraphDao().create_meta_node(1)
        ic(meta_node)

    def test_query_meta_node(self):
        meta_node = GraphDao().query_meta_node()
        ic(meta_node)

    def test_update_version(self):
        meta_node = GraphDao().update_version()
        ic(meta_node)

    def test_cyper(self):
        nodes = GraphDao().run_cypher("""MATCH (n:人物{name:'李白'}) RETURN n""").data()
        print(nodes)


class TestUtils(unittest.TestCase):

    def test_generate_md5_file_name(self):
        result = generate_md5_file_name()
        self.assertEqual(len(result), 32, "Length  of  MD5  hash  should  be  32  characters")
        ic(result)


class TestNodeIOProcessor(unittest.TestCase):
    def test_node_io_processor_multi_thread(self):
        processor = NodeIOProcessorThread()
        processor.run()

    def test_node_io_processor_coroutine(self):
        processor = NodeIOProcessorCoroutine()
        asyncio.run(processor.main())


class TestEntitySearcher(unittest.TestCase):
    def test_build_entity_searcher(self):
        searcher = INSTANCE
        searcher.build()

    def test_reload_latest_entity_searcher(self):
        searcher = INSTANCE
        searcher.reload()

        self.assertEqual(True, searcher.search(["李白"])[0])

    def test_reload_history_entity_searcher(self):
        searcher = INSTANCE
        searcher.reload(version=2)

        self.assertEqual(True, searcher.search(["李白"])[0])

    def test_search_word(self):
        searcher = INSTANCE
        searcher.build()

        self.assertEqual(True, searcher.search(["李白"]))

    def test_search_query(self):
        searcher = INSTANCE
        searcher.build()
        self.assertEqual("李白", searcher.search("李白")[0].name)


class TestDataUtils(unittest.TestCase):

    def test_get_node_entities(self):
        node_entities = NodeEntities()
        for i, node in enumerate(node_entities()):
            ic(node)

        self.assertEqual(i, 2453 - 1)


class TestQa(unittest.TestCase):
    def test_qa_loop(self):
        while True:
            input_ = input("\n请输入您的问题：")
            if input_ == "退出":
                break
            answers = get_answer(input_)
            if isinstance(answers, str):
                for i, char in enumerate(answers):
                    time.sleep(0.05)
                    print(char, end="", flush=True)
                    if i % 40 == 0:
                        print()

            elif isinstance(answers, tuple):
                print(answers[0])
                for chunk in answers[1]:
                    time.sleep(0.05)
                    print(chunk.choices[0].delta.content, end="", flush=True)


class TestSoraVideo(unittest.TestCase):
    def test_video_generator(self):
        print(generate_video("您好，世界"))

class TestMkdir(unittest.TestCase):
    def test(self):
        os.mkdir("temp/1")

if __name__ == '__main__':
    unittest.main()
