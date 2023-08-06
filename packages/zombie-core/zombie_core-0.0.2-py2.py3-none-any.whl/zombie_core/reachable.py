# -*- coding: utf-8 -*-
# 核对url是否可达。并计算分数，更新 is_reachable,可以多启，可以重复启
import csv
import json
import time
import traceback

import pandas as pd
import requests
from XX.Date.DatetimeHelper import get_now_time
from XX.Encrypt.EncryptHelper import Encrypt as Enc
from XX.File.FileHelper import FileHelper as Fh
from logzero import logger
from user_agent import generate_user_agent

Fh.add_python_path(".")
Fh.add_python_path("../")
from check.utils import calc_progress
from check.default_settings import *
from check.parse import parse
from check.pipeline import pipeline
from check.schedule import add_iu_2downloader, init_redis

headers = {
    "User-Agent": generate_user_agent(),
}
max_reachable_score = {}


def add_day(data_day):
    if max_reachable_score.get(data_day['url'] + "_task_id"):
        max_reachable_score[data_day['url'] + "_task_id"].append(data_day)
    else:
        max_reachable_score[data_day['url'] + "_task_id"] = [data_day]
    return len(max_reachable_score[data_day['url'] + "_task_id"])


def get_max_reachable_score(task_id, url):
    max_score = 0
    for i in max_reachable_score.get(url + "_" + task_id, []):
        max_score = max(max_score, i["reachable_score"])
    return max_score


# 计算可用分数，24次请求计算一次
def calculation_score(task_id, url, redis_key, res_num, success_num, timeout_num, fail_num, now_time, score=0,
                      day=0, CRAWL_COUNT_ONE_CIRCLE=24, TOTAL_TS=86400 * 37) -> int:
    try:
        response = requests.get(url, headers=headers, timeout=30)

        if response and response.status_code == 200 and response.text:
            # 直接入ES库！！
            if not Fh.is_file_exit(f"{PATH_ROOT}added_es/k_{redis_key}"):
                item = parse(response, task_id, url)
                _ = pipeline(response, item)
                if _:
                    logger.info(f" ===== Reachable 2  es res is  OK = {_}")
                    open(f"{PATH_ROOT}added_es/k_{redis_key}", "w", encoding="utf-8").write("1")
                else:
                    logger.info(f" ===== Reachable 2  es res is No ====  {_}")

        status = response.status_code
        res_time = response.elapsed.total_seconds()
        if status < 400:
            if res_time <= 15:
                success_num += 1
            else:
                timeout_num += 1
        elif status >= 400:
            fail_num += 1
    except Exception as e:
        traceback.print_exc()
        fail_num += 1

    res_num += 1
    # 最后一次计算得分
    # logger.info(res_num)

    if res_num >= CRAWL_COUNT_ONE_CIRCLE:
        if fail_num > 3:
            score = 100
        elif timeout_num > 8:
            score = 100
        else:
            score = fail_num * 50 + timeout_num * 50
            # logger.info(fail_num)

        logger.debug(f"score是：：：{score}  fail_num ： {fail_num}")

        # 计算完这个就没用了！
        Fh.remove_file(f"{PATH_ROOT}hset{os.sep}{redis_key}_data.json")
        return score

    # 更新redis数据库
    res_data = {"res_num": res_num, "success_num": success_num, "timeout_num": timeout_num,
                "failed_num": fail_num, "req_time": now_time, "url": url,
                "score": score, "day": day}
    open(f"{PATH_ROOT}hset{os.sep}{redis_key}_data.json", "w", encoding="utf-8").write(
        json.dumps(res_data, ensure_ascii=False))
    return -1


# 计算链接是否可用,某一次的
def available_score(url, redis_key, task_id, day, CRAWL_COUNT_ONE_CIRCLE=24, TOTAL_TS=86400 * 37) -> int:
    try:
        now_time = get_now_time()
        try:
            dict_data = json.load(open(f"{PATH_ROOT}hset{os.sep}{redis_key}_data.json", encoding="utf-8"))
        except Exception as e:
            dict_data = {}
        res_num = int(dict_data.get("res_num", 0))
        success_num = int(dict_data.get("success_num", 0))
        timeout_num = int(dict_data.get("timeout_num", 0))
        available_num = int(dict_data.get("failed_num", 0))
        score = int(dict_data.get("score", 0))
        return calculation_score(task_id, url, redis_key, res_num, success_num, timeout_num, available_num, now_time,
                                 score, day, CRAWL_COUNT_ONE_CIRCLE, TOTAL_TS)
    except Exception as e:
        traceback.print_exc()
        return -1


def add_url_result(data) -> int:
    while 1:
        if Fh.is_file_exit("./reading.lock"):
            time.sleep(0.1)
            continue
        with open('./result.csv', 'r', encoding='UTF-8') as csv_file:
            open("./reading.lock", "w", encoding="utf-8").write("1")
            fieldnames = (
                "url", "date", "progress", "reachable_score", "is_reachable", "updated_score",
                "is_zombie")  # 自己添加的表头，在json里作为key
            reader = csv.DictReader(csv_file, fieldnames)  # 转为dict格式
            r_data = []
            num = 0
            for row in reader:
                num += 1
                if num > 1:
                    if row['url'] == data["url"]:
                        row['is_reachable'] = data.get("is_reachable")
                        row['is_zombie'] = data.get("is_zombie")
                        row["reachable_score"] = data.get("reachable_score")
                        print(row)
                    r_data.append(row)
            df = pd.DataFrame(r_data)
            df.to_csv("./result.csv", index=None)
            Fh.remove_file("./reading.lock")
            # logger.info(f" == 添加到csv的df长度是：{len(r_data)}")
            break
    return 1


def schedule():
    while 1:
        time.sleep(1)
        for fp, fn in Fh.get_file_list(f"{PATH_ROOT}scheduler_urls"):
            if fn.find("l_2available") < 0:
                continue
            url = open(fp + os.sep + fn, encoding="utf-8").read().strip()
            res = Fh.remove_file(fp + os.sep + fn)

            hash_code = Enc.md5(f"""{url}_task_id""")
            try:
                circle = int(open(f"{PATH_ROOT}circle/{hash_code}", "r", encoding="utf-8").read()) + 1
            except:
                circle = 1
            open(f"{PATH_ROOT}circle/{hash_code}", "w", encoding="utf-8").write(str(circle))
            day = (circle - 1) // CHECK_COUNT_ONE_CIRCLE + 1

            # 计算这次的可达分数
            available = available_score(
                url,
                hash_code, "task_id", day,
                CRAWL_COUNT_ONE_CIRCLE=CRAWL_COUNT_ONE_CIRCLE,
                TOTAL_TS=TOTAL_TS)
            available = 100 if available >= 100 else available
            # LOG_STATUS
            ts = int(time.time())

            if 0 <= available < 100:
                init_redis(Enc.md5(f"""{url}_task_id"""))
                data_day = {
                    "task_id": 'task_id',
                    "url": url,
                    "day": day,
                    "progress": calc_progress(day / 2, 7),
                    "reachable_score": available,
                    "update_ts": ts,
                }
                res_day = add_day(data_day)
                logger.info(f"Add day score res {res_day}")

            # 某一个周期 不可用,僵尸网站，is_reachable置为0
            elif available >= 100:
                init_redis(Enc.md5(f"""{url}_{'task_id'}"""))

                data_day = {
                    "task_id": "task_id",
                    "url": url,
                    "day": day,
                    "progress": calc_progress(day, 37),
                    "reachable_score": available,
                    "update_ts": ts,
                }
                res_day = add_day(data_day)
                logger.info(f"Add day score res {res_day}")

            # 还无法判断，继续
            else:
                # 更新数据库
                pass

            # res_add = sh.add_log(data_log)
            # logger.info(f"Log added OK! res :{res_add}, task_id {url}")

            # 最后一次
            if int(circle) == int(CIRCLE_NUM_ONE_TURN * CHECK_COUNT_ONE_CIRCLE):
                # 加入待下载队列
                max_reachable = get_max_reachable_score('task_id', url)

                data_add = {
                    "task_id": "task_id",
                    "url": url,
                    "is_reachable": "否",
                    "progress": calc_progress(7, 37),
                    "reachable_score": max_reachable,
                    "update_ts": ts,
                }

                # 僵尸网站
                if max_reachable >= 100:
                    data_add['is_reachable'] = "否"
                    data_add['is_zombie'] = "是"
                    res_update = add_url_result(data_add)
                    _ = f" ==== 【All Done 1,Reachable: {max_reachable}】 结果是：{res_update}, data : {data_add}"

                # 非僵尸网站
                elif 0 <= max_reachable < 100:
                    data_add['is_reachable'] = "是"
                    res_update = add_url_result(data_add)
                    _ = f" ==== 【All Done 2,Reachable:{max_reachable}】 结果是：{res_update}, data : {data_add}"

                    # 下轮抓取调度
                    add_iu_2downloader(url)
                    # logger.info(f" ==== 开始下轮下载调度 {url}==== ")
                else:
                    _ = "XXX" * 20
                logger.info(_)
            else:
                logger.info(f"Now circle is {circle} , >>> {CIRCLE_NUM_ONE_TURN * CHECK_COUNT_ONE_CIRCLE}")


if __name__ == '__main__':
    schedule()
