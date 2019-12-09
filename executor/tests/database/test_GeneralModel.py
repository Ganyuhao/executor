# !/usr/bin/env python
# coding: utf-8
# @Time     : 2019/11/22 15:08
# @Author   : Mr.Gan
# Software  : PyCharm
"""通用模型测试"""

from sqlalchemy import Column, String

from executor.database.models.base import Model
from executor.tests.database.base import DatabaseTestCase


class TokenModel(Model):
    __tablename__ = "tokens"
    token = Column(String(32), nullable=True)


class TestBaseDataModel(DatabaseTestCase):

    def test_tokens_field(self):
        """测试tokens表的字段是有继承于通用模型类"""
        expect = {
            "token": "adadadadadadwadad",
        }
        fm = TokenModel(**expect)
        self.assertTrue(hasattr(fm, "id"))
        self.assertTrue(hasattr(fm, "create_at"))
        self.assertTrue(hasattr(fm, "update_at"))
