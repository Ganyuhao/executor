#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""使用ORM模型定义USER表"""

import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from executor.model import BASE


class Users(BASE):
    """user表ORM模型"""
    __tablename__ = "users"
    id = Column(Integer, autoincrement=True, primary_key=True, unique=True)
    name = Column(String(32), primary_key=True, nullable=False)
    password = Column(String(32))
    role = Column(String(32), nullable=False)
    phone = Column(Integer, unique=True, index=True)
    gender = Column(String(32), nullable=True)
    create_at = Column(DateTime, default=datetime.datetime.now(),
                       nullable=False)
    expires_at = Column(DateTime, nullable=True)
    avatar = Column(String(32), nullable=True)
    enabled = Column(Boolean, nullable=True)
    access_token = Column(String(32), index=True, nullable=True)
    extra = Column(String(32), default=None)

    def __repr__(self):
        return "<User(id={},name={},password={}," \
                 "role={},phone={},gender={}," \
                 "create_at={},expires_at={},avatar={}," \
                 "enabled={},access_token={}, extra={})>"\
                 .format(
                     self.id,
                     self.name,
                     self.password,
                     self.role,
                     self.phone,
                     self.gender,
                     self.create_at,
                     self.expires_at,
                     self.avatar,
                     self.enabled,
                     self.access_token,
                     self.extra,
                 )
