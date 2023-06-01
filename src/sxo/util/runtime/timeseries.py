# -*- coding: utf-8 -*-
from abc import ABC
from abc import abstractmethod
from typing import Tuple

import redis
from sxo.util.runtime.redis import RedisConfig

class TsError(Exception):
    pass


class TimeSeries:
    
    @staticmethod
    def make():
        pass


class PersistedTimeSeries(TimeSeries):
    pass


class RedisTs(PersistedTimeSeries):
    def __init__(
        self,
        name: str,
        retention_period_ms: int | None = None,
        delete_if_exists: bool = False
    ):
        
        self._name = name
        self._retention = retention_period_ms

        (h, p, pwd) = RedisConfig.get()
        self._redis = redis.Redis(h, p, password = pwd)
        self._ts_module = self._redis.ts()

        self._ts = self.__create_redis_ts(delete_if_exists)
        
    def __create_redis_ts(self, delete_prev:bool):
        if self._redis.exists(self._name):
            key_type = self._redis.type(self._name)
            if str(key_type, 'UTF-8') != 'TSDB-TYPE':
                raise TsError(f'Redis key {self._name} already exists but is not a timeseries type: {key_type}')
        else:
            ts_obj = self._ts_module.create(self._name)
