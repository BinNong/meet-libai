# -*- coding: utf-8 -*-
# @Time    : 2024/6/17 10:06
# @Author  : nongbin
# @FileName: client.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
import requests

from lang_chain.client.llm_client_generic import LLMClientGeneric
from logger import Logger


class OllamaClient(LLMClientGeneric):
    """
    Ollama AI Client
    """
    _logger: Logger = Logger("OllamaClient")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._check_ollama_running()

    def _check_ollama_running(self):
        """
        Check if the Ollama server is running.
        """
        base_url = str(self.client.base_url).split("/v1")[0]
        try:
            response = requests.get(base_url)
            if response.status_code == 200:
                self._logger.info("Ollama server is running")
            else:
                self._logger.warning(f"URL returned status code {response.status_code}")
        except requests.ConnectionError:
            self._logger.error("Failed to connect to the URL")
