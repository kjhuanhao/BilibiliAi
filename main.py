# -*- coding:utf-8 -*-
# @FileName  : main.py
# @Time      : 2023/8/21
# @Author    : LaiJiahao
# @Desc      : 启动程序

from service.listener import ListenMessage

if __name__ == "__main__":
    ListenMessage.start()

