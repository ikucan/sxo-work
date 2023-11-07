# -*- coding: utf-8 -*-
from pprint import pprint
import time

from typing import Dict
from typing import Any
from typing import List

from sxo.util.json_utils import JsonWrapperBase
from sxo.interface.entities.instruments.symbology import Instrument
from sxo.interface.entities.instruments.symbology import InstrumentUtil

class PositionError(Exception):
    pass



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
        self.must_have('SourceOrderId')
        self.must_have('SpotDate')
        self.must_have('Status')
        self.must_have('Uic')
        self.must_have('ValueDate')
        asset_type = _json['AssetType']

        self._instrument = InstrumentUtil.find(_json['Uic'])
        self._related_orders = _json['RelatedOpenOrders']

                  

class Position(JsonWrapperBase):
    '''
    an individual position, with related orders
    '''
    def __init__(self, _json: Dict[Any, Any]):
        super().__init__(_json)
        self.must_have('NetPositionId')
        self.must_have('PositionId')
        self.must_have('PositionBase')
        self.must_have('PositionView')
        self._base = PositionBase(self._json['PositionBase'])

    def net_position_id(self,) -> str:
        return self._json['NetPositionId']


class NetPosition(JsonWrapperBase):
    @staticmethod
    def parse(_json: Dict[Any, Any]):
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

        i = 123
        
    
    '''
    a netted position. 
    '''
    def __init__(self, _json: Dict[Any, Any]):
        # store the actual json
        self._json = _json

        pass


from sxo.interface.client import SaxoClient

if __name__ == "__main__":

    # client = SaxoClient(token_file="/data/saxo_token")
    # positions = client.all_positions()
    import json
    f=open('tmp_pos.json', 'r')
    positions_str = f.read()
    positions = json.loads(positions_str)
    f.close()
    pprint(positions)
    np = NetPosition.parse(positions)

