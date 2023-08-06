# -*- coding: utf-8 -*-
# 下载器，可以多启
import os
import time
from copy import deepcopy

import grequests
from XX.File.FileHelper import FileHelper as Fh
from gevent import monkey
from logzero import logger
from user_agent import generate_user_agent

Fh.add_python_path(".")
Fh.add_python_path("../")
from check.default_settings import HEADERS, TIME_TO_WAIT
from check.parse import parse
from check.pipeline import pipeline

monkey.patch_all()
pxy = None


def exception_handler(request, exception):
    logger.info("Request failed  " + request.url)


# 下载
def download(urls):
    rs = list()
    for url in urls:
        # 传输副本！！
        headers = deepcopy(HEADERS)
        headers["Task-Id"] = f"""task_id"""
        headers["User-Agent"] = generate_user_agent()
        rs.append(grequests.get(url, headers=headers, proxies=pxy, timeout=20))
    return grequests.map(rs, exception_handler=exception_handler)


# 下载器
def downloader(urls=None):
    responses = download(urls)
    num = 0
    for response in responses:
        item = parse(response, "task_id", urls[num])
        num += 1
        res = pipeline(response, item)
        logger.info(f"==添加response到es结果是：{res}")


# 下载调度器,从redis中拿URL然后下载
def schedule():
    while 1:
        url_list = []
        for fp, fn in Fh.get_file_list("./logs/scheduler_urls/"):
            if fn.find("l_2downloader") >= 0:
                url_info = open(fp + fn, encoding="utf-8").read()
                if url_info:
                    url_list.append(url_info.strip())
                res = Fh.remove_file(fp + os.sep + fn)
        if url_list:
            logger.info(f"===============去下载{url_list}！===============")
            downloader(url_list)
        else:
            if int(time.time()) % 100 == 0:
                logger.info("== Wait for more job! ==")
            # else:
            #     print("=", end="", flush=True)
            time.sleep(TIME_TO_WAIT)


if __name__ == '__main__':
    schedule()
