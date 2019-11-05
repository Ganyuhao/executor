#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

from executor.database.models.user import Users
from executor.tests.database.base import DatabaseTestCase
from executor.exceptions import UserAlreadyExistException, \
    IncorrectPasswordException


class TestOperatorUser(DatabaseTestCase):

    def test_create_user(self):
        user = Users(
            name="test_create_user",
            password="123456",
            role="admin",
            phone="01234567891",
            gender="man",
            create_at=datetime.now(),
            avatar="/path/test_create_user/avatar.jpg",
            enabled=True,
            access_token="faker_token",
            extra="{\"email\":\"emaill\"}"
        )
        new_user = self.db.create_user(self.context, user)
        self.assertIsInstance(new_user, Users)
        self.db.delete_user(self.context, new_user.id, new_user.password)

    def test_create_same_name_user(self):
        user1 = Users(
            name="test_create_same_name_user",
            password="123456",
            role="admin",
            phone="01234567892",
            gender="man",
            create_at=datetime.now(),
            avatar="/path/test_create_same_name_user/avatar.jpg",
            enabled=True,
            access_token="faker_token",
            extra="{\"email\":\"emaill\"}"
        )
        user2 = Users(
            name="test_create_same_name_user",
            password="123456",
            role="admin",
            phone="01234567893",
            gender="man",
            create_at=datetime.now(),
            avatar="/path/test_create_same_name_user/avatar.jpg",
            enabled=True,
            access_token="faker_token",
            extra="{\"email\":\"emaill\"}"
        )
        self.db.create_user(self.context, user1)
        self.assertRaises(UserAlreadyExistException,
                          self.db.create_user, self.context, user2)
        self.db.delete_user(self.context, user1.phone, user1.password)

    def test_create_same_phone_user(self):
        user1 = Users(
            name="test_create_same_phone_user1",
            password="123456",
            role="admin",
            phone="01234567894",
            gender="man",
            create_at=datetime.now(),
            avatar="/path/test_create_same_name_user/avatar.jpg",
            enabled=True,
            access_token="faker_token",
            extra="{\"email\":\"emaill\"}"
        )
        user2 = Users(
            name="test_create_same_phone_user2",
            password="123456",
            role="admin",
            phone="01234567894",
            gender="man",
            create_at=datetime.now(),
            avatar="/path/test_create_same_name_user/avatar.jpg",
            enabled=True,
            access_token="faker_token",
            extra="{\"email\":\"emaill\"}"
        )
        self.db.create_user(self.context, user1)
        self.assertRaises(UserAlreadyExistException,
                          self.db.create_user, self.context, user2)
        self.db.delete_user(self.context, user1.phone, user1.password)

    def test_get_user_by_id(self):
        user = Users(
            name="test_get_user_by_id",
            password="123456",
            role="admin",
            phone="01234567895",
            gender="man",
            create_at=datetime.now(),
            avatar="/path/test_get_user_by_id/avatar.jpg",
            enabled=True,
            access_token="faker_token",
            extra="{\"email\":\"emaill\"}"
        )
        n_user = self.db.create_user(self.context, user)
        self.assertEqual(
            n_user,
            self.db.get_user(self.context, user.id, user.password))
        self.db.delete_user(self.context, n_user.id, n_user.password)

    def test_get_user_by_name(self):
        user = Users(
            name="test_get_user_by_name",
            password="123456",
            role="admin",
            phone="01234567896",
            gender="man",
            create_at=datetime.now(),
            avatar="/path/test_get_user_by_name/avatar.jpg",
            enabled=True,
            access_token="faker_token",
            extra="{\"email\":\"emaill\"}"
        )
        n_user = self.db.create_user(self.context, user)
        self.assertEqual(
            n_user,
            self.db.get_user(self.context, user.name, user.password))
        self.db.delete_user(self.context, n_user.name, n_user.password)

    def test_get_user_by_phone(self):
        user = Users(
            name="test_get_user_by_phone",
            password="123456",
            role="admin",
            phone="01234567897",
            gender="man",
            create_at=datetime.now(),
            avatar="/path/test_get_user_by_phone/avatar.jpg",
            enabled=True,
            access_token="faker_token",
            extra="{\"email\":\"emaill\"}"
        )
        n_user = self.db.create_user(self.context, user)
        self.assertEqual(
            n_user,
            self.db.get_user(self.context, user.phone, user.password))
        self.db.delete_user(self.context, n_user.phone, n_user.password)

    def test_get_user_with_incorrect_password(self):
        user = Users(
            name="test_get_user_with_incorrect_password",
            password="123456",
            role="admin",
            phone="01234567898",
            gender="man",
            create_at=datetime.now(),
            avatar="/path/test_get_user_by_phone/avatar.jpg",
            enabled=True,
            access_token="faker_token",
            extra="{\"email\":\"emaill\"}"
        )
        n_user = self.db.create_user(self.context, user)
        self.assertRaises(
            IncorrectPasswordException,
            self.db.get_user, self.context, n_user.phone,
            n_user.password + "_"
        )
        self.db.delete_user(self.context, n_user.id, n_user.password)
