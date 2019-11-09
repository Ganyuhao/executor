#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

from executor.common.context import Context
from executor.database.manage import Database
from executor.database.models.user import Users
from executor.tests.base import TestCase


class DatabaseTestCase(TestCase):
    database_name = "fucker_tester_tests"
    db = None
    context = None

    @classmethod
    def setUpClass(cls):
        super(DatabaseTestCase, cls).setUpClass()
        cls.db = Database(cls.database_name)
        cls.context = Context(
            None,
            cls.db.session(),
            user=Users(
                id=1,
                name="admin",
                password="123456",
                role="admin",
                phone="13525847457",
                gender="man",
                create_at=datetime.now(),
                avatar="/path/admin/avatar.jpg",
                enabled=True,
                access_token="faker_token",
                extra="{\"email\":\"emaill\"}"
            ),
        )

    @classmethod
    def tearDownClass(cls):
        super(DatabaseTestCase, cls).tearDownClass()
        cls.context.session.commit()
        cls.context.session.close()
