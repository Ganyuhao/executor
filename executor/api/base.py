#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Basic class define"""
import logging
from functools import wraps

from flask import request
from flask_restful import Resource

LOG = logging.getLogger(__name__)


def _insert_request_to_handler(meth):
    """将request固定为handler的第一个参数"""

    @wraps(meth)
    def _inner(*args, **kwargs):
        return meth(request, *args, **kwargs)

    return _inner


class Restful(Resource):
    """Restful Controller Base class"""
    rule = None
    method_decorators = [_insert_request_to_handler]

    @classmethod
    def setup(cls, api, **kwargs):
        """setup Resource to api component"""
        if not cls.rule:
            rule = cls.__name__.lower()
        else:
            rule = cls.rule
        api.add_resource(cls, "/%s/" % rule, **kwargs)

