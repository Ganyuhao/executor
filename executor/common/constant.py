# !/usr/bin/env python
# coding: utf-8
# @Time     : 2019/11/21 17:40
# @Author   : Mr.Gan
# Software  : PyCharm

"""常量存放"""


class Roles:
    """role define"""
    admin = "admin"
    vip = "vip"
    member = "member"
    guest = "guest"

    # priority of roles
    _priority_ = (admin, vip, member, guest)

    @classmethod
    def contains(cls, role):
        """is there a role definition"""
        return role in cls._priority_

    @classmethod
    def permission_check(cls, role, required):
        """ASD(Access )"""
        assert cls.contains(role)
        assert cls.contains(required)
        return cls._priority_.index(role) <= cls._priority_.index(required)
