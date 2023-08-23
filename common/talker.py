# -*- coding:utf-8 -*-
# @FileName  : talker.py
# @Time      : 2023/8/21
# @Author    : LaiJiahao
# @Desc      : None

class Talker:
    def __init__(self, talker_id: str, content: str, ack_seqno: str):
        self.talker_id = talker_id
        self.content = content
        self.ack_seqno = ack_seqno

    def __str__(self):
        return f"talker_id: {self.talker_id}, content: {self.content}, ack_seqno: {self.ack_seqno}"
