# -*- coding: utf-8 -*-
import json
from pprint import pprint
import time
from sxo.interface.entities.om.positions import *
from sxo.interface.client import SaxoClient


if __name__ == "__main__":
    # client = SaxoClient(token_file="/data/saxo_token")
    # positions = client.all_positions()
    f=open('samples/positions/net_pos_example.json', 'r')
    positions_str = f.read()
    positions = json.loads(positions_str)
    f.close()
    #pprint(positions)
    np = NetPosition.parse(positions)
    for k,v in np.items():
        pprint(v.toJson())


