# -*- coding:utf-8 -*-
# @FileName  : tools_llm.py
# @Time      : 2023/8/22
# @Author    : LaiJiahao
# @Desc      : AI工具类


# from utils.ai_message import CustomLLM
#
#
# class ToolsLLM:
#
#     def __init__(self):
#         self.llm = CustomLLM()
#
#     def summary(self, title: str, subtitle: str):
#         prompt = f""" "视频标题: {title}" 视频字幕: {subtitle} """
#         result = self.llm.get_completion(system=summary_system_prompt, prompt=prompt)
#         return result
