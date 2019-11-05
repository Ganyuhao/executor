#!/usr/bin/env python
# -*- coding: utf-8 -*-
from executor.common.config import Manage
from executor.tests.base import TestCase


class TestConfigManage(TestCase):

    def test_config_manage_singleton_mode(self):
        self.assertIs(self.conf, Manage())

    def test_config_manage_keys(self):
        for k, v in self.config_items.items():
            if not hasattr(self.conf, k):
                self.fail("key %s setting failed" % k)
            self.assertEqual(getattr(self.conf, k), v)
            self.assertIsInstance(getattr(self.conf, k), type(v))
