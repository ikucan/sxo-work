# -*- coding: utf-8 -*-
import re

from sxo.interface.entities.auto_entities import AccountDetails
from sxo.interface.entities.auto_entities import ClientDetails
from sxo.interface.entities.auto_entities import UserDetails
from sxo.interface.factories import SaxoAPIClientBoundMethodMethodFactory
from sxo.interface.factories import SaxoAPIMethodFactory
from sxo.interface.factories import SaxoAPISubscriptionClientMethodFactory
from sxo.interface.orders import DeleteOrders
from sxo.interface.orders import GetOrderDetails
from sxo.interface.orders import LimitOrder
from sxo.interface.orders import ListAllOrders
from sxo.interface.orders import ModifyOrder
from sxo.interface.prices import InfoPrice
from sxo.interface.streaming import InfoPriceSubscription
from sxo.interface.streaming import InfoMessageSubscription
from sxo.interface.positions import ListPositions
from sxo.interface.reference import RefCountries
from sxo.interface.reference import RefCultures
from sxo.interface.reference import RefCurrencies
from sxo.interface.reference import RefCurrencyPairs
from sxo.interface.reference import RefExchanges
from sxo.interface.reference import RefInstruments
from sxo.interface.rest_base import SaxoRestBase

# from functools import cache


class GetUserInfo(metaclass=SaxoAPIMethodFactory):
    def __call__(
        self,
    ):
        return self.rest_conn._GET_json(api_set="port", endpoint="/users/me", api_ver=1)


class GetClientInfo(metaclass=SaxoAPIMethodFactory):
    def __call__(
        self,
    ):
        return self.rest_conn._GET_json(api_set="port", endpoint="/clients/me", api_ver=1)


class GetAccountsInfo(metaclass=SaxoAPIMethodFactory):
    def __call__(
        self,
    ):
        return self.rest_conn._GET_json(api_set="port", endpoint="/accounts/me", api_ver=1)


class ClientMethodFactory(type):
    def __init__(cls, name, bases, namespace, **kwargs):
        if not hasattr(cls, "_methods"):
            cls._methods = {}


class SaxoClient(metaclass=ClientMethodFactory):
    _methods = {
        "user_details": GetUserInfo,
        "client_details": GetClientInfo,
        "account_details": GetAccountsInfo,
        "countries": RefCountries,
        "cultures": RefCultures,
        "currencies": RefCurrencies,
        "currency_pairs": RefCurrencyPairs,
        "exchanges": RefExchanges,
        "instruments": RefInstruments,
        # pricing
        "info_price": InfoPrice,
        # subscriptions
        "subscribe_price": InfoPriceSubscription,
        "subscribe_messages": InfoMessageSubscription,
        # orders
        "limit_order": LimitOrder,
        "order_details": GetOrderDetails,
        "list_orders": ListAllOrders,
        "delete_orders": DeleteOrders,
        "modify_order": ModifyOrder,
        # positions
        "all_positions": ListPositions,
    }

    def __init__(
        self,
        *,
        url_base: str = "https://gateway.saxobank.com/sim/openapi",
        token_file: str = "/tmp/saxo_token",
    ):
        self.rest_helper = SaxoRestBase(url_base=url_base, token_file=token_file)
        self.user_info = UserDetails(self.user_details())  # type: ignore
        self.client_info = ClientDetails(self.client_details())  # type: ignore
        self.account_info = AccountDetails(self.account_details())  # type: ignore

    def __getattr__(self, attr: str):
        if attr in self._methods:
            if type(self._methods[attr]) == SaxoAPISubscriptionClientMethodFactory:
                self._methods[attr] = self.__make_callable_for_a_subscription(attr)
            elif type(self._methods[attr]) == SaxoAPIClientBoundMethodMethodFactory:
                self._methods[attr] = self.__make_callable_for_client_bound_method(attr)
            elif type(self._methods[attr]) == SaxoAPIMethodFactory:
                self._methods[attr] = self.__make_callable_for_method(attr)
            elif type(self._methods[attr]) == type:
                self._methods[attr] = self.__make_callable_for_method(attr)

            return self._methods[attr]
        else:
            raise AttributeError(f"'{type(self)}' has no atribute '{attr}'")

    def __make_callable_for_method(self, method: str):
        #
        # construct and return method for object
        # self.client_info
        if re.match("^.*$", method):
            return self._methods[method](self.rest_helper)  # type: ignore

        raise AttributeError(f"'{type(self)}' dont know how to make '{method}'")

    def __make_callable_for_client_bound_method(self, method: str):
        #
        # construct and return method for object
        # self.client_info
        account_key = self.account_info.Data()[0]["AccountKey"]  # type: ignore
        client_key = self.client_info.ClientKey()  # type: ignore
        if re.match("^.*$", method):
            return self._methods[method](self.rest_helper, account_key, client_key)  # type: ignore

        raise AttributeError(f"'{type(self)}' dont know how to make '{method}'")

    def __make_callable_for_a_subscription(self, method: str):
        #
        if re.match("^.*$", method):
            # context_id = secrets.token_urlsafe(16)
            # reference_id = secrets.token_urlsafe(8)
            return self._methods[method](self.rest_helper)  # type: ignore

        raise AttributeError(f"'{type(self)}' dont know how to make '{method}'")
