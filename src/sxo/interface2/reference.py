# -*- coding: utf-8 -*-
from sxo.interface.factories import SaxoAPIClientBoundMethodMethodFactory
from sxo.interface.factories import SaxoAPIMethodFactory


class RefCountries(metaclass=SaxoAPIMethodFactory):
    def __call__(
        self,
    ):
        return self.rest_conn._GET_json(api_set="ref", endpoint="/countries", api_ver=1)


class RefCultures(metaclass=SaxoAPIMethodFactory):
    def __call__(
        self,
    ):
        return self.rest_conn._GET_json(api_set="ref", endpoint="/cultures", api_ver=1)


class RefCurrencies(metaclass=SaxoAPIMethodFactory):
    def __call__(
        self,
    ):
        return self.rest_conn._GET_json(api_set="ref", endpoint="/currencies", api_ver=1)


class RefExchanges(metaclass=SaxoAPIMethodFactory):
    def __call__(self, top=100000000, skip=0):
        return self.rest_conn._GET_json(api_set="ref", endpoint="/exchanges", api_ver=1)
        # return self.rest_conn._GET_json(api_set="ref", endpoint="/exchanges?$top=1234&$skip=0", api_ver=1)


class RefCurrencyPairs(metaclass=SaxoAPIClientBoundMethodMethodFactory):
    def __call__(
        self,
    ):
        account_key = self.account_key  # type: ignore
        client_key = self.client_key  # type: ignore
        endpoint = f"/currencypairs/?AccountKey={account_key}&ClientKey={client_key}"
        return self.rest_conn._GET_json(api_set="ref", endpoint=endpoint, api_ver=1)


class RefInstruments(metaclass=SaxoAPIClientBoundMethodMethodFactory):
    def __call__(
        self,
        asset_type: str,
    ):
        account_key = self.account_key  # type: ignore
        endpoint = f"/instruments/?$top=1000&$skip=0&AssetTypes={asset_type}&AccountKey={account_key}"
        return self.rest_conn._GET_drain_json(api_set="ref", endpoint=endpoint, api_ver=1)  # type: ignore
