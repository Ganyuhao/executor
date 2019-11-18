# !/usr/bin/env python
# coding: utf-8
# @Time     : 2019/11/18 9:21
# @Author   : Mr.Gan
# Software  : PyCharm

from flask import jsonify
from flask_restful import (
Resource, Api,
reqparse, fields,
marshal
)

from executor.main import APP
from executor.database.models.user import Users
from executor.database.manage import Database
from executor.common.context import Context
from executor.exceptions import UserAlreadyExistException

# 获取 数据库 ORM 对象 与 上下文 对象
DB = Database()
CONTEXT = Context(None, DB.session(), None)

# 错误异常
ERRORS = {
    'UserAlreadyExistsError': {
        'message': "A user with that username already exists.",
        'status': 409,
    },
    'ResourceDoesNotExist': {
        'message': "A resource with that ID no longer exists.",
        'status': 410,
        'extra': "Any extra information you want.",
    },
}

# 注册
API = Api(APP, catch_all_404s=True, errors=ERRORS)

# 参数解析
PARSER = reqparse.RequestParser()
PARSER.add_argument('username', required=True, type=str)
PARSER.add_argument('password', required=True, type=str)
PARSER.add_argument('role', required=True, type=str)
PARSER.add_argument('phone', required=True, type=str)
PARSER.add_argument('gender', type=str)
PARSER.add_argument('create_at', required=True, type=fields.datetime)
PARSER.add_argument('avatar', type=str)
PARSER.add_argument('enabled', required=True, type=bool)
PARSER.add_argument('access_token', type=str)
PARSER.add_argument('extra', type=str)

# 定义参数类型
RESOURCE_FULL_FIELDS = {
    'id': fields.Integer,
    'username': fields.String,
    'password': fields.String,
    'role': fields.String,
    'phone': fields.String,
    'gender': fields.String,
    'create_at': fields.DateTime,
    'avatar': fields.String,
    'enabled': fields.Boolean,
    'access_token': fields.String,
    'extra': fields.String
}


class Common:
    """user 接口返回消息公共类"""

    @classmethod
    def return_true_json(cls, data, msg="request successful"):
        # 输出字段解析
        data = marshal(data, RESOURCE_FULL_FIELDS)
        return jsonify({
            "status": 1,
            "data": data,
            "msg": msg
        })

    @classmethod
    def return_false_json(cls, data=None, msg="request was aborted"):
        msg = str(msg)
        return jsonify({
            "status": 0,
            "data": data,
            "msg": msg
        })


class UserApi(Resource):
    """用户注册API POST"""
    def post(self):
        PARSER.parse_args()
        args = PARSER.parse_args()
        user = Users.from_json(args)
        try:
            # 捕捉用户已存在异常，返回到客户端
            user = DB.create_user(CONTEXT, user)
        except UserAlreadyExistException as error:
            CONTEXT.session.close()
            return Common.return_false_json(msg=error)
        else:
            CONTEXT.session.commit()
            return Common.return_true_json(user)
