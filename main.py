# -*- coding:utf-8 -*-
# @FileName  : main.py
# @Time      : 2023/8/21
# @Author    : LaiJiahao
# @Desc      : 启动程序

from service.listener import ListenMessage
from apscheduler.schedulers.blocking import BlockingScheduler

if __name__ == "__main__":
    schedule = BlockingScheduler()
    schedule.add_job(ListenMessage.start, 'interval', seconds=40)
    schedule.start()
