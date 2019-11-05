# !/usr/bin/env python
# -*- coning: utf-8 -*-
# @Time     : 2019/11/1 13:48
# @Author   : Mr.Gan
# Software  : PyCharm
"""database.mange，定义了表的操作方法"""

import logging

from sqlalchemy import or_

from executor.database import connect
from executor.model.user import Users
from executor import exceptions

LOG = logging.getLogger(__name__)


class Database:
    """提供表的增删改查方法"""

    def create_user(self, user_model):
        """添加用户"""
        session = connect.get_session()
        # 调用查询用户函数，如果抛出用户不存在异常，则开始添加用户
        try:
            user = self.get_user(user_model.name, user_model.password)
            raise exceptions.UserAlreadyExistException(identity=user.name)
        except exceptions.UserNotExistException:
            try:
                session.add(user_model)
                session.commit()
                session.close()
                return
            except (Exception,) as error:
                LOG.error(error)
                raise exceptions.UserConflictException()

    @staticmethod
    def list_user():
        """返回所有用户列表"""
        session = connect.get_session()
        data = session.query(Users).order_by(Users.id).all()
        session.close()
        return data

    @staticmethod
    def get_user(user_identity, password):
        """
        通过id、用户名、电话， 抛出用户不存在异常和密码错误异常

        :param user_identity: 用户唯一标识，可以是ID、用户名、电话
        :param password: 用户密码
        """
        session = connect.get_session()
        # 多条件查询用户信息，返回单条对象，如果查询结果有多条，抛出异常
        condition = or_(
            Users.id == user_identity,
            Users.phone == user_identity,
            Users.name == user_identity,
        )
        user = session.query(Users).filter(condition).first()
        if not user:
            raise exceptions.UserNotExistException(name=user_identity)
        if user.password != password:
            raise exceptions.IncorrectPasswordException()
        return user
