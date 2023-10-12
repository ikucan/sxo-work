# -*- coding: utf-8 -*-
import time
import os
import numpy as np
import pandas as pd

from typing import Any
from typing import Dict

from sxo.apps.simple.config import strategy_config
from sxo.apps.simple.persisted_quote import RedisQuote
from sxo.interface.entities.instruments import Instrument


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
                data_window_mins: int = 30,):
        
        self._tick_db = RedisQuote(instr)
        alpha, beta,  frequency, data_win = strategy_config()
        self._alpha= alpha
        self._beta = beta
        self._frequency = np.timedelta64(frequency, 's')
        self._data_window = np.timedelta64(data_win, 'm')
        self._last_actioned = np.datetime64('now')

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
            print(f" dt =  {time_since_acted}")

            if time_since_acted > self._frequency:
                print("---- ACTING -----")
                self._last_actioned = last_tick_time
                ticks = self.__read_tick_history(self._data_window)
                t1 = time.time()
                print(f"update took {t1 - t0}s. looking at {len(ticks)} quotes. \n---\n{ticks.tail(5)}")



        else:
            print("ignorring NULL update")
