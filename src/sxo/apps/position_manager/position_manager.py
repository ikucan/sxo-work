# -*- coding: utf-8 -*-
import itertools
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

        all_positions = list (itertools.chain.from_iterable([x.get_positions() for x in [np[1] for np in net_positions.items()]]))

        # pos_with_open_stops = [p for p in all_positions if p.has_stop()]
        # pos_wo_open_stops = [p for p in all_positions if p.has_stop()]

        for pos in all_positions:
            self.adjust_open_stop(pos)

    def adjust_open_stop(self, position:Position):
        instrument_def = self._om.get_instrument_def(position.uic())
        live_price = position.current_price()
        open_price = position.open_price()
        pos_size = position.size()

        pnl = (live_price - open_price) * pos_size
        exp = open_price * position.size()

        tick_size = instrument_def.tick_size()
        live_price_tick = position.current_price() / tick_size
        open_price_tick = position.open_price() / tick_size
        pos_sign =  1 if position.size() >= 0 else -1
        pnl_tick = (live_price_tick - open_price_tick) * pos_sign
 
        # if a position is making money
        if pnl_tick > 100:
            target_stop_distance = pnl_tick * 0.8
            target_stop_price_tick = int(open_price_tick + target_stop_distance)
            target_stop_price = target_stop_price_tick * tick_size
        

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

