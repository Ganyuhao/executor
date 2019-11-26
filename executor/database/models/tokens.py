#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author:      Mr.Gan 
# @Time:        2019/11/26 21:00
# @File:        tokens.py

"""token模型"""

from sqlalchemy import Column, String, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship
from executor.database.models.base import Model, GeneralModel


class Tokens(Model, GeneralModel):
    """token 表ORM模型"""
    __tablename__ = "token"
    token = Column(String(64), nullable=False, unique=True)
    # 定义外键 users.id
    u_id = Column(Integer, ForeignKey('users.id'))
    # 建立与主表 users 的关系
    users = relationship("Users", back_populates="tokens_u")
    expire_at = Column(DateTime, nullable=True)
