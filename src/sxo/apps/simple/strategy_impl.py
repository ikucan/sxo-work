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
                data_window_mins: int = 24 * 60,):
        
        self._tick_db = RedisQuote(instr)
        alpha, beta,  frequency, data_win = strategy_config()
        self._alpha= alpha
        self._beta = beta
        self._freequency = np.timedelta64(frequency, 's')
        self._data_window = np.timedelta64(data_win, 'm')
        self._ticks = self.__read_tick_history(self._data_window)

    def __read_tick_history(self, window:np.timedelta64) -> pd.DataFrame:
        df = self._tick_db.tail(window)
        return df

    def __call__(self, update:Dict[Any, Any] | None):
        if update:
            t0 = time.time()
            update['t'] = np.int64(update['t']).astype('datetime64[ms]')
            tick_history = self._ticks
            new_row = pd.DataFrame(update, index=[0])
            combined = pd.concat([tick_history, new_row], ignore_index=True)
            self._ticks = combined
            t1 = time.time()
            print(f"update took {t1 - t0}s. looking at {len(combined)} quotes. \n---\n{combined.tail(5)}")
        else:
            print("ignorring NULL update")
