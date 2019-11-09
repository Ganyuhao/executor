#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""使用ORM模型定义USER表"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from executor.database.models.base import Model


class Users(Model):
    """user表ORM模型"""
    __tablename__ = "users"
    id = Column(Integer, autoincrement=True, primary_key=True, unique=True)
    name = Column(String(64), nullable=False, unique=True)
    password = Column(String(32))
    role = Column(String(32), nullable=False)
    phone = Column(String(16), unique=True, index=True)
    gender = Column(String(32))
    create_at = Column(DateTime, nullable=False)
    avatar = Column(String(255))
    enabled = Column(Boolean, nullable=False)
    access_token = Column(String(255))
    extra = Column(String(255), default=None)
