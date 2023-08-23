# -*- coding:utf-8 -*-
# @FileName  : log.py
# @Time      : 2023/8/22
# @Author    : LaiJiahao
# @Desc      : None

import logging

# 创建一个全局日志记录器
log = logging.getLogger(__name__)

# 设置日志记录级别为DEBUG，这样能够捕捉更详细的日志信息
log.setLevel(logging.DEBUG)

# 创建一个文件处理器，将日志写入到文件中
file_handler = logging.FileHandler("app.log")

# 创建一个格式化器，设置日志记录的格式
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# 将格式化器添加到文件处理器
file_handler.setFormatter(formatter)

# 将文件处理器添加到日志记录器
log.addHandler(file_handler)

# 创建一个控制台处理器，将日志打印到控制台
console_handler = logging.StreamHandler()

# 将格式化器添加到控制台处理器
console_handler.setFormatter(formatter)

# 将控制台处理器添加到日志记录器
log.addHandler(console_handler)