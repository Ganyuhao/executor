#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

from executor.database.models.base import Model
from executor.tests.database.base import DatabaseTestCase
from executor.exceptions import MissNecessaryFields

from sqlalchemy import Column, String, Integer, Boolean, DateTime


class UserModel(Model):
    __tablename__ = "fake_table"
    id = Column(Integer, autoincrement=True, primary_key=True, unique=True)
    age = Column(Integer)
    username = Column(String(64), nullable=False, unique=True)
    password = Column(String(32))
    create_at = Column(DateTime, nullable=False)
    update_at = Column(DateTime)
    enabled = Column(Boolean, nullable=False)
    blocked = Column(Boolean)


class TestBaseDataModel(DatabaseTestCase):

    def test_normal_to_json(self):
        expect = {
            "id": 1,
            "age": 5,
            "username": "faker",
            "password": "abc",
            "create_at": datetime.now(),
            "update_at": datetime.now(),
            "enabled": True,
            "blocked": False,
        }
        fm = UserModel(**expect)
        self.assertEqual(expect, fm.to_json())

    def test_normal_from_json(self):
        expect = {
            "id": 1,
            "age": 5,
            "username": "faker",
            "password": "abc",
            "create_at": datetime.now(),
            "update_at": datetime.now(),
            "enabled": True,
            "blocked": False,
        }
        fm = FakeModel.from_json(expect)
        self.assertEqual(expect, fm.to_json())

    def test_miss_arg_required(self):
        err_model = {
            "id": 1,
            "age": 5,
            "password": "abc",
            "create_at": datetime.now(),
            "update_at": datetime.now(),
            "enabled": True,
            "blocked": False,
        }
        self.assertRaises(MissNecessaryFields, FakeModel.from_json, err_model)

    def test_miss_primary_key(self):
        expect = {
            "age": 5,
            "username": "faker",
            "password": "abc",
            "create_at": datetime.now(),
            "update_at": datetime.now(),
            "enabled": True,
            "blocked": False,
        }
        model = FakeModel.from_json(expect)
        expect["id"] = None
        self.assertEqual(expect, model.to_json())

    def test_string_datetime(self):
        expect = {
            "id": 2,
            "age": 5,
            "username": "faker",
            "password": "abc",
            "create_at": "2019-10-12 11:23:25",
            "update_at": datetime.now(),
            "enabled": True,
            "blocked": False,
        }
        model = FakeModel.from_json(expect)
        expect["create_at"] = datetime.strptime(
            "2019-10-12 11:23:25", "%Y-%m-%d %H:%M:%S")
        self.assertEqual(expect, model.to_json())
