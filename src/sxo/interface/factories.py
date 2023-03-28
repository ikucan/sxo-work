# -*- coding: utf-8 -*-
# import re
# from sxo.interface.entities.auto_entities import AccountDetails
# from sxo.interface.entities.auto_entities import ClientDetails
# from sxo.interface.entities.auto_entities import UserDetails
from sxo.interface.rest_base import SaxoRestBase

# from functools import cache


class SaxoAPIMethodFactory(type):
    def __init__(cls, name, bases, namespace, **kwargs):
        # override the constructor. (defaiult always exists)
        def constructor(cls, rest_helper: SaxoRestBase):
            cls.rest_conn = rest_helper

        cls.__init__ = constructor


class SaxoAPIClientBoundMethodMethodFactory(SaxoAPIMethodFactory, type):
    def __init__(cls, name, bases, namespace, **kwargs):
        # override the constructor. (defaiult always exists)
        def constructor(self, rest_conn: SaxoRestBase, account_key: str, client_key: str):
            cls.rest_conn = rest_conn
            self.account_key = account_key
            self.client_key = client_key

        cls.__init__ = constructor


class SaxoAPISubscriptionClientMethodFactory(SaxoAPIMethodFactory, type):
    default_field_groups = "Quote,PriceInfoDetails,PriceInfo,MarketDepth"

    def __init__(cls, name, bases, namespace, **kwargs):
        # override the constructor. (defaiult always exists)
        def constructor(self, rest_conn: SaxoRestBase):
            cls.rest_conn = rest_conn

        cls.__init__ = constructor
