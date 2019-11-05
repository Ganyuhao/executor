#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
单元测试配置，初始化单元测试时的配置信息
"""

ITEMS = {
    "host": "0.0.0.0",
    "port": "5001",
    "database_port": 3306,
    "debug": False,
    "log_file": "executor.log",
    "database_username": "root",
    "database_host": "10.34.130.44",
    "database_password": "root",
}


def setup_fake_conf():
    """
    加载单元测试的配置信息
    """
    from executor.common.config import Manage
    Manage().update_config_items(**ITEMS)
