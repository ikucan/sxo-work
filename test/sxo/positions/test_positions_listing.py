# -*- coding: utf-8 -*-
from pprint import pprint
import time

from typing import Dict
from typing import Any
from typing import List

from sxo.util.json_utils import JsonUtils
from sxo.interface.entities.instruments.symbology import Instrument
from sxo.interface.entities.instruments.symbology import InstrumentUtil

class PositionError(Exception):
    pass



class PositionBase(JsonUtils):
    '''
    position base part of the Net Position Json

       'AccountId': '18286731',
       'AccountKey': 'Rc9wX9gl1UcU6lsbTh1ZRA==',
       'Amount': 99999.0,
       'AssetType': 'FxSpot',
       'CanBeClosed': False,
       'ClientId': '18286731',
       'CloseConversionRateSettled': True,
       'CorrelationKey': '6d40839c-31ba-49d0-af48-28c8e8e631a5',
       'CorrelationTypes': [],
       'ExecutionTimeClose': '2023-10-20T11:44:52.008630Z',
       'ExecutionTimeOpen': '2023-10-25T22:04:11.619853Z',
       'IsForceOpen': False,
       'IsMarketOpen': True,
       'LockedByBackOffice': False,
       'OpenPrice': 1.1459,
       'OpenPriceIncludingCosts': 1.1459573005730057,
       'RelatedOpenOrders': [],
       'RelatedPositionId': '5017201599',
       'SourceOrderId': '5015400879',
       'SpotDate': '2023-10-30',
       'Status': 'Closed',
       'Uic': 3942,
       'ValueDate': '2023-10-30T00:00:00.000000Z'},

    '''
    def __init__(self, _json: Dict[Any, Any]):
        super().__init__(_json)

        self.must_have('AccountId')
        self.must_have('AccountKey')
        self.must_have('Amount')
        self.must_have('AssetType')
        self.must_have('CanBeClosed')
        self.must_have('ClientId')
        self.must_have('CloseConversionRateSettled')
        self.must_have('CorrelationKey')
        # self.must_have('CorrelationTypes')
        # self.must_have('ExecutionTimeClose')
        self.must_have('ExecutionTimeOpen')
        self.must_have('IsForceOpen')
        self.must_have('IsMarketOpen')
        self.must_have('LockedByBackOffice')
        self.must_have('OpenPrice')
        self.must_have('OpenPriceIncludingCosts')
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

                  

class Position(JsonUtils):
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


class NetPosition(JsonUtils):
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

