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
from executor.exceptions import *

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
        """请求没有异常抛出，则提交事务,
        事务提交失败，则回滚"""
        try:
            G.context.session.commit()
        except (Exception,):
            G.context.session.rollback()
        finally:
            G.context.session.close()

    @staticmethod
    @APP.before_request
    def get_context():
        """每次请求前运行，添加 context 对象到 钩子中"""
        db = Database()
        G.db = db
        G.context = Context(None, G.db.session(), None)

    @staticmethod
    @APP.errorhandler(500)
    def server_error(error):
        return "错错错"

    @staticmethod
    @APP.errorhandler(NotFoundException)
    def not_found(error):
        response = dict(status=NotFoundException.code, message=NotFoundException.message)
        return jsonify(response), 404

    @staticmethod
    @APP.errorhandler(ForbiddenException)
    def user_exit(error):
        response = dict(status=ForbiddenException.code, message=
                        "bu neng fang wen")
        return jsonify(response), 403
