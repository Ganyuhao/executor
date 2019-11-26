#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""User Resource"""
from flask_restful import fields
from flask_restful import marshal

from executor.api.base import Restful
from executor.database.manage import Users
from executor.common.constant import Roles
from executor.common.policy import enforce


class UsersApi(Restful):
    """user api"""
    rule = "users"

    # 扩充父级解析器
    parser = Restful.parser.copy()
    # 参数解析
    parser.add_argument('username', required=True, type=str)
    parser.add_argument('password', required=True, type=str)
    parser.add_argument('phone', required=True, type=str)

    # 定义参数类型
    resource_full_fields = {
        "id": fields.Integer,
        "user_id": fields.String,
        "username": fields.String,
        "password": fields.String,
        "role": fields.String,
        "phone": fields.String,
        "gender": fields.String,
        "create_at": fields.DateTime,
        "avatar": fields.String,
        "enabled": fields.Boolean,
        "access_token": fields.String,
    }

    @enforce(Roles.admin)
    def get(self, req):
        """list users"""
        ctx = req.ctx
        return ctx.db_base.list_users(ctx)

    @enforce(Roles.guest)
    def post(self, req):
        """注册"""
        args = self.parser.parse_args()
        user = Users.from_json(args)
        ctx = req.ctx
        user_data = ctx.db_base.create_user(ctx, user)
        return marshal(user_data, self.resource_full_fields)
