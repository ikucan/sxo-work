# -*- coding: utf-8 -*-
import json
import os
from abc import ABC
from abc import abstractmethod
from typing import Tuple

import redis
from sxo.interface.entities.instruments import Instrument

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
    def __init__(
        self,
    ):
        (h, p, pwd) = self.__get_redis_config()

        self._r = redis.Redis(host=h, port=p, password=pwd)
        try:
            if not self._r.ping():
                raise CacheError("ERROR. Redis db ping was NOT successfull")
        except Exception as e:
            raise CacheError(f"ERROR thrown while trying to connect to redis DB. {e}")

    def add_instrument_def(self, i: Instrument) -> str:
        key = f"instrument_def_{i.uid()}"
        value = json.dumps(i._json)
        if not self._r.set(key, value):
            raise CacheError(f"ERROR. Failed to set a redis DB object with key {keyS}")
        return key

    def get_instrument_def(self, uid: int) -> Instrument:
        key = f"instrument_def_{uid}"
        json_str = self._r.get(key)
        jobj = json.loads(json_str)
        i = Instrument.of_json(jobj)
        return i

    def __get_redis_config(
        self,
    ) -> Tuple[str, int, str | None]:
        host = os.getenv("REDIS_HOST")
        port_str = os.getenv("REDIS_PORT")
        pwrd = os.getenv("REDIS_PASS")

        if host is None:
            host = "127.0.0.1"
        if port_str is None:
            port = 6379
        else:
            port = int(port_str)

        return (host, port, pwrd)
