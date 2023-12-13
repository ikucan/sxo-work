# -*- coding: utf-8 -*-
from pprint import pprint
from typing import Dict
from sxo.om.positions import Position
from sxo.om.manager import Manager
from sxo.om.orders import Order

class Monitor:

    def __init__(self, om:Manager = None):
        if om:
            self._om = om
        else:
            self._om = Manager()


    def scan(self,):
        '''
        - scan all positions and find all Open positions
        - filter those with open orders
        '''
        self._om.refresh_orders()
        net_positions = self._om.net_positions()
        pos_with_open_stops  = []
        for _, net_pos in net_positions.items():
            positions = net_pos.get_positions()
            pos_with_open_stops += [p for p in positions if p.has_stop() ]

        for pos_wos in pos_with_open_stops:
            self.adjust_open_stop(pos_wos)

    def adjust_open_stop(self, position:Position):
        # if a position is making money
        if position.pnl() > 0:
            live_price = position.current_price()
            open_price = position.open_price()

            stop_order = position.related_open_stop()
            stop_price = stop_order.price()

            price_return = abs(open_price - live_price)
            min_abs_stop_offset = price_return * 0.6666

            if position.is_short():
                target_stop_price = open_price - min_abs_stop_offset
                if target_stop_price < stop_price:
                    self._om.modify_order_by_id(
                        stop_order.id(),
                        target_stop_price
                    )
                    i = 123
            else:
                target_stop_price = open_price - min_abs_stop_offset 
            

        i = 123


if __name__ == "__main__":
    mon = Monitor()

    mon.scan()

