# -*- coding: utf-8 -*-
import json
import time
from typing import Union

import jieba
from XX.Encrypt.EncryptHelper import Encrypt as Enc
from XX.File.FileHelper import FileHelper as Fh
from lxml import etree
from lxml.html.clean import Cleaner


Fh.add_python_path(".")
Fh.add_python_path("../")

try:
    from .default_settings import *
    from .utils import get_by_url_hash
except:
    from default_settings import *
    from utils import get_by_url_hash

cleaner = Cleaner()
cleaner.javascript = True
cleaner.style = True

result_parse = Union[None, dict]


# 相似度计算
def similarity(html1, html2):
    if not (html1 and html2):
        return 100
    """
    # 计算两个HTML的相似度
    :param html1: 第一个html
    :param html2: 第二个HTML
    :return: 相似度的百分比，默认乘以100，比如80%就返回80
    """
    # 将html转换为list比较，计算相似度，并返回
    html1_project = jieba.cut(html1)  # 默认精准模式
    html2_project = jieba.cut(html2)

    html1_project_list = list(html1_project)  # 如果需要去重；就改为list
    html2_project_list = list(html2_project)
    temp = 0
    for i in html2_project_list:
        if i in html1_project_list:
            temp = temp + 1
    denominator = len(html2_project_list) + len(html1_project_list) - temp  # 并集
    similarity_data = float(temp / denominator)  # 交集
    similarity_data = int("%.f" % (similarity_data * 100))

    if similarity_data > 100:
        similarity_data = 200 - similarity_data
    else:
        similarity_data = similarity_data
    return similarity_data


def parse(response, task_id, url) -> result_parse:
    # 解析
    hash_code = Enc.md5(f"""{url}_{task_id}""")
    item = dict()
    item['url'] = url
    item['task_id'] = task_id
    item['url_hash'] = hash_code
    item['ts'] = int(time.time())
    html_old = get_by_url_hash(hash_code, 1)
    if html_old:
        html1 = open(html_old[0]["_source"].get("html_path", ""), encoding="utf-8").read()
        item['similarity'] = similarity(html1, response.text)
    else:
        item['similarity'] = 100
    if response:
        if response.text:
            item['request_header'] = json.dumps(dict(response.request.headers), ensure_ascii=False)
            item['status_code'] = response.status_code
            item['wait_time'] = response.elapsed.microseconds / 1000 / 1000
            item['response_header'] = json.dumps(dict(response.headers), ensure_ascii=False)
            item['html'] = response.text[:20000]
            item['html_path'] = PATH_ROOT + "cache" + os.sep + Fh.get_md5_name(
                f"""{response.url}_{task_id}""") + f"_{item['ts']}.html"
            # 保存文件
            Fh.save_file(item['html_path'], response.text)
            item['encoding'] = response.encoding
            item['mime'] = "html"
            item['bsize'] = len(response.text)
            doc = etree.HTML(response.text)
            try:
                doc.xpath("//title/text()")
                item['title'] = doc.xpath("string(//title)")
            except:
                pass
            html = cleaner.clean_html(response.text)
            doc = etree.HTML(html)
            item['content'] = doc.xpath("string(.)")[:30000]
        else:
            item['exception_info'] = " no content in response"
            item['similarity'] = 100
    else:
        item['similarity'] = 100
        item['exception_info'] = "not normal response"
    return item
