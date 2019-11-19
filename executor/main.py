# !/usr/bin/env python
# -*- coning: utf-8 -*-
"""
executor项目入口文件
"""
import logging
from functools import partial

import click
from flask import Flask

from executor.common.config import Manage, IpAddressParamType, PortParamType
from executor.api.register import register_resource

LOG = logging.getLogger(__name__)
# 将click.option转换为偏函数，强制添加两个默认参数
OPTION = partial(click.option, show_default=True, show_envvar=True)


@click.command(name="fucker-executor")
@OPTION(
    "--host",
    required=True,
    default="0.0.0.0",
    type=IpAddressParamType(),
    envvar="FUCKER_EXECUTOR_HOST",
    help="set host"
)
@OPTION(
    "--port",
    required=True,
    default=5050,
    type=PortParamType(),
    envvar="FUCKER_EXECUTOR_PORT",
    help="set port"
)
@OPTION(
    "--database-port",
    required=True,
    default=3306,
    type=PortParamType(),
    help="set database port"
)
@OPTION(
    "--debug",
    default=False,
    is_flag=True,
    flag_value=True,
    envvar="FUCKER_EXECUTOR_DEBUG",
    help="enable debug mode",
    type=click.BOOL
)
@OPTION(
    "--log-file",
    default="/var/log/fucker/executor.log",
    envvar="FUCKER_EXECUTOR_LOG_FILE",
    type=click.types.Path(),
    help="log file path",
)
@OPTION(
    "--database-username",
    default="root",
    help="database username",
    required=True,
)
@OPTION(
    "--database-host",
    default="127.0.0.1",
    help="database host",
    required=True,
)
@OPTION(
    "--database-password",
    required=False,
    help="database password"
)
def main(**kwargs):
    """
    程序入口，返回配置参数到单例类 Manage, LogConfig类接收debug状态，如果
    状态为True, 则日志系统会设置为 debug级别输入，否则默认为 INFO
    """
    app = Flask(__name__)
    conf = Manage()
    conf.update_config_items(**kwargs)
    conf.setup_log()
    LOG.info("start server on host: %s, port :%s", conf.host, conf.port)
    register_resource(app)
    app.run(conf.host, conf.port)


if __name__ == "__main__":
    main()
