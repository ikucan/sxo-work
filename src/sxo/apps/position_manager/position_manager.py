# -*- coding: utf-8 -*-
import json
from pprint import pprint
import time
from sxo.interface.entities.om.positions import *
from sxo.interface.client import SaxoClient
from sxo.apps.simple.persisted_quote import RedisQuote
from sxo.interface.entities.instruments.symbology import InstrumentUtil
import numpy as np

class Monitor:

    def __init__(self,):
        self._tick_dbs = {}
        self._PRICE_HISTORY_WINDOW = np.timedelta64(30 * 60, "s")

    def scan(self, net_pos):
        '''
        - scan all positions and find all Open positions
        - for each open position find all (usually 1) related open orders
        - group by instrument - assuming we will apply same adjustment per instrument
        - adjust
        '''
        orders_by_instr = {}
        for net_pos_name, pos in net_pos.items():
            positions = pos.get_positions()
            open_positions = [p for p in positions if p.status() == 'Open']
            pos_with_open_orders = [p for p in open_positions if len(p.related_open_orders()) > 0]

            for open_pos in pos_with_open_orders:
                pos_instr = open_pos.instrument()
                uid = pos_instr.uid()
                roos = open_pos.related_open_orders()
                for roo in roos:
                    if uid not in orders_by_instr:
                        orders_by_instr[uid] = []
                    orders_by_instr[uid].append(roo)

        self.adjust(orders_by_instr)
        i = 123

    def get_prices(self, instr):
        instr_name = instr.canonical_symbol()
        if instr_name not in self._tick_dbs:
            self._tick_dbs[instr_name] = RedisQuote(instr)

        return self._tick_dbs[instr_name]


    def adjust(self, orders_by_instr):
        for uid, orders in orders_by_instr.items():
            instrument = InstrumentUtil.find(uid)
            print(f"adjusting orders for {str(instrument)}")
            price = self.get_prices(instrument)
            
            i = 123


if __name__ == "__main__":
    mon = Monitor()

    # client = SaxoClient(token_file="/data/saxo_token")
    # positions = client.all_positions()
    # with open('samples/positions/net_pos_example.json', 'w') as f:
    #     f.write(json.dumps(positions))
    with open('samples/positions/net_pos_example.json', 'r') as f:
        positions_str = f.read()    
    positions = json.loads(positions_str)
    #pprint(positions)
    net_pos = NetPosition.parse(positions)
    mon.scan(net_pos)

