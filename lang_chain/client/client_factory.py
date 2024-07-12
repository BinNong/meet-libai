# -*- coding: utf-8 -*-
# @Time    : 2024/6/17 12:41
# @Author  : nongbin
# @FileName: client_factory.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
from env import get_env_value
from lang_chain.client.baichuan.client import BaichuanClient
from lang_chain.client.client_error import ClientUrlFormatError, ClientAPIUnsupportedError
from lang_chain.client.client_provider import ClientProvider
from lang_chain.client.deepseek.client import DeepseekClient
from lang_chain.client.doubao.client import DoubaoClient
from lang_chain.client.lingyiwanwu.client import LingyiwanwuClient
from lang_chain.client.llm_client_generic import LLMClientGeneric
from lang_chain.client.moonshot.client import MoonshotClient
from lang_chain.client.ollama.client import OllamaClient
from lang_chain.client.qwen.client import QwenClient
from lang_chain.client.zhipu.client import ZhipuClient
from lang_chain.client.oneapi.client import OneAPIClient
from utils.singleton import Singleton
from utils.url_paser import is_valid_url


class ClientFactory(metaclass=Singleton):
    _client_provider_mappings = {
        "https://open.bigmodel.cn/api/paas/v4/": ClientProvider.ZHIPU,
        "https://open.bigmodel.cn/api/paas/v4": ClientProvider.ZHIPU,
        "https://api.moonshot.cn/v1/": ClientProvider.MOONSHOT,
        "https://api.moonshot.cn/v1": ClientProvider.MOONSHOT,
        "https://api.baichuan-ai.com/v1/": ClientProvider.BAICHUAN,
        "https://api.baichuan-ai.com/v1": ClientProvider.BAICHUAN,
        "https://dashscope.aliyuncs.com/compatible-mode/v1/": ClientProvider.QWEN,
        "https://dashscope.aliyuncs.com/compatible-mode/v1": ClientProvider.QWEN,
        "https://api.lingyiwanwu.com/v1/": ClientProvider.LINGYIWANWU,
        "https://api.lingyiwanwu.com/v1": ClientProvider.LINGYIWANWU,
        "https://api.deepseek.com/": ClientProvider.DEEPSEEK,
        "https://ark.cn-beijing.volces.com/api/v3/": ClientProvider.DOUBAO,
        "https://ark.cn-beijing.volces.com/api/v3": ClientProvider.DOUBAO,
        get_env_value("LLM_BASE_URL"):ClientProvider.ONEAPI

    }

    def __init__(self):
        self._client_url = get_env_value("LLM_BASE_URL")
        self._api_key = get_env_value("LLM_API_KEY")
        self._sanity_check()

    @property
    def client_provider(self):
        return self._client_provider

    @property
    def client_url(self):
        return self._client_url

    @property
    def api_key(self):
        return self._api_key

    def _sanity_check(self):
        if not is_valid_url(self._client_url):
            raise ClientUrlFormatError("client url provided is not a url string")

        # if self._client_url not in self._client_provider_mappings:
        #     raise ClientAPIUnsupportedError("Invalid client API")

        if self._client_url in self._client_provider_mappings:
            self._client_provider = self._client_provider_mappings[self._client_url]
        elif self.api_key == "ollama":
            self._client_provider = ClientProvider.OLLAMA
        else:
            self._client_provider = ClientProvider.UNKNOWN

    def get_client(self) -> LLMClientGeneric:
        if self._client_provider == ClientProvider.ZHIPU:
            return ZhipuClient()

        if self._client_provider == ClientProvider.MOONSHOT:
            return MoonshotClient()

        if self._client_provider == ClientProvider.BAICHUAN:
            return BaichuanClient()

        if self._client_provider == ClientProvider.QWEN:
            return QwenClient()

        if self._client_provider == ClientProvider.LINGYIWANWU:
            return LingyiwanwuClient()

        if self._client_provider == ClientProvider.DEEPSEEK:
            return DeepseekClient()

        if self._client_provider == ClientProvider.DOUBAO:
            return DoubaoClient()

        if self._client_provider == ClientProvider.OLLAMA:
            return OllamaClient()
        if self._client_provider==ClientProvider.ONEAPI:
            return OneAPIClient()
        raise ClientAPIUnsupportedError("No client API adapted")


if __name__ == "__main__":
    factory1 = ClientFactory()
    factory2 = ClientFactory()

    print(factory1 is factory2)
