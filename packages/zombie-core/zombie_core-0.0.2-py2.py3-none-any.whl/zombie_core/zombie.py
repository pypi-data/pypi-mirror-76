# -*- coding: utf-8 -*-
# 核对是否是僵尸网站 ： # 2.更新指数
import csv
import time

import pandas as pd
from XX.Encrypt.EncryptHelper import Encrypt as Enc
from XX.File.FileHelper import FileHelper as Fh
from logzero import logger

Fh.add_python_path("./")
Fh.add_python_path("../")
from check.reachable import get_max_reachable_score
from check.utils import get_by_url_hash


# 计算更新指数,两轮抓完才能确定
def get_update_score(task_id, url, doc_type="logs", TOTAL_TURN=2):
    hash_code = Enc.md5(f"""{url}_{task_id}""")
    history_data = get_by_url_hash(hash_code, 2)
    if history_data and len(history_data) >= TOTAL_TURN:
        similarity = history_data[1]['_source']['similarity'] if \
            int(history_data[1]['_source']['ts']) > history_data[0]['_source']['ts'] else \
            history_data[0]['_source']['ts']
        if similarity >= 90:
            score = 100
        elif similarity >= 70:
            score = 50
        else:
            score = 0
    else:
        score = -1
    return score


# 从MySQL中拿没有确定的数据，去es中确认
# 从csv中拿没有确定的数据，去es中确认
def scheduler():
    fieldnames = ("url", "date", "progress", "reachable_score", "is_reachable", "updated_score", "is_zombie")
    while 1:
        all_done = True
        with open('./result.csv', 'r', encoding='UTF-8') as csv_file:
            if Fh.is_file_exit("./reading.lock"):
                time.sleep(0.1)
                continue
            open("./reading.lock", "w", encoding="utf-8").write("1")
            reader = csv.DictReader(csv_file, fieldnames)  # 转为dict格式
            num = 0
            r_data = []
            for row in reader:
                num += 1
                if num > 1:
                    if str(row['is_zombie']) == "nan" or str(row['is_zombie']) == "":
                        all_done = False
                        updated = get_update_score("task_id", row['url'])
                        reachable_score = get_max_reachable_score('task_id', row['url'])
                        # 没下完,或者不可用！
                        if updated == -1:
                            time.sleep(0.5)
                        # 可达分数
                        elif reachable_score is None:
                            time.sleep(0.5)
                        else:
                            # 综合判断
                            is_zombie = (
                                0 if 0 <= updated + reachable_score < 100 else 1) if reachable_score >= 0 else 1
                            row['is_zombie'] = "是" if str(is_zombie) == "1" else "否"
                            row['updated_score'] = str(updated)
                            row['date'] = str(int(time.time()))
                    if row["url"].startswith("http"):
                        r_data.append(row)
            df = pd.DataFrame(r_data)
            res = df.to_csv("./result.csv", index=None)
            Fh.remove_file("./reading.lock")
            if int(time.time()) % 10 == 0:
                logger.info(f" {res} All done: {all_done} , 长度是：{len(r_data)}")
        time.sleep(3)


if __name__ == '__main__':
    scheduler()
