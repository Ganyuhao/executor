# !/usr/bin/env python
# coding: utf-8
# @Time     : 2019/11/7 14:22
# @Author   : Mr.Gan
# Software  : PyCharm
"""测试 executor.common.config 文件代码"""
import os

from executor.tests.base import TestCase
from executor.common import config
from click.exceptions import BadParameter


class TestConfigFileMethod(TestCase):

    def test_PortParamType_exception(self):
        """端口错误 测试PortParamType 抛出异常"""
        values = [
            "50222250",
            "hello",
            "$./*\\@",
            "(001880)*"
        ]
        for value in values:
            self.assertRaises(
                BadParameter, config.PortParamType().convert,
                value, None, None
            )

    def test_PortParamType_return_result(self):
        """测试 端口正常 PortParamType 返回结果"""
        values = [
            0,
            65535,
            "0",
            "65535",
            3306
        ]
        for value in values:
            self.assertEqual(config.PortParamType().convert(
                value, None, None
            ), int(value))

    def test_PortParamType_repr(self):
        """测试 __repr__返回值"""
        self.assertEqual(config.PortParamType().__repr__(), "PORT")

    def test_IpAddressParamType_exception(self):
        """测试 ip 不合法 抛出异常"""
        values = [
            "255.256.255.266",
            "192.124.1.a",
            "192..168.1",
            "127.10.01.*?",
            "10.11.23.256"
        ]
        for value in values:
            self.assertRaises(
                BadParameter,
                config.IpAddressParamType().convert,
                value, None, None
            )

    def test_IpAddressParamType_return_result(self):
        """测试 ip 正常 IpAddressParamType 返回结果"""
        values = [
            "1.1.0.1",
            "0.0.0.0",
            "124.132.10.255",
            "255.255.255.255"
        ]
        for value in values:
            self.assertEqual(
                config.IpAddressParamType().convert(
                    value, None, None
                ),
                value
            )

    def test_IpAddressParamType_repr(self):
        """测试 IpAddressParamType __repr__"""
        value = "IP"
        self.assertEqual(
            config.IpAddressParamType().__repr__(),
            value
        )

    def test_Manage_exception(self):
        """测试 Manage 对象找不到属性时， 抛出异常"""
        conf = config.Manage()
        self.assertRaises(
            AttributeError, conf.__getattr__, "age"
        )

    def test_Manage_setup_log(self):
        """测试 setup_log 配置日志是否正确"""
        # debug 能否正常启用
        self.conf.setup_log()
        self.assertTrue(
            os.path.isfile(self.conf.log_file)
        )
        self.assertNotEqual(
            os.path.getsize(self.conf.log_file), 0
        )
