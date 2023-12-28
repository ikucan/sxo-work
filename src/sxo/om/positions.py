# -*- coding: utf-8 -*-
from pprint import pprint
import time

from typing import Dict
from typing import Any
from typing import List

from sxo.util.json_utils import JsonWrapperBase
from sxo.interface.entities.instruments.symbology import InstrumentUtil
from sxo.om.orders import RelatedOrder

class PositionError(Exception):
    ...


class PositionBase(JsonWrapperBase):
    '''
    position base part of the Net Position Json

    '''
    def __init__(self, _json: Dict[Any, Any]):
        super().__init__(_json)

        self.set_int('AccountId')
        self.set_str('AccountKey')
        self.set_float('Amount')
        self.set_str('AssetType')
        self.set_bool('CanBeClosed')
        self.set_int('ClientId')
        self.set_bool('CloseConversionRateSettled')
        self.set_str('CorrelationKey')
        # self.must_have('CorrelationTypes')
        # self.must_have('ExecutionTimeClose')
        self.set_timestamp('ExecutionTimeOpen')
        self.set_bool('IsForceOpen')
        self.set_bool('IsMarketOpen')
        self.set_bool('LockedByBackOffice')
        self.set_float('OpenPrice')
        self.set_float('OpenPriceIncludingCosts')
        self.must_have('RelatedOpenOrders')
        # self.must_have('RelatedPositionId')
        self.set_int('SourceOrderId')
        self.set_date('SpotDate')
        self.set_str('Status')
        self.set_str('Uic')
        self.set_timestamp('ValueDate')

        self._instrument = InstrumentUtil.find(self.Uic)
        self.RelatedOpenOrders = [RelatedOrder(oj) for oj in _json['RelatedOpenOrders']]

class PositionView(JsonWrapperBase):
    '''
    position view part of the Net Position Json

    '''
    def __init__(self, _json: Dict[Any, Any]):
        super().__init__(_json)
        self.set_float('Ask')
        self.set_float('Bid')
        self.set_str('CalculationReliability')
        #self.set_float('ConversionRateCurrent')
        self.set_float('ConversionRateOpen')
        self.set_float('CurrentPrice')
        self.set_float('CurrentPriceDelayMinutes')
        self.set_str('CurrentPriceType')
        self.set_float_if('Exposure')
        self.set_str('ExposureCurrency')
        self.set_float_if('ExposureInBaseCurrency')
        self.set_float('InstrumentPriceDayPercentChange')
        self.set_str('MarketState')
        self.set_float('MarketValue')
        self.set_float_if('MarketValueInBaseCurrency')
        self.set_float('ProfitLossOnTrade')
        self.set_float('ProfitLossOnTradeInBaseCurrency')
        self.set_float('TradeCostsTotal')
        self.set_float('TradeCostsTotalInBaseCurrency')


class Position(JsonWrapperBase):
    '''
    an individual position, with related orders
    '''
    def __init__(self, _json: Dict[Any, Any]):
        super().__init__(_json)
        self.set_str('NetPositionId')
        self.set_int('PositionId')
        self.must_have('PositionBase')
        self.must_have('PositionView')
        self._base = PositionBase(self._json['PositionBase'])
        self._view = PositionView(self._json['PositionView'])


    def account_id(self,) -> str:
        return self._base.AccountId

    def account_key(self,) -> str:
        return self._base.AccountKey
    
    def asset_type(self,) -> str:
        return self._base.AssetType

    def symbol(self,) -> str:
        return self.instrument().symbol()

    def uic(self,) -> str:
        return self._base.Uic

    def net_position_id(self,) -> str:
        return self._json['NetPositionId']

    def instrument(self,) -> str:
        return self._base._instrument

    def status(self,) -> str:
        return self._base.Status

    def open_price(self,) -> str:
        return self._base.OpenPrice

    def is_open(self,) -> bool:
        return self.status() == "Open"

    def is_closed(self,) -> bool:
        return self.status() == "Closed"

    def is_short(self,) -> bool:
        return self._base.Amount < 0

    def size(self,) -> float:
        return self._base.Amount
    
    def current_price(self,) -> float:
        return self._view.CurrentPrice
    def current_price_type(self,) -> str:
        return self._view.CurrentPriceType
    def current_bid(self,) -> float:
        return self._view.Bid
    def current_ask(self,) -> float:
        return self._view.Ask
    def pnl(self,) -> float:
        return self._view.ProfitLossOnTrade
    def exposure(self,) -> float:
        return self._view.Exposure    
    def exposure_ccy(self,) -> str:
        return self._view.ExposureCurrency    
    def conversion_rate(self,) -> float:
        return self._view.ConversionRateCurrent
    def fx(self,) -> float:
        return self.conversion_rate()
    
    def pct_pnl(self,) -> float:
        # percent pnl
        return self._view.ProfitLossOnTrade / self._view.Exposure


    def related_open_orders(self,):
        return self._base.RelatedOpenOrders

    def has_stop(self,) -> bool:
        roos = self.related_open_orders()
        if len(roos) > 0:
            for roo in roos:
                if roo.Status == "Working" and roo.OpenOrderType == "Stop":
                    return True
        return False
    
    def related_open_stop(self,) -> RelatedOrder:
        roos = self.related_open_orders()
        if len(roos) > 0:
            for roo in roos:
                if roo.Status == "Working" and roo.OpenOrderType == "Stop":
                    return roo

        return None


    def __str__(self,) -> str:
        return f"{str(self.instrument())} :: {self.size()}"  
        return pprint(self._json)

class NetPosition(JsonWrapperBase):
    @staticmethod
    def parse(_json: Dict[Any, Any]) -> Dict[str,Any]:
        if "__count" not in _json:
            raise PositionError('ERROR, missing key in initial JSON: __count')
        if "Data" not in _json:
            raise PositionError('ERROR, missing key in initial JSON: Data')
        all_positions = [Position(pj) for pj in _json['Data']]
        by_net_pos_id  = {}
        for pos in all_positions:
            net_pos_id = pos.net_position_id()
            net_pos_list = by_net_pos_id.get(net_pos_id, [])
            net_pos_list.append(pos)
            by_net_pos_id[net_pos_id] = net_pos_list

        return {k:NetPosition(k, v) for k,v in by_net_pos_id.items()}

    
    '''
    a netted position. 
    '''
    def __init__(self, net_pos_id:str, positions: List[Position]):
        # store the actual json
        self._net_position_id = net_pos_id
        self._positions = positions

    def get_positions(self,) -> List[Position] :
        return self._positions

    def toJson(self,):
        return [x._json for x in self._positions]

