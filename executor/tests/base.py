#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
单元测试基类
"""
import os
import tempfile
import unittest

from executor.common.config import Manage

import yaml


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
        "debug": get_config_item("debug", True, bool),
        "log_file": get_config_item("log_file", tempfile.mktemp(), str),
        "database_username": get_config_item("database_username", "root", str),
        "database_host": get_config_item("database_host", "127.0.0.1", str),
        "database_password": get_config_item("database_password", "",
                                             str),
    }
    data_file_path = None
    _test_dataset = {}

    @classmethod
    def setUpClass(cls):
        conf = Manage(**cls.config_items)
        conf.update_config_items(**cls.config_items)
        cls.conf = Manage()
        if cls.data_file_path:
            data_file_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "datas",
                cls.data_file_path)
            with open(data_file_path, "rb") as yaml_fp:
                cls._test_dataset = yaml.safe_load(yaml_fp)

    def get_test_date(self, *args):
        td = self._test_dataset.get(args[0], {})
        for path in args[1:]:
            td = td.get(path, {})
        return td
