# !/usr/bin/env python
# -*- coning: utf-8 -*-
"""
executor项目入口文件
"""
from functools import partial

import click

from executor.manage.config import Manage, IpAddressParamType, PortParamType

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
    "--debug",
    required=False,
    is_flag=True,
    flag_value=True,
    envvar="FUCKER_EXECUTOR_DEBUG",
    help="enable debug mode",
    type=click.BOOL
)
def main(**kwargs):
    """程序入口，返回配置参数到单例类 Manage"""
    Manage(**kwargs)


if __name__ == '__main__':
    main()
