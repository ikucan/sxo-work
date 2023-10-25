# -*- coding: utf-8 -*-
from pprint import pprint
import time

from typing import Dict
from typing import Any
from typing import List

from sxo.util.json_utils import JsonUtils

class PositionError(Exception):
    pass

class Position(JsonUtils):
    '''
    an individual position, with related orders
    '''
    def __init__(self, _json: Dict[Any, Any]):
        super().__init__(_json)
        self.must_have('NetPositionId')
        self.must_have('PositionBase')

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
        by_net_pos_id  = {p.net_position_id():p for p in all_positions}
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
    client = SaxoClient(token_file="/data/saxo_token")

    positions = client.all_positions()
    pprint(positions)
    np = NetPosition.parse(positions)
