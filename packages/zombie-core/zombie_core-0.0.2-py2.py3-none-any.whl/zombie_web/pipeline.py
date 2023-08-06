# -*- coding: utf-8 -*-
# 入库
import copy
import json
import os
import time

from XX.Encrypt.EncryptHelper import Encrypt as Enc
from XX.File.FileHelper import FileHelper as Fh

Fh.add_python_path(".")
Fh.add_python_path("../")
# item数据处理
from check.default_settings import PATH_ROOT


def pipeline(response, item, es=None) -> dict:
    if item:
        data_ = copy.deepcopy(item)
        if data_.get("exception_info"):
            data_["exception_info"] = json.dumps(data_["exception_info"], ensure_ascii=False)
        hash_code = Enc.md5(f"""{item['url']}_{item['task_id']}""")
        fn = f"{PATH_ROOT}pipeline{os.sep}{hash_code}_{int(time.time())}.pipeline"
        res = open(fn, "w", encoding="utf-8").write(json.dumps(data_, ensure_ascii=False))
        return res
    else:
        return {}
