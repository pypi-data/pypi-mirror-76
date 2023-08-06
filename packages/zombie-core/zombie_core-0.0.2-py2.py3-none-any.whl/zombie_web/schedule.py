# -*- coding: utf-8 -*-
# 调度器，将MySQL数据存入到redis待抓队列中，不可以多启
# 调度器，将csv数据存入到待抓文件中
import csv
import datetime
import json
import time

from XX.Encrypt.EncryptHelper import Encrypt as Enc
from XX.File.FileHelper import FileHelper as Fh
from apscheduler.schedulers.background import BackgroundScheduler
from logzero import logger

Fh.add_python_path(".")
Fh.add_python_path("../")
from check.default_settings import *


def init_redis(redis_key):
    return Fh.remove_file(f"./logs/hset/{redis_key}_data")


# 添加可用检测任务
def add_iu(d, redis_key):
    js = d if isinstance(d, str) else json.dumps(d, ensure_ascii=False)
    Fh.save_file(f"./logs/scheduler_urls/{redis_key}_{int(time.time())}_{Enc.md5(js)}.txt", js)
    logger.info(f" == Add task url 2 {redis_key} is over. content is {js}")


# 添加第二轮的下载调度
def add_iu_2downloader(d):
    scheduler_one_week = BackgroundScheduler()
    scheduler_one_week.add_job(
        add_iu,
        'date',
        (d, "l_2downloader"),
        run_date=datetime.datetime.now() + datetime.timedelta(seconds=INTERVAL_TS),
    )
    scheduler_one_week.start()


# 按周添加调度器，一天添加 CRAWL_COUNT_ONE_CIRCLE 次，添加 天，
# 如果某天可达，则不再判断，30天后会再调度一次
def add_iu_one_week(d, times=1, redis_key="l_2available", INTERVAL_TS=30 * 86400):
    scheduler_one_week = BackgroundScheduler()
    logger.info(f"Add scheduler  {times} <= {TOTAL_TURN} ")

    scheduler_one_week.add_job(
        add_iu,
        'interval',
        (d, redis_key),
        seconds=CRAWL_EVERY_TS,
        start_date=datetime.datetime.now() + datetime.timedelta(seconds=(times - 1) * INTERVAL_TS + 1),
        # 一轮结束的时间：就是当前时间加上一轮所需要的时间再加第几波的时间
        # 比如第二次确定的结束时间，就是当前时间+30天
        end_date=datetime.datetime.now() + datetime.timedelta(
            seconds=(times - 1) * INTERVAL_TS + TOTAL_TS_ONE_TURN - 1)
    )
    scheduler_one_week.start()


# 调度URL,把所有未确认的URL添加到存活检测队列中
def schedule_url():
    # 读取csv获取URL
    while 1:
        try:
            start = open(PATH_ROOT + "toschedu.log", encoding="utf-8").read().strip()
        except:
            start = 0

        if start:
            fieldnames = (
                "url", "date", "progress", "reachable_score", "is_reachable", "updated_score",
                "is_zombie")  # 自己添加的表头，在json里作为key

            with open('./result.csv', 'r', encoding='UTF-8') as csv_file:
                if Fh.is_file_exit("./reading.lock"):
                    time.sleep(0.1)
                    continue
                else:
                    open("./reading.lock", "w", encoding="utf-8").write("1")
                    # logger.info("=== schedule lock file   ==== ")
                    reader = csv.DictReader(csv_file, fieldnames)  # 转为dict格式
                    urls = [row['url'] for row in reader if row['url'].startswith("http")]
                    if urls:
                        for url in urls:
                            # 添加第一周的初始URL
                            add_iu_one_week(url, 1, "l_2available", INTERVAL_TS)
                    else:
                        if int(time.time()) % 100 == 0:
                            logger.info("== Wait for more job!==")
                        # else:
                            # print("=", end="", flush=True)
                        time.sleep(TIME_TO_WAIT)
                    open(PATH_ROOT + "toschedu.log", "w", encoding="utf-8").write("")
                    Fh.remove_file("./reading.lock")
                    time.sleep(TOTAL_TS + 10)
        else:
            time.sleep(1)
            continue


if __name__ == '__main__':
    schedule_url()
