# !/usr/bin/env python
# -*- coning: utf-8 -*-

"""fucker-tester base exception handling.
Includes decorator for re-raising fucker-tester-type exceptions.
SHOULD include dedicated exception logging.
"""

import re
import logging
import six

LOG = logging.getLogger(__name__)


class Error(Exception):
    """ERROR异常基类"""


class FuckerTesterException(Exception):
    """Base fucker-tester Exception
    To correctly use this class, inherit from it and define
    a 'message' property. That message will get printf'd
    with the keyword arguments provided to the constructor.
    """
    message = "An unknown exception occurred."
    code = 500
    headers = {}
    safe = False

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs

        if "code" not in kwargs:
            try:
                self.kwargs["code"] = self.code
            except AttributeError:
                LOG.exception("FuckerTesterException 缺少属性 code")
                raise AttributeError
        for k, value in self.kwargs.items():
            if isinstance(value, Exception):
                self.kwargs[k] = six.text_type(value)

        if not message:
            try:
                message = self.message % kwargs
            except (ValueError, AttributeError, TypeError, NameError,):
                # kwargs doesn't match a variable in the message
                # log the issue and the kwargs
                LOG.exception('Exception in string format operation.')
                for name, value in kwargs.items():
                    LOG.error("%(name)s: %(value)s", {
                        'name': name, 'value': value})
                raise AttributeError

        elif isinstance(message, Exception):
            message = six.text_type(message)

        if re.match(r".*[^\.]\.\.$", message):
            message = message[:-1]
        self.msg = message
        super(FuckerTesterException, self).__init__(message)


class NetworkException(FuckerTesterException):
    """网络连接异常错误"""
    message = "Exception due to network failure."


class NetworkBindException(FuckerTesterException):
    """绑定端口冲突或失败导致连接异常"""
    message = "Exception due to failed port status in binding."


class BadRequestException(FuckerTesterException):
    """错误的请求格式"""
    code = 400


class UnauthorizedException(FuckerTesterException):
    """认证错误异常"""
    code = 401


class ForbiddenException(FuckerTesterException):
    """拒绝访问异常"""
    code = 403


class NotFoundException(FuckerTesterException):
    """资源缺失异常"""
    code = 404


class UserNotExistException(NotFoundException):
    """用户不存在异常"""
    message = "user %(identity)s does not exist"


class UserAlreadyExistException(ForbiddenException):
    """用户已经存在"""
    message = "user %(identity)s already exist"


class IncorrectPasswordException(UnauthorizedException):
    """密码错误"""
    message = "Incorrect user password"


class MissNecessaryFields(BadRequestException):
    """数据表字段缺失"""
    message = "missing necessary database field: %(field)s"
