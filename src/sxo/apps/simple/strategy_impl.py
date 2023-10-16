# -*- coding: utf-8 -*-
import time
import os
import numpy as np
import pandas as pd

from math import log10, floor

from typing import Any
from typing import Dict
from typing import Tuple


from sxo.apps.simple.config import strategy_config
from sxo.apps.simple.persisted_quote import RedisQuote

from sxo.interface.definitions import OrderDirection
from sxo.interface.entities.instruments import Instrument


def round_sig(x, sig=100):
    return round(x, sig-int(floor(log10(abs(x))))-1)


class StrategyConfig:
    TRADE_FREQUENCY = "TRADE_FREQUENCY"
    ALPHA = "ALPHA"
    BETA = "BETA"

    def __init__(self,):
        frequency = os.getenv(StrategyConfig.TRADE_FREQUENCY)
        alpha = os.getenv(StrategyConfig.ALPHA)
        beta = os.getenv(StrategyConfig.BETA)
        
        self._frequency = int(frequency)
        self._alpha = float(alpha)
        self._beta = float(beta)

    def frequency(self,) -> int:
        return self._frequency

    def alpha(self,) -> float:
        return self._alpha

    def beta(self,) -> float:
        return self._beta


class StrategyImpl(StrategyConfig):

    def __init__(self,
                instr: Instrument,
                sxo_client: int,):
        
        self._instrument = instr
        self._client = sxo_client
        self._tick_db = RedisQuote(instr)
        alpha, beta,  frequency, data_win = strategy_config()
        self._alpha= alpha
        self._beta = beta
        self._frequency = np.timedelta64(frequency, 's')
        self._data_window = np.timedelta64(data_win, 'm')
        self._last_actioned = np.datetime64('now')
        instr.canonical_symbol

    def __read_tick_history(self, window:np.timedelta64) -> pd.DataFrame:
        df = self._tick_db.tail(window)
        return df

    def __call__(self, update:Dict[Any, Any] | None):
        if update:
            t0 = time.time()

            last_tick_time = np.int64(update['t']).astype('datetime64[ms]')            

            time_since_acted = last_tick_time - self._last_actioned

            # print(f" tick time: {last_tick_time}")
            # print(f" last acted: {self._last_actioned}")
            print(f" {self._instrument.__str__()}. dt =  {time_since_acted}")

            if time_since_acted > self._frequency:
                print("---- ACTING -----")
                self._last_actioned = last_tick_time
                ticks = self.__read_tick_history(self._data_window)
                if len(ticks) > 5:
                    longEntry, longExit, shortEntry, shortExit = self.__strat(ticks, 1.5, 0.6, 7)
                    self.__review_orders()
                    self.__place_new_orders(longEntry, longExit, shortEntry, shortExit)

                t1 = time.time()
                print(f"update took {t1 - t0}s. looking at {len(ticks)} quotes. \n---\n{ticks.tail(5)}")

        else:
            print("ignorring NULL update")


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
        from sxo.interface.client import SaxoClient
        client = SaxoClient(token_file = "/data/saxo_token")
        client.limit_order(self._instrument.__str__(), OrderDirection.Buy, longEntry, longExit, 1000000)
        pass
    
    def __review_orders(self,):
        pass