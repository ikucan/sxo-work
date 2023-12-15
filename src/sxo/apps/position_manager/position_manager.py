# -*- coding: utf-8 -*-
from pprint import pprint
from typing import Dict
from sxo.om.positions import Position
from sxo.om.manager import Manager
from sxo.om.orders import Order

from math import floor
from math import log10

def round_sig(x, sig=100):
    if x == 0:
        return 0
    else:
        return round(x, sig-int(floor(log10(abs(x))))-1)
    
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
            instrument_def = self._om.get_instrument_def(position.uic())
            live_price = position.current_price()
            open_price = position.open_price()

            stop_order = position.related_open_stop()
            current_stop_price = stop_order.price()

            price_return = abs(open_price - live_price)

            if position.is_short():
                ik_pnl = abs(live_price - open_price) / open_price * 100
                min_abs_stop_offset = price_return * 0.6666
                target_stop_price = open_price - min_abs_stop_offset
                rounded_stop_price =int(target_stop_price/instrument_def.tick_size()) * instrument_def.tick_size()
                rounded_stop_price = round_sig(rounded_stop_price, 7)
                if target_stop_price < current_stop_price:
                    print(f"moving spot for SHORT {instrument_def.symbol()} position from {current_stop_price} to {target_stop_price}")
                    self._om.modify_order_by_id(
                        stop_order.id(),
                        rounded_stop_price
                    )

            else:
                ik_pnl = abs(live_price - open_price) / open_price * 100
                min_abs_stop_offset = price_return * 0.6666
                target_stop_price = open_price + min_abs_stop_offset 
                rounded_stop_price =int(target_stop_price/instrument_def.tick_size()) * instrument_def.tick_size()
                rounded_stop_price = round_sig(rounded_stop_price, 7)
                if target_stop_price > current_stop_price:
                    print(f"moving spot for LONG {instrument_def.symbol()} position from {current_stop_price} to {target_stop_price}")
                    self._om.modify_order_by_id(
                        stop_order.id(),
                        rounded_stop_price
                    )


        i = 123


if __name__ == "__main__":
    import time

    mon = Monitor()
    while 1 < 2:
        try:
            mon.scan()
        except Exception as e:
            print(e)

        time.sleep(10)

