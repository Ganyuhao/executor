# !/usr/bin/env python
# coding: utf-8
# @Time     : 2019/11/18 14:28
# @Author   : Mr.Gan
# Software  : PyCharm

from flask_restful import (Resource, marshal,
                           reqparse)
from flask import jsonify
from flask import g

from executor.database.manage import Database
from executor.common.context import Context
from executor.api import APP

# 钩子，用于添加context
G = g


class RestfulBase(Resource):
    """user 接口返回消息公共类"""
    # 父级解析器，默认为 id，所有子类通用
    parser = reqparse.RequestParser()
    parser.add_argument("id", type=int)
    success_msg = "request successful"
    fail_msg = "request was aborted"

    @staticmethod
    @APP.after_request
    def return_true_json(response, return_format=None):
        """在请求处理完成后，进行参数解析返回"""
        if isinstance(response, str):
            pass

    @staticmethod
    @APP.before_first_request
    def get_database_conn():
        """连接数据库，添加 db 对象到 钩子中"""
        G.db = Database()

    @staticmethod
    @APP.before_request
    def get_context():
        """每次请求前运行，添加 context 对象到 钩子中"""
        G.context = Context(None, G.db.session(), None)
