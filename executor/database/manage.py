# !/usr/bin/env python
# -*- coning: utf-8 -*-
# @Time     : 2019/11/1 13:48
# @Author   : Mr.Gan
# Software  : PyCharm
"""database.mange，定义了表的操作方法"""

import time
import logging
import copy
import uuid
from datetime import datetime

from sqlalchemy import or_
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError  # 数据库死锁异常

from executor.common.config import Manage
from executor.database.models.user import Users
from executor.database.models.tokens import Tokens
from executor import exceptions
from executor.common.utils import retry_on_exception
from executor.database.models.base import Model
from executor.database.token_manage import TokenManage

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
        # 调用查询用户函数，如果用户存, 抛出异常
        if self.user_exist(ctx, user_model):
            raise exceptions.UserAlreadyExistException(
                identity=user_model.username)
        user_model.user_id = self._get_uuid()
        user_model.create_at = self._get_time()
        session.add(user_model)
        return self.get_user(ctx, user_model.username, user_model.password)

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
            Users.username == user_model.username,
            Users.user_id == user_model.user_id,
        )
        return self._get_session(ctx).query(Users).filter(
            condition).count() == 1

    def _get_uuid(self):
        """生成32为 uuid"""
        return uuid.uuid4().hex

    def _get_time(self):
        """生成创建时间"""
        return datetime.now()

    def _get_datetime(self, create_time):
        """把时间戳转换为datetime对象"""
        return datetime.fromtimestamp(create_time)

    @retry_on_exception(InvalidRequestError)
    def get_user(self, ctx, user_identity, password):
        """
        通过id、用户名、电话， 抛出用户不存在异常和密码错误异常
        """
        # 多条件查询用户信息，返回单条对象，如果查询结果有多条，抛出异常
        condition = or_(
            Users.id == user_identity,
            Users.phone == user_identity,
            Users.username == user_identity,
            Users.user_id == user_identity,
        )
        user = self._get_session(ctx).query(Users).filter(condition).first()
        if not user:
            raise exceptions.UserNotExistException(identity=user_identity)
        if user.password != password:
            raise exceptions.IncorrectPasswordException()
        token = self.issue_token(ctx, user)
        setattr(user, "token", token.token)
        return user

    @retry_on_exception(InvalidRequestError)
    def delete_user(self, ctx, user_identity, password):
        """删除用户"""
        user = self.get_user(ctx, user_identity, password)
        session = self._get_session(ctx)
        session.delete(user)

    @retry_on_exception(InvalidRequestError)
    def issue_token(self, ctx, user_model):
        """不存在则创建token，存在则验证token"""
        token_manage = TokenManage()
        session = self._get_session(ctx)
        token = self.get_token(ctx, user_model)
        create_time = time.time()
        if not token:
            # token为空则 添加
            token_model = Tokens(
                token=token_manage.generate_token(create_time),
                u_id=user_model.id,
                create_at=self._get_datetime(create_time),
                expire_at=self._get_datetime(
                    float(create_time + token_manage.aging)
                )
            )
            session.add(token_model)
        else:
            # token过期则更新
            g_token = token_manage.checkout_token(token.token, create_time)
            if not g_token.get("code"):
                # 更新token
                session.query(Tokens).filter(
                    Tokens.u_id == user_model.id).update(
                    {"token": g_token.get("token")})
                # 更新时间
                session.query(Tokens).filter(
                    Tokens.u_id == user_model.id
                ).update(
                    {"update_at": self._get_datetime(create_time)}
                )
                # 过期时间
                session.query(Tokens).filter(
                    Tokens.u_id == user_model.id
                ).update(
                    {"expire_at": self._get_datetime(
                        create_time + token_manage.aging
                    )}
                )

        return self.get_token(ctx, user_model)

    @retry_on_exception(InvalidRequestError)
    def get_token(self, ctx, user_model):
        token = self._get_session(ctx).query(Tokens).filter(
            Tokens.u_id == user_model.id
        ).first()
        return token
