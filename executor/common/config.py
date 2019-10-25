#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
fucker-executor的配置信息
"""
import re
import sys
from functools import partial
import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter

import six
from click.types import StringParamType, IntParamType

LABEL = """
                       .::::.
                     .::::::::.
                    :::::::::::  FUCK YOU
                ..:::::::::::'
              '::::::::::::'
                .::::::::::
           '::::::::::::::..
                ..::::::::::::.
              ``::::::::::::::::
               ::::``:::::::::'        .:::.
              ::::'   ':::::'       .::::::::.
            .::::'      ::::     .:::::::'::::.
           .:::'       :::::  .:::::::::' ':::::.
          .::'        :::::.:::::::::'      ':::::.
         .::'         ::::::::::::::'         ``::::.
     ...:::           ::::::::::::'              ``::.
    ```` ':.          ':::::::::'                  ::::..
                       '.:::::'                    ':'````..
"""

LOG = logging.getLogger(__name__)


class PortParamType(IntParamType):
    """
    检测端口是否合法，不合法则抛出异常，合法则返回端口值
    """
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
    """
    检测IP是否合法，如果不合法则抛出异常，合法则返回IP参数
    """
    name = "ip"
    _regex = r"(?=(\b|\D))(((\d{1,2})|(1\d{1,2})|(2[0-4]\d)|(25[0-5]))\.)" \
             r"{3}((\d{1,2})|(1\d{1,2})|(2[0-4]\d)|(25[0-5]))(?=(\b|\D))"

    def raise_fail(self, value, param, ctx):
        """统一使用此方法抛出错误描述"""
        self.fail("%s is not a valid ip address" % value, param, ctx)

    def convert(self, value, param, ctx):
        fail = partial(self.raise_fail, value=value, param=param, ctx=ctx)
        value = super(IpAddressParamType, self).convert(value, param, ctx)
        # 校验IP是否合法
        if re.match(self._regex, value) is not None:
            return value
        fail()
        return None

    def __repr__(self):
        return "IP"


class Manage:
    """
    单例类，该类接收程序启动时，所设置的配置参数
    """
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

    def setup_log(self):
        """
        日志系统配置, state参数为配置日志输出等级，True为DEBUG， False为INFO，
        日志系统默认为INFO输出, log_file_path为日志输出的目录，如果目录不存在，
        则会动态创建
        """
        # basic config for logging need invoke before add handler to root
        formatter = "[%(asctime)s %(levelname)s " \
                    "%(pathname)s:%(lineno)s] %(message)s"
        data_fmt = "%Y/%m/%d %H:%M:%S"
        log_format = Formatter(formatter, datefmt=data_fmt)
        logging.basicConfig(
            format=formatter, datefmt=data_fmt, stream=sys.stderr,
            level=self.debug and logging.DEBUG or logging.INFO,
        )
        file_handler = RotatingFileHandler(self.log_file)
        file_handler.setFormatter(log_format)
        # Root logger add file handler
        logging.getLogger().addHandler(file_handler)
        self._debug_config_items()

    def _debug_config_items(self):
        for line in str(LABEL).split("\n"):
            LOG.debug(line)
        LOG.debug("=" * 50)
        LOG.debug("|%s|", "-Fucker Executor config-".center(48))
        LOG.debug("=" * 50)
        for key, value in six.iteritems(self.items):
            LOG.debug("|%s:%s|", key.center(17), str(value).center(30))
        LOG.debug("=" * 50)
        LOG.debug("success setup logging config")
