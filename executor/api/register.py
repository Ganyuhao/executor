#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""register and setting app"""
import logging

from flask import request
from flask_restful import Api

from executor.api.users import UsersApi
from executor.api.login import LoginApi
from executor.exceptions import FuckerTesterException
from executor.api.hooks import HookDispatcher, ContextHook

LOG = logging.getLogger(__name__)


def _url_not_found(error):
    """unknown url path"""
    return {"error": "you request url path %s not found" % request.path}, 404


def _del_fucker_exception(error):
    """raise Fucker exception"""
    assert isinstance(error, FuckerTesterException)
    return {"error": error.msg}, error.code


def register_resource(app):
    """setup rest api handler"""
    # initial error handler
    LOG.debug("start register flask app")
    app.register_error_handler(404, _url_not_found)
    app.register_error_handler(FuckerTesterException, _del_fucker_exception)

    # setup app hook
    LOG.debug("add app hook")
    dispatcher = HookDispatcher()
    dispatcher.append_hook(ContextHook())
    dispatcher.setup_app(app)

    # setup api handler
    LOG.debug("add app api resource")
    api = Api(app, prefix="/api")
    UsersApi.setup(api)
    LoginApi.setup(api)

    LOG.debug("register flask app done")
