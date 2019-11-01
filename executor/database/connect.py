#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""初始化连接数据库"""

import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from executor.common.config import Manage
from executor.exceptions import DatabaseConnException
from executor.model import BASE

LOG = logging.getLogger(__name__)
CONF = Manage()
ENGINE = None

# pylint: disable=wrong-import-position
from executor.model.user import Users as _  # pylint: disable=unused-import


def init_db():
    """
    初始化连接数据库,设置连接条件
    必须在所有ORM模型都被申明后才可以调用该方法，不然该步骤不会同步数据库表格
    """
    # pylint: disable=global-statement
    global ENGINE
    if ENGINE:
        return
    connect_formatter = "mysql+mysqlconnector://{}:{}@{}:{}/{}?charset=utf8"
    try:
        with create_engine(
                connect_formatter.format(
                    CONF.database_username,
                    CONF.database_password,
                    CONF.database_host,
                    CONF.database_port,
                    ""),
                isolation_level="AUTOCOMMIT").connect() as connection:
            connection.execute("CREATE DATABASE IF NOT EXISTS fucker_tester")
        ENGINE = create_engine(
            connect_formatter.format(
                CONF.database_username,
                CONF.database_password,
                CONF.database_host,
                CONF.database_port,
                "fucker_tester"),
            max_overflow=0,
            pool_size=5,
            pool_timeout=30, pool_recycle=-1)
    except Exception as error:
        LOG.error(error)
        raise DatabaseConnException(
            host=CONF.database_host,
            port=CONF.database_port,
            name=CONF.database_username)

    BASE.metadata.create_all(ENGINE, )


def get_session():
    """获取数据库会话"""
    # pylint: disable=global-statement
    global ENGINE
    if not ENGINE:
        LOG.critical(
            "the session can only be obtained after the engine is initialized"
        )
    return sessionmaker(bind=ENGINE)()
