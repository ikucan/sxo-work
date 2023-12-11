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

    def scan(self, net_positions):
        '''
        - scan all positions and find all Open positions
        - filter those with open orders
        '''
        pos_with_open_stops  = []
        for _, net_pos in net_positions.items():
            positions = net_pos.get_positions()
            pos_with_open_stops += [p for p in positions if p.has_stop() ]

        for pos_wos in pos_with_open_stops:
            self.adjust_open_stop(pos_wos)

    def adjust_open_stop(self, position:Position):
        # if a position is making money
        if position.pnl() > 0:
            price = position.current_price()
            stop_order = position.related_open_stop()

        i = 123

        #     for open_pos in pos_with_open_orders:
        #         pos_instr = open_pos.instrument()
        #         uid = pos_instr.uid()
        #         roos = open_pos.related_open_orders()
        #         for roo in roos:
        #             if uid not in orders_by_instr:
        #                 orders_by_instr[uid] = []
        #             orders_by_instr[uid].append(roo)

        # self.adjust(orders_by_instr)


    # def get_prices(self, instr):
    #     instr_name = instr.canonical_symbol()
    #     if instr_name not in self._tick_dbs:
    #         self._tick_dbs[instr_name] = RedisQuote(instr)

    #     return self._tick_dbs[instr_name]
    #     for uid, orders in orders_by_instr.items():
    #         instrument = InstrumentUtil.find(uid)
    #         print(f"adjusting orders for {str(instrument)}")
    #         price = self.get_prices(instrument)


    # def adjust(self, orders_by_instr):
    #     for uid, orders in orders_by_instr.items():
    #         instrument = InstrumentUtil.find(uid)
    #         print(f"adjusting orders for {str(instrument)}")
    #         price = self.get_prices(instrument)
            
    #         i = 123


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

