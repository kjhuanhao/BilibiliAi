# -*- coding:utf-8 -*-
# @FileName  : ai_message.py
# @Time      : 2023/8/22
# @Author    : LaiJiahao
# @Desc      : AI交互类

import requests
import toml
import tiktoken
import random

from common.video_info import BilibiliVideoInfo
from typing import Tuple, List, Dict
from prompt.summary_prompt import summary_single_system_prompt, summary_multiple_system_prompt
from common.handler import retry_on_exception
from common.log import log


class CustomLLM:
    config = toml.load("config.toml")
    API_KEY = config["openai"]["api_key"]
    CHAT_URL = "https://api.openai.com/v1/chat/completions"

    def __init__(self):
        pass

    def summary(self, video_info: BilibiliVideoInfo) -> str:
        subtitle = video_info.subtitle
        texts = self.get_text_spliter(subtitle, 15000)
        log.info(f"视频字幕分割完成，共{len(texts)}段")
        prompt = f"视频标题: {video_info.title}\n 视频简介: {video_info.desc}\n 视频字幕: {texts[0]}"
        last_summary = self.get_json_completion(summary_single_system_prompt + prompt)

        if len(texts) == 1:
            return "\n摘要:\n" + last_summary["summary"].replace("\n", "") + "\n亮点:\n" + "".join(["- " + highlight.replace("\n", "") + "\n" for highlight in last_summary["highlights"]])
        summary = last_summary["summary"]
        highlights = last_summary["highlights"]

        for text in texts[1:]:
            log.info(f"正在处理第{texts.index(text) + 1}段")
            prompt = f"视频参考信息: {summary}\n 视频字幕: {text}"
            current_summary = self.get_json_completion(summary_multiple_system_prompt + prompt)
            summary += current_summary["summary"]
            highlights += current_summary["highlights"]

        return "\n摘要:\n" + summary.replace("\n", "") + "\n亮点:\n" + "".join(["- " + highlight.replace("\n", "") + "\n" for highlight in highlights])

    @retry_on_exception(3)
    def get_json_completion(self, prompt: str) -> Dict:
        headers = {
            "Authorization": f"Bearer {self.API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-3.5-turbo-16k",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        resp = requests.post(
            self.CHAT_URL,
            headers=headers,
            json=data)
        print(resp.json())
        content = resp.json()["choices"][0]["message"]["content"]

        return eval(content)

    def get_text_spliter(self, text: str, max_token: int) -> List[str]:
        if len(text) == 0:
            return [text][:-1]
        split_text, max_length = self._recursive_text_spliter(text, max_token, len(text))
        remaining_text = text[max_length:]
        return [split_text] + self.get_text_spliter(remaining_text, max_token)

    def _recursive_text_spliter(
            self,
            text: str,
            max_token: int,
            max_length: int
    ) -> Tuple[str, int]:
        text_tokens = self.get_tokens(text)

        if text_tokens < max_token:
            return text, max_length

        recursive_length = max_length - random.randint(100, 1000)
        if recursive_length < 0:
            return text, max_length

        text = text[:recursive_length]

        return self._recursive_text_spliter(text, max_token, recursive_length)

    @staticmethod
    def get_tokens(text) -> int:
        if len(text) == 0:
            return 0
        """or cl100k_base"""
        encoding = tiktoken.get_encoding("cl100k_base")
        token_integers = encoding.encode(text)
        tokens = len(token_integers)
        return tokens
