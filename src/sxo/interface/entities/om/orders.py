# -*- coding: utf-8 -*-
from pprint import pprint
import time

from typing import Dict
from typing import Any
from typing import List

from sxo.util.json_utils import JsonWrapperBase
from sxo.interface.entities.instruments.symbology import InstrumentUtil

class OrderError(Exception):
    ...


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3
    
class OrderDuration:


            # "Duration": {
            #     "DurationType": "GoodTillCancel"
            # },


class Order(JsonWrapperBase):

    '''
    an individual position, with related orders
    '''
    def __init__(self, _json: Dict[Any, Any]):
        super().__init__(_json)
        self.set_int('AccountId')
        self.set_str('AccountKey')
        self.set_str('AdviceNote')
        self.set_float('Amount')
        self.set_float('Ask')
        self.set_float('Bid')
        self.set_str('AssetType')
        self.set_str('BuySell')
        self.set_str('CalculationReliability')
        self.set_int('ClientId')
        self.set_str('ClientKey')
        self.set_str('ClientName')
        self.set_str('ClientNote')
        self.set_str('CorrelationKey')
        self.must_have('CorrelationTypes')
        self.set_float('CurrentPrice')
        self.set_float('CurrentPriceDelayMinutes')
        self.set_str('CurrentPriceType')
        self.set_float('DistanceToMarket')
        #
        # parse nested
        # 
        self.set_float('IpoSubscriptionFee')
        self.set_bool('IsExtendedHoursEnabled')
        self.set_bool('IsForceOpen')
        self.set_bool('IsMarketOpen')
        self.set_float('MarketPrice')
        self.set_str('MarketState')
        self.set_float('MarketValue')
        self.set_str('NonTradableReason')
        self.set_str('OpenOrderType')
        self.set_str('OrderAmountType')
        self.set_int('OrderId')
        self.set_str('OrderRelation')
        self.set_timestamp('OrderTime')
        self.set_float('Price')
        self.set_str('RelatedOpenOrders')
        self.set_int('RelatedPositionId')
        self.set_str('Status')
        self.set_str('TradingStatus')
        self.set_int('Uic')


            # "DisplayAndFormat": {
            #     "Currency": "EUR",
            #     "Decimals": 4,
            #     "Description": "British Pound/Euro",
            #     "Format": "AllowDecimalPips",
            #     "Symbol": "GBPEUR"
            # },
            # "Duration": {
            #     "DurationType": "GoodTillCancel"
            # },
            # "Exchange": {
            #     "Description": "Inter Bank",
            #     "ExchangeId": "SBFX",
            #     "IsOpen": true,
            #     "TimeZoneId": "3"
            # },
  

    def __str__(self,) -> str:
        return pprint(self._json)
    
    @staticmethod
    def parse(_json: Dict[Any, Any]) -> str:
        if "__count" not in _json:
            raise OrderError('ERROR, missing key in initial JSON: __count')
        if "Data" not in _json:
            raise OrderError('ERROR, missing key in initial JSON: Data')
        all_orders = [Order(oj) for oj in _json['Data']]

        pass

import json

if __name__ == "__main__":
    # client = SaxoClient(token_file="/data/saxo_token")
    # positions = client.all_positions()
    f=open('samples/orders/order_example.json', 'r')
    orders_str = f.read()
    f.close()
    order_json = json.loads(orders_str)
    pprint(order_json)
    Order.parse(order_json)
