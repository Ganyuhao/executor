# !/usr/bin/env python
# coding: utf-8
# @Time     : 2019/11/9 11:41
# @Author   : Mr.Gan
# Software  : PyCharm
"""Model基类定义"""

import json
import logging
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import String, Integer, DateTime, Boolean
from sqlalchemy import Column
from executor.exceptions import MissNecessaryFields

LOG = logging.getLogger(__name__)


def datetime_convert(value):
    """转换时间字符串为时间对象"""
    # value为字符串时转换
    if isinstance(value, str):
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    # value为时间对象时直接返回
    return value


def integer_convert(value):
    """转换整型数据"""
    if value is None:
        return None
    return int(value)


class _ModelBase:
    """Model元类的基类，也是所有数据表的基类"""

    # 数据库字段与python数据类型转换对应表
    type_mappers = {
        String: str,
        Integer: integer_convert,
        DateTime: datetime_convert,
        Boolean: bool,
    }

    def to_json(self):
        """将ORM模型转换为Json,所有模型的extra列都必须是Json字符串或None"""
        ret = dict()
        table = self.__class__.__dict__.get("__table__")
        for col in table.columns:
            name = col.name
            value = getattr(self, name)
            if name == "extra":
                # extra列必须是json字符串
                value = json.loads(value) if value else {}
            ret.setdefault(name, value)
        return ret

    @classmethod
    def from_json(cls, model):
        """
        从Json数据反序列化一个ORM模型

        :param model: dict格式的数据
        """
        self = cls()
        table = cls.__dict__.get("__table__")
        for col in table.columns:
            name = col.name
            _type = col.type
            convert = cls.type_mappers[_type.__class__]
            value = model.get(name)
            if not value and value is None:
                # 如果字段为创建时间 并且必填 则跳过
                if name == "create_at" and not col.nullable:
                    continue
                # 如字段为主键 or 外键 为 user_id
                if not col.nullable and not col.primary_key\
                        and not col.name == "user_id":
                    # 不允许为空，且未传值，则抛出异常
                    raise MissNecessaryFields(field=name)
                continue
            # 特殊处理extra字段
            if name == "extra":
                value = json.dumps(value)
            else:
                value = convert(value)
            setattr(self, name, value)
        return self


Model = declarative_base(cls=_ModelBase)


class GeneralModel:
    """通用模型"""
    id = Column(Integer, autoincrement=True, primary_key=True, unique=True)
    create_at = Column(DateTime, nullable=True)
    update_at = Column(DateTime, nullable=True)
