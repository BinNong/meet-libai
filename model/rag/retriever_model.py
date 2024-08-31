# -*- coding: utf-8 -*-
# @Time    : 2024/3/3 20:46
# @Author  : nongbin
# @FileName: retriever_model.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
import os.path
from abc import ABC

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.vectorstores.faiss import FAISS
from langchain_core.vectorstores import VST, VectorStoreRetriever

from env import get_app_root
from logger import Logger
from model.embedding.modelscope_embedding import ModelScopeEmbedding
from model.model_base import ModelBase, ModelStatus
from model.model_error import ModelLoadError, ModelError


class RagRetriever(ModelBase, ABC):
    """
    RAG 检索模型
    """
    _name = "rag_retriever"

    _vector: VST
    _retriever: VectorStoreRetriever
    _embedding = ModelScopeEmbedding().embedding

    _model_path_base = os.path.join(get_app_root(), f"data/model/{_name}")
    _pdf_data_path = os.path.join(get_app_root(), "data/corpus/retriever/pdf")  # todo: 目前仅支持pdf格式，后续可支持网页等其他格式

    _logger: Logger = Logger("rag_retriever")

    def __init__(self):
        super().__init__(self._name)

    def build(self, *args, **kwargs):

        self._version = self.get_latest_model_version() + 1
        self._logger.info(f"building version {self._version}")

        loader = PyPDFDirectoryLoader(path=self._pdf_data_path)
        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=240, chunk_overlap=40)
        documents = text_splitter.split_documents(docs)
        self._vector = FAISS.from_documents(documents, self._embedding)

        self._retriever = self._vector.as_retriever(search_kwargs={"k": 6})
        self._model_status = ModelStatus.READY

        self._logger.logger.opt(colors=True).info("vector db <red>built</red> successfully")

        self.dump(**kwargs)

    def reload(self, version: int | None = None):
        if not version:
            version = self.get_latest_model_version()

        self._logger.logger.opt(colors=True).info(f"<red>loading</red> vector db [version:{version}]")

        self._load_model_info(version)

        if self._model_status == ModelStatus.READY:
            try:
                self._load_model(version)
                self._logger.logger.opt(colors=True).info(f"successfully <blue>loaded</blue> vector db [version:{version}]")
            except Exception as e:
                self._logger.logger.opt(colors=True).error(f"failed to <red>load</red> vector db [version:{version}]")
                self._model_status = ModelStatus.INVALID
                raise ModelLoadError(repr(e))

        else:
            raise ModelLoadError(f"vector db [version:{version}] is invalid")

    def _load_model(self, version: int):
        """
        load retriever from file
        """
        model_path = self.get_model_path(version)

        if not os.path.exists(model_path):
            self._model_status = ModelStatus.FAILED

            self._logger.error("vector db file not found")
            raise ModelLoadError("vector db file not found")

        self._logger.info("loading vector db")
        self._vector = FAISS.load_local(model_path, self._embedding, allow_dangerous_deserialization=True)
        self._retriever = self._vector.as_retriever(search_kwargs={"k": 6})

    def dump(self, *args, **kwargs):
        self._remove_obsolete_versions()

        self._dump_model_info(**kwargs)
        self._dump_model()

        self._logger.logger.opt(colors=True).info("successfully <red>dumped</red> vector db")

    def _dump_model_info(self, **kwargs):
        super()._dump_model_info(engine="faiss", **kwargs)

    def _dump_model(self):
        model_path = self.get_model_path(version=self._version, create=True)
        self._vector.save_local(model_path)

    @property
    def retriever(self) -> VectorStoreRetriever:
        if self.model_status == ModelStatus.READY:
            return self._retriever
        elif self.model_status == ModelStatus.INITIAL or self._model_status == ModelStatus.INVALID:
            try:
                self._logger.warning("Model not loaded. Loading model...")
                self.reload()
                return self._retriever
            except ModelLoadError as e:
                self._logger.warning(f"Failed to load model: {e}"
                                     "\nAttempting to build model..."
                                     "\nThis may take a while..."
                                     "\nIf the error persists, please using management api.")
                self.build()
                return self._retriever

        raise ModelError("Model not built")

    @property
    def vector_db(self) -> VST:
        if self.model_status == ModelStatus.READY:
            return self._vector

        raise ModelError("Model not built")


INSTANCE = RagRetriever()
