# !/usr/bin/env python
# -*- coning: utf-8 -*-
# @Time     : 2019/11/1 13:48
# @Author   : Mr.Gan
# Software  : PyCharm
"""database.mange，定义了表的操作方法"""

import logging
import copy

from sqlalchemy import or_
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError  # 数据库死锁异常

from executor.common.config import Manage
from executor.database.models.user import Users
from executor import exceptions
from executor.common.utils import retry_on_exception
from executor.database.models.base import Model

CONF = Manage()
LOG = logging.getLogger(__name__)


class Database:
    """提供表的增删改查方法"""
    connect_formatter = "mysql+mysqlconnector:" \
                        "//%(user)s:%(password)s" \
                        "@%(host)s:%(port)s/%(database)s?" \
                        "charset=utf8"

    def __init__(self, database_name="fucker_tester"):
        self.database_name = database_name
        self._connect_info = {
            "user": CONF.database_username,
            "password": CONF.database_password,
            "host": CONF.database_host,
            "port": str(CONF.database_port),
            "database": self.database_name,
        }
        self._ensure_database_exist()
        self.engine = create_engine(
            self.connect_formatter % self._connect_info,
            max_overflow=0,
            pool_size=5,
            pool_timeout=30,
            pool_recycle=-1
        )
        Model.metadata.create_all(bind=self.engine)
        self.session_maker = sessionmaker(bind=self.engine)

    def session(self):
        """返回一个新的session"""
        return self.session_maker()

    def _ensure_database_exist(self):
        """
        确保数据库存在
        """
        _connect_info = copy.deepcopy(self._connect_info)
        _connect_info.update({"database": ""})
        connect_str = self.connect_formatter % _connect_info
        with create_engine(
                connect_str,
                isolation_level="AUTOCOMMIT").connect() as connection:
            connection.execute(
                "CREATE DATABASE IF NOT EXISTS %s" % self.database_name)
            connection.execute("use %s" % self.database_name)

    def _get_session(self, ctx):
        """获取session"""
        if hasattr(ctx, "session"):
            return getattr(ctx, "session")
        return self.session()

    @retry_on_exception(InvalidRequestError)
    def create_user(self, ctx, user_model):
        """添加用户"""
        session = self._get_session(ctx)
        # 调用查询用户函数，如果抛出用户不存在异常，则开始添加用户
        if self.user_exist(ctx, user_model):
            raise exceptions.UserAlreadyExistException(
                identity=user_model.name)
        session.add(user_model)
        return self.get_user(ctx, user_model.name, user_model.password)

    @retry_on_exception(InvalidRequestError)
    def list_user(self, ctx):
        """返回所有用户列表"""
        return self._get_session(ctx).query(Users).order_by(Users.id).all()

    @retry_on_exception(InvalidRequestError)
    def user_exist(self, ctx, user_model):
        """判断用户是否存在"""
        condition = or_(
            Users.id == user_model.id,
            Users.phone == user_model.phone,
            Users.name == user_model.name,
            Users.user_id == user_model.user_id,
        )
        return self._get_session(ctx).query(Users).filter(
            condition).count() == 1

    @retry_on_exception(InvalidRequestError)
    def get_user(self, ctx, user_identity, password):
        """
        通过id、用户名、电话， 抛出用户不存在异常和密码错误异常
        """
        # 多条件查询用户信息，返回单条对象，如果查询结果有多条，抛出异常
        condition = or_(
            Users.id == user_identity,
            Users.phone == user_identity,
            Users.name == user_identity,
            Users.user_id == user_identity,
        )
        user = self._get_session(ctx).query(Users).filter(condition).first()
        if not user:
            raise exceptions.UserNotExistException(identity=user_identity)
        if user.password != password:
            raise exceptions.IncorrectPasswordException()
        return user

    @retry_on_exception(InvalidRequestError)
    def delete_user(self, ctx, user_identity, password):
        """删除用户"""
        user = self.get_user(ctx, user_identity, password)
        session = self._get_session(ctx)
        session.delete(user)
