#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""API鉴权相关代码"""
from functools import wraps

from executor.common import constant
from executor import exceptions


def enforce(required=constant.ROLE_GUEST):
    """
    校验身份用户身份的Handler装饰器，默认是Guest权限，若权限不足则直接返回401
    """
    assert required in constant.ROLES

    def wrap(handler):
        @wraps(handler)
        def _inner(self, req, *args, **kwargs):
            # 没有上下文，用户未登陆， 且API不是访客权限，直接拒绝访问
            if req.ctx is None and required != constant.ROLE_GUEST:
                raise exceptions.AccessDeniedException()
            current_user = req.ctx.user
            # 当前用户未登录， API需权限， 拒接访问
            if not current_user and required != constant.ROLE_GUEST:
                raise exceptions.AccessDeniedException()
            user_role = current_user.role
            if verify_permission(user_role, required):
                return handler(req, *args, **kwargs)
            # 当前用户权限不足，拒接访问
            raise exceptions.AccessDeniedException()

        return _inner

    return wrap


def verify_permission(role, required):
    """校验权限"""
    assert role in constant.ROLES
    assert required in constant.ROLES
    if required == constant.ROLE_ADMIN:
        return role == constant.ROLE_ADMIN
    if required == constant.ROLE_VIP:
        return role in (constant.ROLE_VIP, constant.ROLE_ADMIN)
    if required == constant.ROLE_MEMBER:
        return role != constant.ROLE_GUEST
    return True
