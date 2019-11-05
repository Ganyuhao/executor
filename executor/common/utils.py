#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
工具模块，所有通用的方法、类等都放在该模块
"""
from retrying import retry


def retry_on_exception(exceptions=None):
    """
    忽略指定异常并进行重试，重试3次，整体执行时间最大为10秒，
    每次重试的间隔为1~3秒之间的随机数
    """
    if exceptions and not isinstance(exceptions, list):
        exceptions = [exceptions]

    def _is_exception(exc):
        if not exceptions:
            return True
        for exception in exceptions:
            if isinstance(exc, exception):
                return True
            return False

    return retry(
        stop_max_attempt_number=3, stop_max_delay=10000,
        wait_random_min=1000, wait_random_max=3000,
        retry_on_exception=_is_exception,
    )
