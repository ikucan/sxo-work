# -*- coding: utf-8 -*-
from typing import List
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


class RefInstrumentDetails(metaclass=SaxoAPIClientBoundMethodMethodFactory):
    '''
    TBD!:
    https://www.developer.saxo/openapi/referencedocsoas/refoas/v1/instruments/get__ref__details_uic_assettype

    GET https://gateway.saxobank.com/sim/openapi/ref/v1/instruments/details/{Uic}/{AssetType}?AccountKey={AccountKey}&ClientKey={ClientKey}&FieldGroups={FieldGroups}
    '''
    def __call__(
        self,
        uic: int,
        asset_type:str,
        field_groups: str | List[str] = None,  # noqa:B006
    ):
        account_key = self.account_key  # type: ignore
        client_key = self.client_key  # type: ignore

        endpoint = f"/instruments/details/{uic}/{asset_type}?AccountKey={account_key}&ClientKey={client_key}"
        if field_groups:
            endpoint = endpoint + f"&FieldGroups={','.joint(field_groups)}"

        return self.rest_conn._GET_json(api_set="ref", endpoint=endpoint, api_ver=1)  # type: ignore
