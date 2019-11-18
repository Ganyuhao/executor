# !/usr/bin/env python
# coding: utf-8
# @Time     : 2019/11/18 14:28
# @Author   : Mr.Gan
# Software  : PyCharm


from flask_restful import (Resource, marshal, Api,
                           reqparse)
from flask import jsonify

from executor.main import APP
from executor.api.user_api import UserApi

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
# 所有 API 添加处
APP.add_resource(UserApi, '/users/<int:userId>/<string:password>')  # userAPI


class Common(Resource):
    """user 接口返回消息公共类"""
    # 父级解析器，默认为 id，所有子类通用
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)

    def __init__(self, return_format=None):
        """:param return_format:   返回参数解析格式"""
        self.return_format = return_format

    def return_true_json(self, data, msg="request successful"):
        # 输出字段解析
        data = marshal(data, self.return_format)
        return jsonify({
            "status": 1,
            "data": data,
            "msg": msg
        })

    def return_false_json(self, data=None, msg="request was aborted"):
        msg = str(msg)
        return jsonify({
            "status": 0,
            "data": data,
            "msg": msg
        })
