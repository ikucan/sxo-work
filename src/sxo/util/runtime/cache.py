# -*- coding: utf-8 -*-
import json
from abc import ABC
from abc import abstractmethod

import redis
from sxo.interface.entities.instruments import Instrument
from sxo.util.runtime.redis_cfg import RedisConfig


class CacheError(Exception):
    pass


class Cache(ABC):
    @abstractmethod
    def add_instrument_def(self, i: Instrument) -> str:
        ...

    @abstractmethod
    def get_instrument_def(self, uid: int) -> Instrument:
        ...

    @staticmethod
    def make_redis_cache():
        return RedisCache()


class RedisCache(Cache):
    def __init__(self):
        (h, p, pwd) = RedisConfig.get()

        self._r = redis.Redis(host=h, port=p, password=pwd)
        try:
            if not self._r.ping():
                raise CacheError("ERROR. Redis db ping was NOT successfull")
        except Exception as e:
            raise CacheError(f"ERROR thrown while trying to connect to redis DB. {e}")

    def add_instrument_def(self, i: Instrument) -> str:
        key = f"instr_def_{i.canonical_symbol()}"
        value = json.dumps(i._json)
        if not self._r.set(key, value):
            raise CacheError(f"ERROR. Failed to set a redis DB object with key {key}")
        return key

    def get_instrument_def(self, uid: int) -> Instrument:
        key = f"instrument_def_{uid}"
        json_str = self._r.get(key)
        jobj = json.loads(json_str)
        i = Instrument.of_json(jobj)
        return i
