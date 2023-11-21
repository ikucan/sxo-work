# -*- coding: utf-8 -*-
import time
import os
import numpy as np
import pandas as pd

from math import log10, floor

from typing import Any
from typing import Dict
from typing import Tuple


from sxo.apps.simple.persisted_quote import RedisQuote

from sxo.util.time import GranularTime
from sxo.util.runtime.redis_set import RedisSet

from sxo.interface.client import SaxoClient
from sxo.interface.definitions import OrderDirection
from sxo.apps.simple.strategy_config import StrategyConfig


def round_sig(x, sig=100):
    if x == 0:
        return 0
    else:
        return round(x, sig-int(floor(log10(abs(x))))-1)


class StrategyImpl():

    def __init__(self,):

        # get config        
        conf = StrategyConfig()
        self._instrument = conf.instrument()
        self._alpha= conf.alpha()
        self._beta = conf.beta()
        frequency = conf.frequency()        
        self._order_size = conf._trade_size
        self._frequency = np.timedelta64(frequency, 's')
        self._tick_size = None

        self._strategy_name = "simple_strat"

        # connect to db
        self._tick_db = RedisQuote(self._instrument)        
        self._last_actioned = np.datetime64('now')

        self._short_entry_oids = RedisSet(f"<{self._strategy_name}>:<orders>:SHORT_ENTRY")
        self._short_exit_oids = RedisSet(f"<{self._strategy_name}>:<orders>:SHORT_EXIT")

        self._long_entry_oids = RedisSet(f"<{self._strategy_name}>:<orders>:LONG_ENTRY")
        self._long_exit_oids = RedisSet(f"<{self._strategy_name}>:<orders>:LONG_EXIT")

        # create a client
        self._client = SaxoClient(token_file='/data/saxo_token')
        # clean any old orders
        self.__review_orders()


    def __read_tick_history(self, window:np.timedelta64) -> pd.DataFrame:
        df = self._tick_db.tail(window)
        return df

    def __call__(self,):
        t0 = time.time()

        now = np.datetime64('now')
        time_since_acted = now  - self._last_actioned

        # print(f" {self._instrument.__str__()}. dt =  {time_since_acted}")

        if time_since_acted > self._frequency:
            print(f"\n---- {now.astype('datetime64[s]')} ACTING -----")
            self._last_actioned = now
            # get data for the window
            ticks = self.__read_tick_history(self._frequency)
            if len(ticks) > 5:
                staleness = self.__age_of_last_tick(now, ticks)
                long_entry, long_exit, short_entry, short_exit = self.__strat(ticks, self._alpha, self._beta, 6)
                long_size, short_size = self._order_size, self._order_size
                self.__review_orders()
                self.__place_new_orders(long_entry, long_exit, long_size, short_entry, short_exit, short_size)
                # test - strat in tick space
                self.__strat_ticks(ticks, self._alpha, self._beta, 6)

            else:
                print(f"SKIPPING. not enough data to run strategy:\n{ticks}")

            t1 = time.time()
            print(f"update took {t1 - t0}s. looking at {len(ticks)} quotes")
        else:
            print('.', end='')

    def __age_of_last_tick(self,
                           now:np.datetime64,
                           df:pd.DataFrame) -> np.timedelta64:
        return df['t'].values[-1] - now
        pass

    def __strat(self,
                df:pd.DataFrame,
                alpha:float,
                beta:float,
                precision:int = -1) -> Tuple[np.float64, np.float64, np.float64, np.float64]:
        
        wmid = (df['bid'].values * df['asz'].values + df['ask'].values * df['bsz'].values) / (df['asz'].values + df['bsz'].values)
        mid = (df['bid'].values + df['ask'].values) / 2
        range = np.max(wmid) - min(wmid)
        last_bid, last_ask, last_mid, = df.bid.values[-1], df.ask.values[-1], wmid[-1]

        #
        # find tick_size. basically smallest dp
        #
        price_increments = np.sort(np.diff(np.sort(np.append(df['bid'].values, df['ask'].values))))
        non_zero_increments = price_increments[price_increments > 0]
        if len(non_zero_increments) > 0:
            tick_size_canditate = round_sig(non_zero_increments[0], 5)
            print(f"tick size candidate: {tick_size_canditate}")
            if not self._tick_size:
                self._tick_size = tick_size_canditate
            elif tick_size_canditate < self._tick_size:
                self._tick_size = tick_size_canditate


        price = last_mid
        longEntry = price - alpha * range
        longExit = longEntry + beta * range
        shortEntry = price + alpha * range
        shortExit = shortEntry - beta * range

        rs = round_sig
        if precision > 0:
            price = round_sig(price, precision)
            range = round_sig(range, precision)
            longEntry = round_sig(longEntry, precision)
            longExit = round_sig(longExit, precision)
            shortEntry = round_sig(shortEntry, precision)
            shortExit = round_sig(shortExit, precision)

        print(f"LONG:  {price} / {range}. in: {longEntry} -> {longExit}. Delta: {rs(longEntry - price, 5)} -> {rs(longEntry - longExit, 5)}")
        print(f"SHORT: {price} / {range}. in: {shortEntry} -> {shortExit}. Delta: {rs(price - shortEntry, 5)} -> {rs(shortEntry- shortExit, 5)}")

        # check to see where the conputed order prices are
        if price and longEntry and longExit:
            if longEntry == longExit:
                longEntry, longExit = None, None

            if price - longEntry <= 0 :
                longEntry, longExit = None, None

        if price and shortEntry and shortExit:
            if shortEntry == shortExit:
                shortEntry, shortExit = None, None
            if shortEntry - price <= 0:
                shortEntry, shortExit = None, None

        return (longEntry, longExit, shortEntry, shortExit)

    def __strat_ticks(self,
                df:pd.DataFrame,
                alpha:float,
                beta:float,
                precision:int = -1) -> Tuple[np.float64, np.float64, np.float64, np.float64]:
        
        print(f"... tick version ...")
        
        wmid = (df['bid'].values * df['asz'].values + df['ask'].values * df['bsz'].values) / (df['asz'].values + df['bsz'].values)
        range = np.max(wmid) - min(wmid)
        last_bid, last_ask, last_mid, = df.bid.values[-1], df.ask.values[-1], wmid[-1]

        #
        # find tick_size. basically smallest dp
        #
        price_increments = np.sort(np.diff(np.sort(np.append(df['bid'].values, df['ask'].values))))
        non_zero_increments = price_increments[price_increments > 0]
        if len(non_zero_increments) > 0:
            tick_size_canditate = round_sig(non_zero_increments[0], 5)
            print(f"tick size candidate: {tick_size_canditate}")
            if not self._tick_size:
                self._tick_size = tick_size_canditate
            elif tick_size_canditate < self._tick_size:
                self._tick_size = tick_size_canditate

        if not self._tick_size:
            print(f"ERROR. Unknown tick size: {tick_size_canditate}")
            return (None, None, None, None)

        price = last_mid
        longEntry = price - alpha * range
        longExit = longEntry + beta * range
        shortEntry = price + alpha * range
        shortExit = shortEntry - beta * range

        rs = round_sig
        if precision > 0:
            price = round_sig(price, precision)
            range = round_sig(range, precision)
            longEntry = round_sig(longEntry, precision)
            longExit = round_sig(longExit, precision)
            shortEntry = round_sig(shortEntry, precision)
            shortExit = round_sig(shortExit, precision)

        print(f"LONG:  {price} / {range}. in: {longEntry} -> {longExit}. Delta: {rs(longEntry - price, 5)} -> {rs(longEntry - longExit, 5)}")
        print(f"SHORT: {price} / {range}. in: {shortEntry} -> {shortExit}. Delta: {rs(price - shortEntry, 5)} -> {rs(shortEntry- shortExit, 5)}")

        # # check to see where the conputed order prices are
        # if price and longEntry and longExit:
        #     if longEntry == longExit:
        #         longEntry, longExit = None, None

        #     if price - longEntry <= 0 :
        #         longEntry, longExit = None, None

        # if price and shortEntry and shortExit:
        #     if shortEntry == shortExit:
        #         shortEntry, shortExit = None, None
        #     if shortEntry - price <= 0:
        #         shortEntry, shortExit = None, None

        # return (longEntry, longExit, shortEntry, shortExit)

    def __place_new_orders(self, longEntry, longExit, long_size, short_entry, short_exit, short_size):
        instr = self._instrument.__str__()

        texp = GranularTime(units ='m').add(self._frequency).round(0.1)

        def place(side, entry_price, exit_price, size) -> int:
            try:
                if entry_price and exit_price:
                    print(f"placing {side} {{{instr}}} at : {entry_price} -> {exit_price} (size:{size})")
                    oid =  self._client.limit_order(instr, side, entry_price, exit_price, size, expiry_time = str(texp))
                    print(f"SUCCESSFULLY Placed {side} : detail {oid}")
                    return oid
                else :
                    print(f"IGNORING - BAD PRICE when placing {side} {{ {instr} }} at : {entry_price} -> {exit_price} (size:{size})")
                    return None
            except Exception as e:
                print(f"ERROR:>> FAILED placing {side} {{ {instr} }} at : {entry_price} -> {exit_price} (size:{size})")
                print(f"exception : \n -----{e}\n -----")
            return None

        if short_entry and short_exit:
            oid_short = place(OrderDirection.Sell, short_entry, short_exit, short_size)
            if oid_short:
                short_entry_oid = oid_short['OrderId']
                short_exit_oids = [x['OrderId'] for x in oid_short['Orders']]
                self._short_entry_oids.add(short_entry_oid)
                self._short_exit_oids.madd(short_exit_oids)
                time.sleep(0.5)
    
        if longEntry and longExit:
            oid_long = place(OrderDirection.Buy, longEntry, longExit, long_size)
            if oid_long:
                long_entry_oid = oid_long['OrderId']
                long_exit_oids = [x['OrderId'] for x in oid_long['Orders']]
                self._long_entry_oids.add(long_entry_oid)
                self._long_exit_oids.madd(long_exit_oids)

    def __review_orders(self,):
        
        try:
            #
            # what is in the OMS
            #
            all_current_orders = self._client.list_orders()
            all_order_ids = {o["OrderId"] for o in all_current_orders["Data"]}
            #
            # delete our short orders that hevent been filled
            # 
            def delete_old_entry_orders(label:str, order_set):
                for oid in order_set.list():
                    if oid in all_order_ids:
                        print(f"DELETING active {label} order. {oid}.")
                        self._client.delete_orders(oid)
                    else:
                        print(f"DELETING a MISSING {label} order. {oid}.")
                    # either way, delete the entry order from our list
                    order_set.rm(oid)
                    time.sleep(0.5)

            delete_old_entry_orders("SHORT", self._short_entry_oids)
            delete_old_entry_orders("LONG", self._long_entry_oids)

            # print("===========")
            # for oid in self._long_exit_oids.list():
            #     if oid in all_order_ids:
            #         print(f"exit OID {oid} is still known")
            #     else:
            #         print(f"exit OID {oid} NOT known")
            # print("===========")

        except Exception as e:
            print(f"ERROR deleting orders. {e}")
