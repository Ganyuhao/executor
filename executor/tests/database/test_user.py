#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from datetime import datetime

from executor.database.models.user import Users
from executor.tests.database.base import DatabaseTestCase
from executor.exceptions import UserAlreadyExistException, \
    IncorrectPasswordException


class TestOperatorUser(DatabaseTestCase):
    data_file_path = "database_user_data.yaml"

    def _convert_to_model(self, json_data):
        return Users(
            name=json_data.get("name"),
            password=str(json_data.get("password")),
            role=json_data.get("role"),
            phone=json_data.get("phone"),
            gender=json_data.get("gender"),
            create_at=datetime.now(),
            avatar=json_data.get("avatar"),
            enabled=json_data.get("enabled"),
            access_token=json_data.get("access_token"),
            extra=json.dumps(json_data.get("extra"))
        )

    def test_create_user(self):
        user = self._convert_to_model(self.get_test_date("test_create_user"))
        new_user = self.db.create_user(self.context, user)
        self.assertIsInstance(new_user, Users)
        self.db.delete_user(self.context, new_user.id, new_user.password)

    def test_create_same_name_user(self):
        user1 = self._convert_to_model(
            self.get_test_date(
                "test_create_same_name_user", "test_create_same_name_user1"
            )
        )
        user2 = self._convert_to_model(
            self.get_test_date(
                "test_create_same_name_user", "test_create_same_name_user2"
            )
        )
        self.db.create_user(self.context, user1)
        self.assertRaises(UserAlreadyExistException,
                          self.db.create_user, self.context, user2)
        self.db.delete_user(self.context, user1.phone, user1.password)

    def test_create_same_phone_user(self):
        user1 = self._convert_to_model(
            self.get_test_date(
                "test_create_same_phone_user", "test_create_same_phone_user1"
            )
        )
        user2 = self._convert_to_model(
            self.get_test_date(
                "test_create_same_phone_user", "test_create_same_phone_user2"
            )
        )
        self.db.create_user(self.context, user1)
        self.assertRaises(UserAlreadyExistException,
                          self.db.create_user, self.context, user2)
        self.db.delete_user(self.context, user1.phone, user1.password)

    def test_get_user_by_id(self):
        user = self._convert_to_model(
            self.get_test_date("test_get_user_by_id")
        )
        n_user = self.db.create_user(self.context, user)
        self.assertEqual(
            n_user,
            self.db.get_user(self.context, user.id, user.password))
        self.db.delete_user(self.context, n_user.id, n_user.password)

    def test_get_user_by_name(self):
        user = self._convert_to_model(
            self.get_test_date("test_get_user_by_name")
        )
        n_user = self.db.create_user(self.context, user)
        self.assertEqual(
            n_user,
            self.db.get_user(self.context, user.name, user.password))
        self.db.delete_user(self.context, n_user.name, n_user.password)

    def test_get_user_by_phone(self):
        user = self._convert_to_model(
            self.get_test_date("test_get_user_by_phone")
        )
        n_user = self.db.create_user(self.context, user)
        self.assertEqual(
            n_user,
            self.db.get_user(self.context, user.phone, user.password))
        self.db.delete_user(self.context, n_user.phone, n_user.password)

    def test_get_user_with_incorrect_password(self):
        user = self._convert_to_model(
            self.get_test_date("test_get_user_with_incorrect_password")
        )
        n_user = self.db.create_user(self.context, user)
        self.assertRaises(
            IncorrectPasswordException,
            self.db.get_user, self.context, n_user.phone,
            n_user.password + "_"
        )
        self.db.delete_user(self.context, n_user.id, n_user.password)
