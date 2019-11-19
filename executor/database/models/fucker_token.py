# !/usr/bin/env python
# coding: utf-8
# @Time     : 2019/11/19 14:45
# @Author   : Mr.Gan
# Software  : PyCharm


from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship

from executor.database.models.base import Model, GeneralModel


class Tokens(Model, GeneralModel):
    """user表ORM模型"""
    __tablename__ = "tokens"
    token = Column(String(64), nullable=False, unique=True)
    # 定义外键 users.id
    users_id = Column(Integer, ForeignKey('users.id'))
    # 建立与主表 users 的关系
    parent = relationship("Users", back_populates="tokens_ren")
