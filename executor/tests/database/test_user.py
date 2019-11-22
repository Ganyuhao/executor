#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""user表测试"""
from executor.database.models.user import Users
from executor.tests.database.base import DatabaseTestCase
from executor.exceptions import UserAlreadyExistException, \
    IncorrectPasswordException


class TestOperatorUser(DatabaseTestCase):
    data_file_path = "database_user_data.yaml"

    def test_create_user(self):
        user = Users.from_json(self.get_test_date("test_create_user"))
        new_user = self.db.create_user(self.context, user)
        self.assertIsInstance(new_user, Users)
        self.db.delete_user(self.context, new_user.id, new_user.password)

    def test_create_same_name_user(self):
        user1 = Users.from_json(
            self.get_test_date(
                "test_create_same_name_user", "test_create_same_name_user1"))
        user2 = Users.from_json(
            self.get_test_date(
                "test_create_same_name_user", "test_create_same_name_user2"))
        self.db.create_user(self.context, user1)
        self.assertRaises(UserAlreadyExistException,
                          self.db.create_user, self.context, user2)
        self.db.delete_user(self.context, user1.phone, user1.password)

    def test_create_same_phone_user(self):
        user1 = Users.from_json(
            self.get_test_date(
                "test_create_same_phone_user", "test_create_same_phone_user1"
            ))
        user2 = Users.from_json(
            self.get_test_date(
                "test_create_same_phone_user", "test_create_same_phone_user2"
            ))
        self.db.create_user(self.context, user1)
        self.assertRaises(UserAlreadyExistException,
                          self.db.create_user, self.context, user2)
        self.db.delete_user(self.context, user1.phone, user1.password)

    def test_get_user_by_id(self):
        user = Users.from_json(
            self.get_test_date("test_get_user_by_id")
        )
        n_user = self.db.create_user(self.context, user)
        self.assertEqual(
            n_user,
            self.db.get_user(self.context, user.id, user.password))
        self.db.delete_user(self.context, n_user.id, n_user.password)

    def test_get_user_by_user_id(self):
        user = Users.from_json(
            self.get_test_date("test_get_user_by_user_id")
        )
        n_user = self.db.create_user(self.context, user)
        self.assertEqual(
            n_user,
            self.db.get_user(self.context, user.user_id, user.password))
        self.db.delete_user(self.context, n_user.user_id, n_user.password)

    def test_get_user_by_name(self):
        user = Users.from_json(
            self.get_test_date("test_get_user_by_name")
        )
        n_user = self.db.create_user(self.context, user)
        self.assertEqual(
            n_user,
            self.db.get_user(self.context, user.username, user.password))
        self.db.delete_user(self.context, n_user.username, n_user.password)

    def test_get_user_by_phone(self):
        user = Users.from_json(
            self.get_test_date("test_get_user_by_phone")
        )
        n_user = self.db.create_user(self.context, user)
        self.assertEqual(
            n_user,
            self.db.get_user(self.context, user.phone, user.password))
        self.db.delete_user(self.context, n_user.phone, n_user.password)

    def test_get_user_with_incorrect_password(self):
        user = Users.from_json(
            self.get_test_date("test_get_user_with_incorrect_password")
        )
        n_user = self.db.create_user(self.context, user)
        self.assertRaises(
            IncorrectPasswordException,
            self.db.get_user, self.context, n_user.phone,
            n_user.password + "_"
        )
        self.db.delete_user(self.context, n_user.id, n_user.password)
