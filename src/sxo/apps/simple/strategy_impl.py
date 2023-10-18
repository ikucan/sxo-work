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

from sxo.interface.client import SaxoClient
from sxo.interface.definitions import OrderDirection
from sxo.apps.simple.strategy_config import StrategyConfig


def round_sig(x, sig=100):
    return round(x, sig-int(floor(log10(abs(x))))-1)


class StrategyImpl():

    def __init__(self,):

        # get config        
        conf = StrategyConfig()
        self._instrument = conf.instrument()
        self._alpha= conf.alpha()
        self._beta = conf.beta()
        frequency = conf.frequency()        
        self._frequency = np.timedelta64(frequency, 's')

        # connect to db
        self._tick_db = RedisQuote(self._instrument)        
        self._last_actioned = np.datetime64('now')
        self._long_oid = None
        self._short_oid = None

        # create a client
        self._client = SaxoClient(token_file='/data/saxo_token')


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
                longEntry, longExit, shortEntry, shortExit = self.__strat(ticks, self._alpha, self._beta, 6)
                self.__review_orders()
                self.__place_new_orders(longEntry, longExit, shortEntry, shortExit)

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
        range = np.max(wmid) - min(wmid)
        last_bid, last_ask, last_mid, = df.bid.values[-1], df.ask.values[-1], wmid[-1]

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
        
        assert(longEntry <  longExit) 
        assert(longEntry <  price) 
        assert(shortEntry >  shortExit) 
        assert(shortEntry >  price) 
        return (longEntry, longExit, shortEntry, shortExit)

    def __place_new_orders(self, longEntry, longExit, shortEntry, shortExit):
        instr = self._instrument.__str__()
        try:
            print(f"placing SHORT {{ {instr} }} at : {shortEntry} -> {shortExit}")
            oid =  self._client.limit_order(instr, OrderDirection.Sell, shortEntry, shortExit, 100000)
            print(oid)
            self._short_oid = oid['OrderId']

        except Exception as e:
            print(f"ERROR placing SHORT order for  for  {{ {instr} }}. {e}")

        time.sleep(0.5)

        try:
            print(f"placing LONG  {{ {instr} }} at : {longEntry} -> {longExit}")
            oid =  self._client.limit_order(instr, OrderDirection.Buy, longEntry, longExit, 1000000)
            print(oid)
            self._long_oid = oid['OrderId']
        except Exception as e:
            print(f"ERROR placing LONG order for  {{ {instr} }}. {e}")
    
    def __review_orders(self,):
            try:
                #oid = None
                orders = self._client.list_orders()
                all_order_ids = {o["OrderId"] for o in orders["Data"]}

                oids = [self._long_oid, self._short_oid]
                for oid in oids:
                    print(f"DELETING  order : {oid} ")
                    if oid in all_order_ids:
                        #check if the order is still around...
                        self._client.delete_orders(oid)
                    else:
                        print(f"=================")
                        print(f"  CANNOT DELETE order {oid}. It must have been filled.")
                        print(f"=================")
            except Exception as e:
                print(f"ERROR deleting orders. {oid}. {e}")
