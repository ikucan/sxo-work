import os
from abc import ABC, abstractmethod
from sxo.interface.entities.instruments import InstrumentUtil
from sxo.interface.entities.instruments import Instrument

class ConfigBase:
    '''
    a bunch of general-purpose helper methods
    for dealing with config
    '''
    # ###
    # split the instruments out of the CSV env string
    # ###
    def parse_instruments(self, raw_instr_string: str):
        instrs = []
        for entry in raw_instr_string.split(","):
            clean_str = entry.strip()
            if len(clean_str) > 0:
                instrs.append(clean_str)
        return instrs


    def get_env(self, var: str, raise_if_missing: bool = True, default_value=None) -> str:
        if var in os.environ:
            return os.environ[var]
        elif raise_if_missing and not default_value:
            raise ValueError(f"missing environment varialble '{var}'")
        else:
            return default_value

    def get_str(self,
                var: str,
                raise_if_missing: bool = True,
                default_value=None) -> str | None:
        return self.get_env(var, raise_if_missing, default_value)

    def get_int(self,
                var: str,
                raise_if_missing: bool = True,
                default_value=None) -> int | None:
        str_val = self.get_env(var, raise_if_missing, default_value)
        return int(str_val)

    def get_float(self,
                  var: str,
                  raise_if_missing: bool = True,
                  default_value=None) -> float | None:
        str_val = self.get_env(var, raise_if_missing, default_value)
        return float(str_val)

class RedisConfig(ConfigBase):
    REDIS_HOST = "REDIS_HOST"
    REDIS_PORT = "REDIS_PORT"
    REDIS_PASS = "REDIS_PASS"
    '''
    Config for a redis connections
    '''
    def __init__(self,):
        self._host = self.get_str(RedisConfig.REDIS_HOST, False, "localhost")
        self._port = self.get_int(RedisConfig.REDIS_HOST, False, "6379")
        self._pass = self.get_str(RedisConfig.REDIS_HOST, False, None)

    def redis_host(self,) -> str:
        return self._host

    def redis_port(self,) -> int:
        return self._port

    def redis_pass(self,) -> str | None:
        return self._pass


class StrategyConfig(ConfigBase):
    INSTRUMENT = "STRATEGY_INSTRUMENT"
    TRADE_FREQUENCY = "STRATEGY_TRADE_FREQUENCY"
    ALPHA = "STRATEGY_ALPHA"
    BETA = "STRATEGY_BETA"

    def __init__(self,):
        instr_str = self.get_str(StrategyConfig.INSTRUMENT)
        self._inst = InstrumentUtil.parse(instr_str)
        self._freq = self.get_int(StrategyConfig.TRADE_FREQUENCY)
        self._alph = self.get_float(StrategyConfig.ALPHA)
        self._beta = self.get_float(StrategyConfig.BETA)


    def instrument(self,) -> Instrument:
        return self._inst

    def frequency(self,) -> int:
        return self._freq

    def alpha(self,) -> float:
        return self._alph

    def beta(self,) -> float:
        return self._beta
