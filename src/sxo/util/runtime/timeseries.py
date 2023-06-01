# -*- coding: utf-8 -*-
from abc import ABC
from abc import abstractmethod
from typing import Generic
from typing import Tuple
from typing import TypeVar

import numpy as np
import redis
from sxo.util.runtime.redis import RedisConfig

T = TypeVar('T')

class TsError(Exception):
    pass

class TimeSeries(ABC, Generic[T]):
    @staticmethod
    def make():
        pass

    @abstractmethod
    def add(self, t:np.int64, v:T):
        ...


class PersistedTimeSeries(TimeSeries[T]):
    pass


class RedisTs(PersistedTimeSeries[T]):
    def __init__(self, name: str, retention_period_ms: int = 0, delete_if_exists: bool = False):
        self._name = name
        self._retention = retention_period_ms

        (h, p, pwd) = RedisConfig.get()
        self._redis = redis.Redis(h, p, password=pwd)
        self._ts_module = self._redis.ts()

        self._ts = self.__create_or_validate_redis_ts(delete_if_exists)

    def __create_or_validate_redis_ts(self, delete_prev: bool):
        if self._redis.exists(self._name):
            if delete_prev:
                self._redis.delete(self._name)
                self.__create_redis_ts()
            else:
                key_type = self._redis.type(self._name)
                if str(key_type, "UTF-8") != "TSDB-TYPE":
                    raise TsError(f"Redis key {self._name} already exists but is not a timeseries type: {key_type}")
        else:
            self.__create_redis_ts()

    def __create_redis_ts(self):
        self._ts_obj = self._ts_module.create(self._name, retention_msecs=self._retention)


    def add(self, t:int, v:T):
        self._ts_module.add(self._name, t, v)
