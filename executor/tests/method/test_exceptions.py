# !/usr/bin/env python
# coding: utf-8
# @Time     : 2019/11/7 15:21
# @Author   : Mr.Gan
# Software  : PyCharm
"""测试 executor.exceptions 文件代码"""
import unittest

from executor import exceptions


class TestExceptionsFileMethod(unittest.TestCase):

    def test_FuckerTesterException_exception(self):
        """测试 self.kwargs[k] = six.text_type(value) 转换后是否是 str 类型 """
        fuck = exceptions.FuckerTesterException(name=ValueError(123))
        self.assertIsInstance(fuck.kwargs.get("name"), str)

    def test_FuckerTesterException_message_is_exception_subclass(self):
        """测试 message 为 Exception 子类"""
        value = "are you Okey?"
        fuck = exceptions.FuckerTesterException(message=Exception(value))
        self.assertEqual(fuck.msg, value)
