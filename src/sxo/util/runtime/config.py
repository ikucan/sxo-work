
import os
from abc import ABC, abstractmethod
from sxo.interface.entities.instruments import InstrumentUtil
from sxo.interface.entities.instruments import Instrument
from typing import Tuple

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
        self._port = self.get_int(RedisConfig.REDIS_PORT, False, "6379")
        self._pass = self.get_str(RedisConfig.REDIS_PASS, False, None)

    def redis_host(self,) -> str:
        return self._host

    def redis_port(self,) -> int:
        return self._port

    def redis_pass(self,) -> str | None:
        return self._pass
    
    def get_all(self,) -> Tuple[str, int, str]:
        return (
            self.redis_host(),
            self.redis_port(),
            self.redis_pass(),
        )


# # -*- coding: utf-8 -*-
# import os


# # ###
# # split the instruments out of the CSV env string
# # ###
# def parse_instruments(raw_instr_string: str):
#     instrs = []
#     for entry in raw_instr_string.split(","):
#         clean_str = entry.strip()
#         if len(clean_str) > 0:
#             instrs.append(entry.strip())
#     return instrs


# def read_env(var: str, raise_if_missing: bool = True, default_value=None) -> str:
#     if var in os.environ:
#         return os.environ[var]
#     elif raise_if_missing and not default_value:
#         raise ValueError(f"missing environment varialble '{var}'")
#     else:
#         return default_value

# # ###
# # # read and check config to make sure everything is sensible
# # ###
# def config():
#     """
#     read the config from environemnt variables
#     """

#     token_file = read_env("TOKEN_FILE")
#     raw_instruments = read_env("INSTRUMENTS")
#     loop_sleep = read_env("SLEEP_PERIOD", raise_if_missing=False)
#     hb_tolerrance = read_env("HB_TOLERANCE", raise_if_missing=False)
#     if loop_sleep is None:
#         loop_sleep = 5
#     if hb_tolerrance is None:
#         hb_tolerrance = 20
#     else:
#         hb_tolerrance = int(hb_tolerrance)
#     instruments = parse_instruments(raw_instruments)
#     return token_file, instruments, loop_sleep, hb_tolerrance
