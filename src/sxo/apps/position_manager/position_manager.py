# -*- coding: utf-8 -*-
import json
from pprint import pprint
import time
from sxo.interface.entities.om.positions import *
from sxo.interface.client import SaxoClient
from sxo.apps.simple.persisted_quote import RedisQuote
import numpy as np

class Monitor:

    def __init__(self,):
        self._tick_dbs = {}

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


            for open_pos in open_positions:
                pos_instr = open_pos.instrument()
                instr_name = pos_instr.canonical_symbol()
                roos = open_pos.related_open_orders()
                for roo in roos:
                    if instr_name not in orders_by_instr:
                        orders_by_instr[instr_name] = []
                    orders_by_instr[instr_name].append(roo)

        self.adjust(roos, pos_instr)
        i = 123

    def get_prices(self, instr):
        instr_name = instr.canonical_symbol()
        if instr_name not in self._tick_dbs:
            self._tick_dbs[instr_name] = RedisQuote(instr)

        return self._tick_dbs[instr_name]


    def adjust(self, order, instrument):
        price = self.get_prices(instrument)
        i = 123


if __name__ == "__main__":
    mon = Monitor()

    # client = SaxoClient(token_file="/data/saxo_token")
    # positions = client.all_positions()
    f=open('samples/positions/net_pos_example.json', 'r')
    positions_str = f.read()
    positions = json.loads(positions_str)
    f.close()
    #pprint(positions)
    net_pos = NetPosition.parse(positions)
    mon.scan(net_pos)

