import os
from abc import ABC
from abc import abstractmethod
import redis
import json
from typing import Tuple
from sxo.interface.entities.instruments import Instrument

class Cache(ABC):
    def __init__(self, ):
        pass

    @abstractmethod
    def add_instrument_def(self, i:Instrument):
        ...
    @abstractmethod
    def get_instrument_def(self, uid:int) -> Instrument:
        ...

    @staticmethod
    def make_redis_cache():
        return RedisCache()


class RedisCache(Cache):

    def __init__(self,):
        super().__init__()
        (h,p,pwd) = self.__get_redis_config()

        self._r = redis.Redis(host = h, port=p, password= pwd)

    def add_instrument_def(self, i:Instrument):
        key = f"instrument_def_{i.uid()}"
        value = json.dumps(i._json)
        self._r.set(key, value)

    def get_instrument_def(self, uid:int) -> Instrument:
        key = f"instrument_def_{uid}"
        json_str = self._r.get(key)
        jobj = json.loads(json_str)
        i = Instrument.of_json(jobj)
        return i


    def __get_redis_config(self,) -> Tuple[str, int, str | None]:
        host = os.getenv("REDIS_HOST")
        port = os.getenv("REDIS_PORT")
        pwrd = os.getenv("REDIS_PASS")

        if host is None:
            host = "127.0.0.1"
        if port is None:
            port = 6379

        return (host, port, pwrd)
