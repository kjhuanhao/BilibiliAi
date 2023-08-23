# -*- coding:utf-8 -*-
# @FileName  : bilibili.py
# @Time      : 2023/8/21
# @Author    : LaiJiahao
# @Desc      : Bilibili工具类

import requests
import toml
import time
import random
import json
import re

from typing import List, Union
from common.talker import Talker
from common.video_info import BilibiliVideoInfo
from common.log import log


class Bilibili:
    config = toml.load("config.toml")

    UNREAD_URL = "https://api.vc.bilibili.com/session_svr/v1/session_svr/single_unread"
    GET_MESSAGE_URL = "https://api.vc.bilibili.com/session_svr/v1/session_svr/get_sessions"
    ACK_MESSAGE_URL = "https://api.vc.bilibili.com/session_svr/v1/session_svr/update_ack"
    SEND_MESSAGE_URL = "https://api.vc.bilibili.com/web_im/v1/web_im/send_msg"
    GET_VIDEO_INFO = "https://api.bilibili.com/x/web-interface/view"
    GET_SUBTITLE_URL = "https://api.bilibili.com/x/player/wbi/v2"

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203"
    }
    COOKIES = {
        "SESSDATA": config["bilibili"]["SESSDATA"]
    }
    bili_jct = config["bilibili"]["bili_jct"]
    uid = config["bilibili"]["uid"]

    def get_unread(self) -> int:
        """
        获取未读的消息
        :return: 未读的消息数量
        """
        resp = requests.get(self.UNREAD_URL, headers=self.HEADERS, cookies=self.COOKIES)
        unread_data = resp.json()["data"]
        follow_unread = unread_data["follow_unread"]
        return follow_unread

    def get_message(self) -> List[Talker]:
        """
        获取未处理确认的消息
        :return: 一个未读的消息列表（只返回与关注列表有关的消息）
        """
        params = {
            "session_type": 1,
            "group_fold": 1,
            "unfollow_fold": 0,
            "sort_rule": 2,
            "build": 0,
            "mobi_app": "web"
        }

        resp = requests.get(self.GET_MESSAGE_URL, headers=self.HEADERS, cookies=self.COOKIES, params=params)
        message_data = resp.json()["data"]["session_list"]
        talker = []

        for message in message_data:
            if message["unread_count"] > 0:
                last_msg = message["last_msg"]
                log.info("信息初始内容为:" + last_msg["content"])
                content_json = eval(last_msg["content"])
                id_ = None
                if content_json.get("bvid") is not None:
                    id_ = content_json["bvid"]
                if content_json.get("id") is not None:
                    id_ = str(content_json["id"])
                if content_json.get("content") is not None:
                    id_ = self.find_bvid(content_json["content"])

                talker_id = message["talker_id"]
                content = id_
                msg_seqno = last_msg["msg_seqno"]
                talker_info = Talker(talker_id, content, msg_seqno)
                talker.append(talker_info)

        return talker

    def ack_message(self, talker_id: str, ack_seqno: str) -> str:
        """
        确认未读的消息
        :param talker_id: id
        :param ack_seqno: 消息的确认参数
        :return: 成功则返回成功的消息，失败则抛出异常
        """
        data = {
            'talker_id': talker_id,
            'session_type': '1',
            'ack_seqno': ack_seqno,
            'build': '0',
            'mobi_app': 'web',
            'csrf_token': self.bili_jct,
            'csrf': self.bili_jct,
        }
        headers = self.HEADERS
        resp = requests.post(self.ACK_MESSAGE_URL, headers=headers, cookies=self.COOKIES, data=data)
        resp_ack_message = resp.json()

        if resp_ack_message["code"] == 0:
            return "信息确认成功"

        raise Exception("信息确认失败")

    def send_message(self, talker_id: str, content: str) -> str:
        """
        发送私信
        :param talker_id: 接收者id
        :param content: 信息内容
        :return: 成功则返回成功的消息，失败则抛出异常
        """
        send_content = {"content": content}
        data = {
            'msg[sender_uid]': self.uid,
            'msg[receiver_id]': talker_id,
            'msg[receiver_type]': '1',
            'msg[msg_type]': '1',
            'msg[msg_status]': '0',
            'msg[content]': json.dumps(send_content),
            'msg[timestamp]': str(int(time.time())),
            'msg[new_face_version]': '0',
            'msg[dev_id]': self._generate_deviceid(),
            'from_firework': '0',
            'build': '0',
            'mobi_app': 'web',
            'csrf_token': self.bili_jct,
            'csrf': self.bili_jct,
        }
        resp = requests.post(self.SEND_MESSAGE_URL, headers=self.HEADERS, cookies=self.COOKIES, data=data)
        send_message = resp.json()
        send_message_code = send_message["code"]
        if send_message_code == 0:
            return "发送成功"

        raise Exception("消息发送失败")

    def get_video_info(self, id_: str, page: int = 1) -> BilibiliVideoInfo:
        """
        获取视频的信息
        :param id_: aid 或者 bvid
        :param page: 集数
        :return: 视频信息
        """
        if "BV" in id_:
            param = {
                "bvid": id_
            }
        else:
            param = {
                "aid": id_
            }

        resp = requests.get(self.GET_VIDEO_INFO, headers=self.HEADERS, params=param)
        info_resp = resp.json()
        if info_resp["code"] == 0:
            data = info_resp["data"]
            pages = data["pages"]
            cid = None
            for p in pages:
                if p["page"] == page:
                    cid = p["cid"]

            if cid is None:
                raise Exception("没有找到对应的cid")

            video_info = BilibiliVideoInfo(
                id_=data["bvid"],
                cid=cid,
                title=data["title"],
                desc=data["desc"],
                subtitle=self._get_subtitle(data["bvid"], cid),
            )

            return video_info

    @staticmethod
    def find_bvid(content: str) -> Union[str, None]:
        """
        查找bvid
        :param content: 内容
        :return: bvid
        """
        pattern = r"(BV[A-Za-z0-9]+)"
        match = re.search(pattern, content)
        if match:
            bvid = match.group(1)
            return bvid
        else:
            return None

    def _get_subtitle(self, bv_id: str, cid: int) -> str:
        """
        获取视频字幕
        :param bv_id: 视频bv号
        :param cid: 视频cid号
        :return: 字幕信息
        """
        subtitle_url = self._get_subtitle_url(bv_id, cid)
        resp = requests.get(subtitle_url, headers=self.HEADERS, cookies=self.COOKIES)
        subtitle_data = resp.json()["body"]
        subtitles = ""
        for subtitle in subtitle_data:
            subtitles += f"{subtitle['content']}\n"
        return subtitles

    def _get_subtitle_url(self, bv_id: str, cid: int) -> str:
        """
        获取视频字幕的URL地址
        :param bv_id: 视频bv号
        :param cid: 视频cid号
        :return: 视频字幕URL
        """
        params = {
            "bvid": bv_id,
            "cid": cid,
        }
        resp = requests.get(self.GET_SUBTITLE_URL, headers=self.HEADERS, cookies=self.COOKIES, params=params)
        subtitle_resp = resp.json()

        if subtitle_resp["code"] == 0:
            subtitle_data = subtitle_resp["data"]
            subtitle = subtitle_data["subtitle"]["subtitles"]
            if len(subtitle) != 0:
                subtitle_url = subtitle[0]["subtitle_url"]
                return "https:" + subtitle_url

        raise Exception("此视频无字幕")

    @staticmethod
    def _generate_deviceid() -> str:
        """
        发送私信的msg[dev_id]逆向算法
        :return: dev_id
        """
        replace_map = {
            'x': lambda: format(random.randint(0, 15), 'x').upper(),
            'y': lambda: format((random.randint(0, 15) & 0x3) | 0x8, 'x').upper()
        }

        deviceid = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx"
        deviceid = ''.join(replace_map[c]() if c in replace_map else c for c in deviceid)

        return deviceid
