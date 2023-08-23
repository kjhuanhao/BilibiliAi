# -*- coding:utf-8 -*-
# @FileName  : video_info.py
# @Time      : 2023/8/22
# @Author    : LaiJiahao
# @Desc      : 视频信息实体类


class BilibiliVideoInfo:
    def __init__(
            self,
            id_: str,
            cid: str,
            title: str,
            desc: str,
            subtitle: str
    ):
        self.id_ = id_
        self.cid = cid
        self.title = title
        self.desc = desc
        self.subtitle = subtitle

    def __str__(self):
        return f"id: {self.id_}, cid: {self.cid}, title: {self.title}, desc: {self.desc}, subtitle: {self.subtitle}"
