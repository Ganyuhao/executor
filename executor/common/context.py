#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
请求上下文对象， 保存每个请求的所有上下文信息
"""


class Context:
    """请求上下文"""

    def __init__(self, req, session, user=None):
        """
        :param req: 当前的请求对象
        :param session: 一个数据库session
        :param user: 当前请求的用户信息
        """
        self.session = session
        self.req = req
        self.user = user
