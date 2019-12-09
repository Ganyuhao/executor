# !/usr/bin/env python
# coding: utf-8
"""生成与验证token"""

import hashlib
import os
import time
import base64


class TokenManage:
    """Token类"""
    def __init__(self, aging=259200):
        """token 默认有效期 72 小时"""
        self.aging = aging

    def generate_token(self, times):
        """生成token"""
        # 加密
        sha1_token = hashlib.sha1(os.urandom(24)).hexdigest()
        create_time = int(times)
        time_group = str(create_time) + ":" + str(self.aging)
        time_group = time_group.encode("utf8")
        # 当前时间+时间间隔 生成base64编码 并且去掉 '='
        time_token = base64.urlsafe_b64encode(time_group) \
            .decode("utf8").strip().lstrip().rstrip("=")
        token = sha1_token + time_token
        return token

    def checkout_token(self, token, _create=None):
        """验证token"""
        result = {}
        decode_time = self._safe_b64decode(token[40:]).decode("utf8")
        # 分割时间字符串
        decode_split_time = decode_time.split(":")
        # 解密创建时间
        decode_create_time = decode_split_time[0]
        # 解密时效
        decode_aging_time = decode_split_time[1]
        # 获取当前时间
        now_time = int(time.time())
        # 时间差
        difference_time = now_time - int(decode_create_time)
        # 判断 是否失效 如果失效state值为0，生成新的token
        if difference_time > int(decode_aging_time):
            result["code"] = 0
            result["token"] = self.generate_token(_create)
        else:
            result["code"] = 1
            result["token"] = token
        return result

    @staticmethod
    def _safe_b64decode(hax):
        """base64'='符号添加"""
        length = len(hax) % 4
        for index in range(length):
            hax = hax + "="
        return base64.b64decode(hax)
