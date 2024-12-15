# -*- coding: utf-8 -*-
# @Time    : 2024/12/8 10:46
# @Author  : nongbin
# @FileName: poetry_game.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
"""
 <h3> 飞花令 💐 </h3>

> 举杯邀明月，对影成三人。
> 月落乌啼霜满天，江枫渔火对愁眠。
> 小楼一夜听春雨，深巷明月到人来。
> 疏影横斜水清浅，暗香浮动月黄昏。

```
[^10:00]: 剩余时间
```
"""

from enum import Enum, auto

from dao.redis.redis_dao import RedisDao
from lang_chain.client.client_factory import ClientFactory
from lang_chain.client.llm_client_generic import LLMClientGeneric
from qa.supported_tool_calling.utils import ChatResponse
from utils.singleton import Singleton


class GameMode(Enum):
    """
    Enumeration of different QA models for different interaction scenarios
    """
    FOG_MODEL = auto()  # For the Flying-flower Order Game（飞花令） questions and interactions


class PoetryGame(object, metaclass=Singleton):
    """
    The class to manage the game model
    """
    mode: GameMode = None
    poetry_cache = RedisDao()
    _chat_client = ClientFactory().get_client()
    def __init__(self):
        self._prefix = {GameMode.FOG_MODEL: "# [飞花令💐]\n\n"}
        self._suffix = {GameMode.FOG_MODEL: "\n\n```剩余时间: {time}```"}
        self._preface = {GameMode.FOG_MODEL: "```> 游戏开始，请说出一首古诗，包含“月”字，然后等待对方回复吧！```"}
        self._ending_words = "游戏结束，感谢参与!🏄‍♂🏄‍♂"

    def construct_fog_prompt(self, message: str) -> str:
        """
        古诗词飞花令提示词，包含“月”字的古诗词，并且不能重复
        :param message: 当前用户说出的古诗词
        :param history: 已经说出的古诗词
        :return:
        """
        prompt_template = """
        你正在参与古诗词飞花令游戏，请说出包含“月”字的古诗词，并且不能和下面的古诗词重复：\n
        {poetry}\n
        注意：只需给出一句诗句就可以，不需要额外的解释信息，不需要引号。
        """
        used_poetries = self.poetry_cache.get_set_members(str(self.mode))
        return prompt_template.format(poetry=str(used_poetries))

    def start_game(self, game_mode):
        self.mode = game_mode
        response = ChatResponse(prefix=self._prefix[self.mode] + self._preface[self.mode])

        yield from response()

    def end_game(self):
        self.poetry_cache.delete_set(str(self.mode))
        self.mode = None

        yield from ChatResponse(prefix=self._ending_words)()

    def play(self, message, history, game_mode):
        self.mode = game_mode
        if self.mode == GameMode.FOG_MODEL:
            yield from self._play_fog(message)
        else:
            raise NotImplementedError("Game mode not supported")

    def _play_fog(self, message: str):
        message = message.strip()

        if self.poetry_cache.is_member(str(self.mode), message):
            ttl = self.poetry_cache.get_set_ttl(str(self.mode))
            yield from ChatResponse(suffix="该诗已存在，请换一首吧🥀" + self._suffix[self.mode].format(time=ttl))()
            return  # The return keyword is used to stop the generator and raise a StopIteration exception
        else:
            self.poetry_cache.add_to_set(str(self.mode), message)

        messages = LLMClientGeneric.construct_messages(self.construct_fog_prompt(message), [])

        content = self._chat_client.chat_using_messages(messages)
        self.poetry_cache.add_to_set(str(self.mode), content)

        if not self.poetry_cache.has_expiration(str(self.mode)):
            self.poetry_cache.set_expiration(str(self.mode), 60 * 10)  # 10 minutes

        ttl = self.poetry_cache.get_set_ttl(str(self.mode))
        yield from ChatResponse(prefix=self._prefix[self.mode],
                                suffix=content + self._suffix[self.mode].format(time=ttl))()
