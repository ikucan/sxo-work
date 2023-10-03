# -*- coding: utf-8 -*-
import os

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
    def __init__(self, instr: Instrument):
        self._quote = RedisQuote(instr)

    def __call__(self,):
        df = self._quote.get()
        print(df)
