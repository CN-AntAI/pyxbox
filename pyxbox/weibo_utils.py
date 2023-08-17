# #!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2023/8/17 21:58
# @Author : BruceLong
# @FileName: weibo_utils.py
# @Email   : 18656170559@163.com
# @Software: PyCharm
# @Blog ：http://www.cnblogs.com/yunlongaimeng/
import re

str62keys = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def get_id_from_url(url):
    mid = get_mid_from_url(url)
    if not mid:
        return ""
    return mid_to_id(mid)


def get_mid_from_url(url):
    if not url:
        return ""

    if '?' in url:
        url = url.split('?')[0]

    pattern = r'^https?://(?:[\w\-]+\.)?weibo\.com/[\w\-]+/(?P<id>[\w\-]+)$'
    match = re.match(pattern, url)
    if match:
        id = match.group("id")
        if id.isdigit():
            return id_to_mid(id)
        else:
            return id
    return ""


def mid_to_id(mid):
    id_ = ""
    for i in range(len(mid) - 4, -4, -4):
        offset1 = 0 if i < 0 else i
        length = len(mid) % 4 if i < 0 else 4
        substr = mid[offset1: offset1 + length]
        substr = str62_to_int(substr)
        if offset1 > 0:
            while len(substr) < 7:
                substr = "0" + substr
        id_ = substr + id_
    return id_


def id_to_mid(id_):
    mid = ""
    for i in range(len(id_) - 7, -7, -7):
        start_idx = 0 if i < 0 else i
        length = len(id_) % 7 if i < 0 else 7
        temp_str = id_[start_idx: start_idx + length]
        mid = int_to_str62(int(temp_str)) + mid
    return mid


def str62_to_int(str62):
    int10 = 0
    for i, char in enumerate(str62[::-1]):
        int10 += str62keys.index(char) * (62 ** i)
    return str(int10)


def int_to_str62(int10):
    s62 = ""
    while int10:
        r = int10 % 62
        s62 = str62keys[r] + s62
        int10 //= 62
    return s62
