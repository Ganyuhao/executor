#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""define request hook class"""
import logging

from flask import request

from executor.database.manage import Database
from executor.common.context import Context

LOG = logging.getLogger(__name__)


class HookDispatcher:
    """schedule hook for flask"""

    def __init__(self, hooks=None):
        self.hooks = hooks if hooks else []

    def append_hook(self, hook):
        """append hook for dispatcher"""
        assert isinstance(hook, Hook)
        LOG.debug("append hook %s" % hook.name)
        self.hooks.append(hook)

    def setup_app(self, app):
        """setup hook for app"""
        for hook in self.hooks:
            app.before_request_funcs.setdefault(
                None, []).append(getattr(hook, "before_request"))
            app.after_request_funcs.setdefault(
                None, []).append(getattr(hook, "after_request"))
            app.teardown_request_funcs.setdefault(
                None, []).append(getattr(hook, "teardown_request"))


class Hook:
    """Basic class for Hook"""
    name = "hook"

    def before_request(self):
        """before request"""

    def after_request(self, resp):
        """after request"""

    def teardown_request(self, exc):
        """teardown each request"""


class ContextHook(Hook):
    """setup context for each request"""

    db_base = None
    name = "context"

    def __init__(self):
        self.db_base = Database()

    def before_request(self):
        """set context for each request"""
        request.ctx = Context(request, self.db_base.session())
        # 解决处理请求时 ctx 没有 db 属性问题
        setattr(Context, "db_base", self.db_base)

    def after_request(self, resp):
        """if request success, commit db session"""
        request.ctx.session.commit()
        return resp

    def teardown_request(self, exc):
        """if raise exception, just rollback and close session"""
        if exc:
            request.ctx.session.rollback()
        request.ctx.session.close()
