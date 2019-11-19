#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""register and setting app"""
import logging

from flask import request
from flask_restful import Api

from executor.api.users import Users
from executor.exceptions import FuckerTesterException

LOG = logging.getLogger(__name__)


def _url_not_found(e):
    return {"error": "you request url path %s not found" % request.path}, 404


def _del_fucker_exception(e):
    assert isinstance(e, FuckerTesterException)
    return {"error": e.msg}, e.code


def register_resource(app):
    """setup rest api handler"""
    app.register_error_handler(404, _url_not_found)
    app.register_error_handler(FuckerTesterException, _del_fucker_exception)
    api = Api(app, prefix="/api")
    Users.setup(api)
