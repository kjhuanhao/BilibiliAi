# -*- coding:utf-8 -*-
# @FileName  : listener.py
# @Time      : 2023/8/22
# @Author    : LaiJiahao
# @Desc      : 监听信息

import time
import toml

from utils.bilibili import Bilibili
from utils.ai_message import CustomLLM
from common.log import log


class ListenMessage:

    @staticmethod
    def start():
        b = Bilibili()
        llm = CustomLLM()
        config = toml.load("config.toml")
        user_message = config["robot"]["user_message"]
        current_message = None
        while True:
            try:
                count_unread = b.get_unread()
                if count_unread == 0:
                    continue
                else:
                    log.info(f"有{count_unread}条未读消息，开始处理")
                    message_list = b.get_message()
                    for message in message_list:
                        current_message = message
                        log.info(f"消息内容为：{message.content}，用户id为{message.talker_id}")

                        ack_message = b.ack_message(current_message.talker_id, current_message.ack_seqno)
                        log.info(f"已确认消息：{ack_message}")

                        if message.content is None:
                            send_message = b.send_message(message.talker_id, "您发送的视频信息格式不正确，未寻找到视频的BV号，请重新发送")
                            log.info(f"发送AI消息完成：{send_message}")
                            break

                        b.send_message(message.talker_id, user_message)
                        log.info(f"向用户发送提示成功")

                        log.info(f"等待ai返回信息")
                        to_message = llm.summary(b.get_video_info(message.content))
                        print(to_message)
                        log.info("ai返回信息成功")

                        send_message = b.send_message(message.talker_id, to_message)
                        log.info(f"发送AI消息完成：{send_message}")

                time.sleep(20)
            except Exception as e:
                log.error(f"监听消息出现异常,向用户发送异常消息：{e}")
                if 'current_message' in locals():
                    b.send_message(current_message.talker_id, f"出现异常，请联系管理员以下是异常信息: {e}")
                    b.ack_message(current_message.talker_id, current_message.ack_seqno)
                    continue
                else:
                    log.info("current_message 未定义")
                    continue

    print("程序启动成功")
