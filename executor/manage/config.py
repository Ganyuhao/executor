#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
检测配置参数是否合法，并 添加到单例类 Manage, 调用 Manage可获取配置参数
"""
import re
from functools import partial

from click.types import StringParamType, IntParamType


class PortParamType(IntParamType):
    """检测端口是否合法，不合法则抛出异常，
    合法则返回端口值"""
    name = "port"

    def convert(self, value, param, ctx):
        """效验端口是否合法"""
        value = super(PortParamType, self).convert(value, param, ctx)
        if value > 65535 or value < 0:
            self.fail("%s is not a valid port" % value, param, ctx)
        return value

    def __repr__(self):
        return "PORT"


class IpAddressParamType(StringParamType):
    """检测IP是否合法，如果不合法则抛出异常，合法则
    返回IP参数"""
    name = "ip"

    def raise_fail(self, value, param, ctx):
        """统一使用此方法抛出错误描述"""
        self.fail("%s is not a valid ip address" % value, param, ctx)

    def convert(self, value, param, ctx):
        fail = partial(self.raise_fail, value=value, param=param, ctx=ctx)
        value = super(IpAddressParamType, self).convert(value, param, ctx)
        # 校验IP是否合法
        re_compile = re.compile(
            r"(?=(\b|\D))(((\d{1,2})|(1\d{1,2})|(2[0-4]\d)|(25[0-5]))\.)"
            r"{3}((\d{1,2})|(1\d{1,2})|(2[0-4]\d)|(25[0-5]))(?=(\b|\D))"
        )
        if re.match(re_compile, value) is not None:
            return value
        fail()
        return None

    def __repr__(self):
        return "IP"


class Manage:
    """单例类，该类接收程序启动时，所设置的配置参数"""
    items = {}

    # 该类为单例模式
    def __new__(cls, **kwargs):
        instance_key = "__instance"
        if not hasattr(cls, instance_key):
            cls.items = kwargs
            setattr(cls, instance_key, super(Manage, cls).__new__(cls))
        return getattr(cls, instance_key)

    # 获取配置项的值
    def __getattr__(self, item):
        item = str(item).lower()
        if item not in self.items:
            raise AttributeError(item)
        return self.items.get(item)
