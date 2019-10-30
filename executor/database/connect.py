#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""初始化连接数据库"""

import logging

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

from executor.common.config import Manage
from executor.exceptions import DatabaseConnException

LOG = logging.getLogger(__name__)
BASE = declarative_base()
CONF = Manage()


def init_db():
    """初始化连接数据库,设置连接条件"""
    port = CONF.database_port
    host = CONF.host
    name = CONF.database_name
    pwd = CONF.database_password
    try:
        engine = create_engine(
            "mysql+mysqlconnector://{}:{}@{}:{}/fucker_tester?"
            "charset=utf8".format(
                name,
                pwd,
                host,
                port
            ),
            # 设置连接条件，连接池大小，线程等待时长，回收线程时间
            max_overflow=0,
            pool_size=5,
            pool_timeout=30,
            pool_recycle=-1
        )
    except Exception as database_error:
        LOG.error(database_error)
        raise DatabaseConnException(host=host, port=port, name=name)

    # 读取继承了Base类的所有表在数据库中进行创建
    BASE.metadata.create_all(engine, )
