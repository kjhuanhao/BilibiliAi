# -*- coding:utf-8 -*-
# @FileName  : handler.py
# @Time      : 2023/8/22
# @Author    : LaiJiahao
# @Desc      : None

import functools
import time


def retry_on_exception(max_retries):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    print(f"Exception caught: {e}")
                    retries += 1
                    time.sleep(60)
            raise Exception(f"Failed to execute {func.__name__} after {max_retries} retries")

        return wrapper

    return decorator
