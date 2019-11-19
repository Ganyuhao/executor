#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Basic class define"""
import logging

from flask_restful import Resource

from executor.exceptions import FuckerTesterException

LOG = logging.getLogger(__name__)


class Restful(Resource):
    """Restful Controller Base class"""
    rule = None

    @classmethod
    def setup(cls, api, **kwargs):
        """setup Resource to api component"""
        if not cls.rule:
            rule = cls.__name__.lower()
        else:
            rule = cls.rule
        api.add_resource(cls, "/%s/" % rule, **kwargs)
