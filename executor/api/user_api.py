# !/usr/bin/env python
# coding: utf-8
# @Time     : 2019/11/18 9:21
# @Author   : Mr.Gan
# Software  : PyCharm

from flask_restful import fields

from executor.database.models.user import Users
from executor.exceptions import UserAlreadyExistException
from executor.api.base import RestfulBase
from executor.api.base import G


class UserApi(RestfulBase):

    # 扩充父级解析器
    parser = RestfulBase.parser.copy()
    # 参数解析
    parser.add_argument('username', required=True, type=str)
    parser.add_argument('password', required=True, type=str)
    parser.add_argument('role', required=True, type=str)
    parser.add_argument('phone', required=True, type=str)
    parser.add_argument('gender', type=str)
    parser.add_argument('create_at', required=True, type=fields.DateTime)
    parser.add_argument('avatar', type=str)
    parser.add_argument('enabled', required=True, type=bool)
    parser.add_argument('access_token', type=str)
    parser.add_argument('extra', type=str)

    # 定义参数类型
    resource_full_fields = {
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

    def post(self):
        """用户注册API POST"""
        args = self.parser.parse_args()
        user = Users.from_json(args)
        try:
            # 捕捉用户已存在异常，返回到客户端
            user = G.db.create_user(G.context, user)
        except UserAlreadyExistException as error:
            G.context.session.close()
            return self.return_false_json(msg=error)
        else:
            G.context.session.commit()
            return self.return_true_json(user)
