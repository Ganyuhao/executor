#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
单元测试基类
"""
import os
import unittest
from datetime import datetime

from executor.common.context import Context
from executor.common.config import Manage
from executor.database.manage import Database
from executor.database.models.user import Users


def get_config_item(item, default, type_c):
    upper_item = str(item).upper().replace("-", "_")
    env_var = os.getenv("FUCKER_EXECUTOR_%s" % upper_item)
    if env_var:
        var = env_var
    else:
        var = default
    if not type_c:
        return str(var)
    elif type_c == bool:
        return str(var).lower() == "true"
    return type_c(var)


class TestCase(unittest.TestCase):
    config_items = {
        "host": get_config_item("host", "0.0.0.0", str),
        "port": get_config_item("port", "5001", int),
        "database_port": get_config_item("database_port", 3306, int),
        "debug": get_config_item("debug", False, bool),
        "log_file": get_config_item("log_file", "executor.log", str),
        "database_username": get_config_item("database_username", "root", str),
        "database_host": get_config_item("database_host", "10.34.130.44", str),
        "database_password": get_config_item("database_password", "root", str),
    }

    @classmethod
    def setUpClass(cls):
        conf = Manage(**cls.config_items)
        conf.update_config_items(**cls.config_items)
        cls.conf = Manage()
