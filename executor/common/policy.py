#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""API鉴权相关代码"""
from functools import wraps

from executor.common.constant import Roles
from executor import exceptions


def enforce(required=Roles.guest):
    """
    校验身份用户身份的Handler装饰器，默认是Guest权限，若权限不足则直接返回401
    """
    assert Roles.contains(required)

    def wrap(handler):
        @wraps(handler)
        def _inner(self, req, *args, **kwargs):
            # 没有上下文，用户未登陆， 且API不是访客权限，直接拒绝访问
            if not hasattr(req, "ctx") and required != Roles.guest:
                raise exceptions.AccessDeniedException()
            current_user = req.ctx.user
            # 当前用户未登录， API需权限， 拒接访问
            if not current_user and required != Roles.guest:
                raise exceptions.AccessDeniedException()
            user_role = getattr(current_user, "role", Roles.guest)
            if Roles.permission_check(user_role, required):
                return handler(self, req, *args, **kwargs)
            # 当前用户权限不足，拒接访问
            raise exceptions.AccessDeniedException()

        return _inner

    return wrap
