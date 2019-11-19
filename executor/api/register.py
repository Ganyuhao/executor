# !/usr/bin/env python
# coding: utf-8
# @Time     : 2019/11/18 17:33
# @Author   : Mr.Gan
# Software  : PyCharm

from executor.api import APP
from flask_restful import Api
from executor.api.user_api import UserApi


# 注册
API = Api(APP, catch_all_404s=True)

# 所有 API 添加处
API.add_resource(UserApi, '/users')  # userAPI
