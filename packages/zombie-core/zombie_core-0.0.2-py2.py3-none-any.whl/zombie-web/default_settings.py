#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Time : 2020/6/29 14:17
# @Author : Yao
import logging
import os

DEFAULT_LOG_LEVEL = logging.INFO  # 默认等级
DEFAULT_LOG_FMT = '[%(asctime)s] %(levelname)s %(filename)s[line:%(lineno)d]: %(message)s'  # 默认日志格式
DEFAULT_LOG_DATE_FMT = '%Y-%m-%d %H:%M:%S'  # 默认时间格式
# DEFAULT_LOG_DIR = './'  # 默认日志文件名称
# DEFAULT_LOG_FILENAME = 'log.log'  # 默认日志文件名称
PATH_ROOT = f".{os.sep}logs" + os.sep
DEFAULT_LOG_FILENAME = PATH_ROOT + 'log.log'  # 默认日志文件名称
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;"
              "q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
}

# 创建一个连接池来进行使用
# 最大超时时间
ALIVE_MAX_TIMEOUT = 20

# 没任务了 停多久！
TIME_TO_WAIT = 3

# 2轮测试、 7天一轮/一轮7个周期，1天是1个周期  1个周期里抓24次，每隔1小时抓一次

# 最多抓2轮
TOTAL_TURN = 2
# TOTAL_TURN = 2

dev = 0
if dev:
    # 一轮几个周期
    # CIRCLE = 7
    CIRCLE_NUM_ONE_TURN = 7

    # 一周期抓多久
    TOTAL_TS_ONE_CIRCLE = 86400

    # 一轮抓多久
    TOTAL_TS_ONE_TURN = CIRCLE_NUM_ONE_TURN * TOTAL_TS_ONE_CIRCLE

    # 一周期内，每多久检测一次，1小时
    CRAWL_EVERY_TS = 60 * 60

    # 核对1个周期，抓几次
    CHECK_COUNT_ONE_CIRCLE = TOTAL_TS_ONE_CIRCLE // CRAWL_EVERY_TS

    # =>一个周期抓几次
    CRAWL_COUNT_ONE_CIRCLE = int(TOTAL_TS_ONE_CIRCLE / CRAWL_EVERY_TS)

    # 两次间隔多少ts，30天
    INTERVAL_TS = 30 * 86400

    # 所有时间
    TOTAL_TS = int(CIRCLE_NUM_ONE_TURN * TOTAL_TS_ONE_CIRCLE + INTERVAL_TS)

    title = f"本次任务最低需要: {TOTAL_TS // 1}秒。" \
            f"可用性检测 {CHECK_COUNT_ONE_CIRCLE} 次，共{TOTAL_TS_ONE_TURN // 1}秒。" \
            f"两轮之间间隔 {INTERVAL_TS // 1} 秒。"

# else:
#     # 一轮几个周期
#     # CIRCLE = 7
#     CIRCLE_NUM_ONE_TURN = 3
#
#     # 一周期抓多久
#     # 20s是一轮
#     TOTAL_TS_ONE_CIRCLE = 6
#
#     # 一轮抓多久
#     TOTAL_TS_ONE_TURN = CIRCLE_NUM_ONE_TURN * TOTAL_TS_ONE_CIRCLE
#
#     # 一周期内，每多久检测一次，1小时
#     CRAWL_EVERY_TS = 2
#
#     # 核对1个周期，抓几次
#     CHECK_COUNT_ONE_CIRCLE = TOTAL_TS_ONE_CIRCLE // CRAWL_EVERY_TS
#
#     # =>一个周期抓几次
#     CRAWL_COUNT_ONE_CIRCLE = int(TOTAL_TS_ONE_CIRCLE / CRAWL_EVERY_TS)
#
#     # 两次间隔多少ts，30天
#     INTERVAL_TS = 4
#
#     # 所有时间
#     TOTAL_TS = int(CIRCLE_NUM_ONE_TURN * TOTAL_TS_ONE_CIRCLE + INTERVAL_TS)
#
#     # title = f"本次任务最低需要: {TOTAL_TS // 1}分钟。" \
#     #         f"可用性检测 {CHECK_COUNT_ONE_CIRCLE} 次，共{TOTAL_TS_ONE_TURN // 1}分钟。" \
#     #         f"两轮之间间隔 {INTERVAL_TS // 1} 分钟。"
#     title = f"本次任务最低需要: {TOTAL_TS // 1}秒。" \
#             f"可用性检测 {CHECK_COUNT_ONE_CIRCLE} 次，共{TOTAL_TS_ONE_TURN // 1}秒。" \
#             f"两轮之间间隔 {INTERVAL_TS // 1} 秒。"
else:
    # 一轮几个周期
    # CIRCLE = 7
    CIRCLE_NUM_ONE_TURN = 10

    # 一周期抓多久
    # 20s是一轮
    TOTAL_TS_ONE_CIRCLE = 60

    # 一轮抓多久
    TOTAL_TS_ONE_TURN = CIRCLE_NUM_ONE_TURN * TOTAL_TS_ONE_CIRCLE

    # 一周期内，每多久检测一次，1小时
    CRAWL_EVERY_TS = 30

    # 核对1个周期，抓几次
    CHECK_COUNT_ONE_CIRCLE = TOTAL_TS_ONE_CIRCLE // CRAWL_EVERY_TS

    # =>一个周期抓几次
    CRAWL_COUNT_ONE_CIRCLE = int(TOTAL_TS_ONE_CIRCLE / CRAWL_EVERY_TS)

    # 两次间隔多少ts，30天
    INTERVAL_TS = 1

# 确定结果需要多久

msg = f"一个任务最多需要: {TOTAL_TS // 60}分. " \
      f"共抓 {TOTAL_TURN} 轮 ,  " \
      f"第一轮{CIRCLE_NUM_ONE_TURN}个周期;" \
      f"每周期抓 {CHECK_COUNT_ONE_CIRCLE}/{CRAWL_COUNT_ONE_CIRCLE} 次, " \
      f"抓 {TOTAL_TS_ONE_TURN} s, " \
      f"每次抓取间隔{CRAWL_EVERY_TS}s. " \
      f"共 {TOTAL_TS_ONE_CIRCLE}s ;\t " \
      f"两轮之间间隔 {INTERVAL_TS} s"
# print(msg)


# # 每次抓取间隔多久
# CRAWL_EVERY_TS = None
# # 两次间隔多久
# INTERVAL_TS = None
# # 一轮总共多久
# TOTAL_TS_ONE_TURN = None
# # 一周期抓多久
# TOTAL_TS_ONE_CIRCLE = None
# # 一轮几天（周期）
# CIRCLE_NUM_ONE_TURN = None
