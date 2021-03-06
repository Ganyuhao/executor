#!/usr/bin/env python
# -*- coding: utf-8 -*-
from executor.common.policy import enforce
from executor.common.constant import Roles
from executor.common.context import Context
from executor.database.models.user import Users
from executor.tests.base import TestCase
from executor.exceptions import AccessDeniedException


class FakeRequest:
    pass


class Faker:

    @enforce(Roles.admin)
    def admin_only(self, req):
        return True

    @enforce(Roles.vip)
    def vip_only(self, req):
        return True

    @enforce(Roles.member)
    def member_only(self, req):
        return True

    @enforce()
    def guest_api(self, req):
        return True


class TestPolicyVerify(TestCase):

    def setUp(self):
        self.resource = Faker()
        self.admin_req = self.make_request(Roles.admin)
        self.vip_req = self.make_request(Roles.vip)
        self.member_req = self.make_request(Roles.member)
        self.guest_req = self.make_request(Roles.guest)
        self.none_req = self.make_request(None, False)

    @staticmethod
    def make_request(role, user=True):
        fake_req = FakeRequest()
        fake_req.ctx = Context(
            fake_req, None, Users(role=role) if user else None)
        return fake_req

    def test_admin_only(self):
        self.assertRaises(
            AccessDeniedException, self.resource.admin_only, self.vip_req)
        self.assertRaises(
            AccessDeniedException, self.resource.admin_only, self.member_req)
        self.assertRaises(
            AccessDeniedException, self.resource.admin_only, self.guest_req)
        self.assertRaises(
            AccessDeniedException, self.resource.admin_only, self.none_req)
        self.assertTrue(self.resource.admin_only(self.admin_req))

    def test_vip_only(self):
        self.assertRaises(
            AccessDeniedException, self.resource.vip_only, self.member_req)
        self.assertRaises(
            AccessDeniedException, self.resource.vip_only, self.guest_req)
        self.assertRaises(
            AccessDeniedException, self.resource.vip_only, self.none_req)
        self.assertTrue(self.resource.vip_only(self.vip_req))
        self.assertTrue(self.resource.vip_only(self.admin_req))

    def test_member_only(self):
        self.assertRaises(
            AccessDeniedException, self.resource.member_only, self.guest_req)
        self.assertRaises(
            AccessDeniedException, self.resource.member_only, self.none_req)
        self.assertTrue(self.resource.member_only(self.member_req))
        self.assertTrue(self.resource.member_only(self.vip_req))
        self.assertTrue(self.resource.member_only(self.admin_req))

    def test_guest_only(self):
        self.assertTrue(self.resource.guest_api(self.none_req))
        self.assertTrue(self.resource.guest_api(self.guest_req))
        self.assertTrue(self.resource.guest_api(self.member_req))
        self.assertTrue(self.resource.guest_api(self.vip_req))
        self.assertTrue(self.resource.guest_api(self.admin_req))
