# -*- coding: utf-8 -*-
from pprint import pprint
import time
from enum import Enum

from typing import Dict
from typing import Any
from typing import List

from sxo.util.json_utils import JsonWrapperBase
from sxo.interface.entities.instruments.symbology import InstrumentUtil

class InstrumentError(Exception):
    ...

class Exchange(JsonWrapperBase):
    def __init__(self, _json: Dict[Any, Any]):
        super().__init__(_json)
        self.set_str('CountryCode')
        self.set_str('ExchangeId')
        self.set_str('Name')
        self.set_str('TimeZoneId')

class Format(JsonWrapperBase):
    def __init__(self, _json: Dict[Any, Any]):
        super().__init__(_json)
        self.set_str('Decimals')
        self.set_str('Format')
        self.set_str('OrderDecimals')

class InstrumentDef(JsonWrapperBase):
    def __init__(self, _json: Dict[Any, Any]):
        super().__init__(_json)
        self.set_int('AmountDecimals')
        self.set_str('AssetType')
        self.set_str('CurrencyCode')
        self.set_float('DefaultAmount')
        self.set_float('DefaultSlippage')
        self.set_str('DefaultSlippageType')
        self.set_str('Description')

        self.must_have('Exchange')
        self._exchange = Exchange(_json['Exchange'])
        self.must_have('Format')
        self._format = Format(_json['Format'])

        self.set_timestamp('FxForwardMaxForwardDate')
        self.set_timestamp('FxForwardMinForwardDate')
        self.set_timestamp('FxSpotDate')

        self.set_int('GroupId')
        self.set_float('IncrementSize')

        self.set_bool('IsBarrierEqualsStrike')
        self.set_bool('IsComplex')
        self.set_bool('IsPEAEligible')
        self.set_bool('IsPEASMEEligible')
        self.set_bool('IsRedemptionByAmounts')
        self.set_bool('IsSwitchBySameCurrency')
        self.set_bool('IsTradable')
        self.set_str('LotSizeType')
        self.set_float('MinimumTradeSize')
        self.set_str('NonTradableReason')

        self.must_have('OrderDistances')
        self.must_have('StandardAmounts')
        self.must_have('SupportedOrderTriggerPriceTypes')
        self.must_have('SupportedOrderTypes')

        self.set_str('Symbol')
        self.set_float('TickSize')
        self.set_float('TickSizeLimitOrder')
        self.set_float('TickSizeStopOrder')
    
        self.must_have('TradableAs')
        self.must_have('TradableOn')

        self.set_str('TradingSignals')
        self.set_str('TradingStatus')
        self.set_int('Uic')

    def uic(self,) -> int:
        return self.Uic

    def asset_type(self,) -> str:
        return self.AssetType

    def symbol(self,) -> str:
        return self.Symbol

    def tick_size(self,) -> float:
        return self.TickSize

    def limit_order_tick_size(self,) -> float:
        return self.TickSizeLimitOrder

    def stop_order_tick_size(self,) -> float:
        return self.TickSizeStopOrder

    def __expr__(self,) -> str:
        return f"{self.asset_type}::{self.Symbol}"
    def __str__(self,) -> str:
        return self.__expr__()


# if __name__ == "__main__" :
#     import json
#     with open("instrument_def.json", "r") as f:
#         json_str = f.read()
#     print(json_str) 

#     id = InstrumentDef(json.loads(json_str))


# example JSON
#
# {
#     "AffiliateInfoRequired": false,
#     "AmountDecimals": 6,
#     "AssetType": "FxSpot",
#     "CurrencyCode": "USD",
#     "DefaultAmount": 10000.0,
#     "DefaultSlippage": 0.01,
#     "DefaultSlippageType": "Percentage",
#     "Description": "British Pound/US Dollar",
#     "Exchange": {
#         "CountryCode": "DK",
#         "ExchangeId": "SBFX",
#         "Name": "Inter Bank",
#         "TimeZoneId": "3"
#     },
#     "Format": {
#         "Decimals": 4,
#         "Format": "AllowDecimalPips",
#         "OrderDecimals": 4
#     },
#     "FxForwardMaxForwardDate": "2024-12-19T00:00:00.000000Z",
#     "FxForwardMinForwardDate": "2023-12-15T00:00:00.000000Z",
#     "FxSpotDate": "2023-12-15T00:00:00.000000Z",
#     "GroupId": 0,
#     "IncrementSize": 5000.0,
#     "IsBarrierEqualsStrike": false,
#     "IsComplex": true,
#     "IsPEAEligible": false,
#     "IsPEASMEEligible": false,
#     "IsRedemptionByAmounts": false,
#     "IsSwitchBySameCurrency": false,
#     "IsTradable": true,
#     "LotSizeType": "NotUsed",
#     "MinimumTradeSize": 1000.0,
#     "NonTradableReason": "None",
#     "OrderDistances": {
#         "EntryDefaultDistance": 0.5,
#         "EntryDefaultDistanceType": "Percentage",
#         "LimitDefaultDistance": 0.0,
#         "LimitDefaultDistanceType": "Percentage",
#         "StopLimitDefaultDistance": 5.0,
#         "StopLimitDefaultDistanceType": "Pips",
#         "StopLossDefaultDistance": 50.0,
#         "StopLossDefaultDistanceType": "Pips",
#         "StopLossDefaultEnabled": false,
#         "StopLossDefaultOrderType": "Stop",
#         "TakeProfitDefaultDistance": 50.0,
#         "TakeProfitDefaultDistanceType": "Pips",
#         "TakeProfitDefaultEnabled": false
#     },
#     "StandardAmounts": [
#         10000.0,
#         50000.0,
#         100000.0,
#         250000.0,
#         500000.0,
#         1000000.0,
#         2000000.0,
#         5000000.0,
#         10000000.0,
#         20000000.0
#     ],
#     "SupportedOrderTriggerPriceTypes": [],
#     "SupportedOrderTypes": [
#         "Stop",
#         "TrailingStop",
#         "StopLimit",
#         "Limit",
#         "Market"
#     ],
#     "Symbol": "GBPUSD",
#     "TickSize": 1e-05,
#     "TickSizeLimitOrder": 1e-05,
#     "TickSizeStopOrder": 1e-05,
#     "TradableAs": [
#         "FxSpot",
#         "FxForwards",
#         "FxSwap"
#     ],
#     "TradableOn": [
#         "18286731"
#     ],
#     "TradingSignals": "Allowed",
#     "TradingStatus": "Tradable",
#     "Uic": 31
# }