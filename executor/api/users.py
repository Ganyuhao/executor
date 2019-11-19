#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""User Resource"""
from executor.api.base import Restful


class Users(Restful):
    rule = "users"

    def get(self, req):
        """list users"""
        ctx = req.ctx
        return ctx.db.list_users(ctx)
