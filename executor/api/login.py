# !/usr/bin/env python
# coding: utf-8
# @Time     : 2019/11/26 13:03
# @Author   : Mr.Gan
# Software  : PyCharm
"""登录 API """

from executor.api.base import Restful


class Login(Restful):
    """login api"""
    rule = "login"

    # 扩充父级解析器
    parser = Restful.parser.copy()
    # 参数解析
    parser.add_argument("username", required=True, type=str)
    parser.add_argument("password", required=True, type=str)

    def post(self, req):
        """登录"""
        args = self.parser.parse_args()
        username = args.get("username")
        password = args.get("password")
        ctx = req.ctx
        user_data = ctx.db_base.get_user(
            ctx, username, password
        )
        return "成功", 200, {"X-AUTH-TOKEN": user_data.token}
