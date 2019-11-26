#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""使用ORM模型定义USER表"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from executor.database.models.base import Model
from executor.common.constant import Roles


class Users(Model):
    """user表ORM模型"""
    __tablename__ = "users"
    id = Column(Integer, autoincrement=True, primary_key=True, unique=True)
    user_id = Column(String(64), unique=True, nullable=False)
    username = Column(String(64), nullable=False, unique=True)
    password = Column(String(64), nullable=False)
    role = Column(String(32), nullable=True, default=Roles.member)
    phone = Column(String(16), unique=True, index=True, nullable=False)
    gender = Column(String(32), nullable=True)
    create_at = Column(DateTime, nullable=False)
    avatar = Column(String(255), default=None, nullable=True)
    enabled = Column(Boolean, nullable=True, default=True)
    access_token = Column(String(255), default=None, nullable=True)
    extra = Column(String(255), default=None, nullable=True)
