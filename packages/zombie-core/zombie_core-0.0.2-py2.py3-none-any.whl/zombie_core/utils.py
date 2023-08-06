# -*- coding: utf-8 -*-
import json
import os

import pandas as pd
from XX.File.FileHelper import FileHelper as Fh

Fh.add_python_path(".")
Fh.add_python_path("../")

from check.default_settings import PATH_ROOT


def get_urls():
    csv_data = pd.read_csv("./result.csv", usecols=['url'])
    return [d[0] for d in csv_data.values]


def get_by_url_hash(hash_code, count=1):
    r_data = []
    pp = os.getcwd() + PATH_ROOT.strip(".") + "pipeline"
    for fn in os.listdir(pp):
        if fn.find(hash_code) >= 0:
            data = {
                "_source": json.load(open(pp + os.sep + fn, encoding="utf-8"))
            }
            r_data.append(data)
    if r_data and len(r_data) >= count:
        return r_data[-count:]
    else:
        return []


def calc_progress(num1, num2):
    num = num1 / num2
    num = 0.999 if num >= 1 else num
    return "{:.1%}".format(num) if num != 1 else "100%"

