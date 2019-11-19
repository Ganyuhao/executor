#!/usr/bin/env python
# -*- coding: utf-8 -*-
from executor.api.base import Restful

from executor.exceptions import MissNecessaryFields


class Users(Restful):
    rule = "users"

    def get(self):
        """list users"""
        raise MissNecessaryFields(field="unknown")
