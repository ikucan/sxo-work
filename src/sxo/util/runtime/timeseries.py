# -*- coding: utf-8 -*-
from abc import ABC
from abc import abstractmethod
from typing import Tuple

import numpy as np
import pandas as pd
import redis
from sxo.util.runtime.redis import RedisConfig

TMIN, TMAX = 0, np.iinfo(np.int64).max


class TsError(Exception):
    pass


class TimeSeries(ABC):
    '''
    A timeseries interface
    '''
    @abstractmethod
    def add(self, t: np.int64, v: float) -> int:
        ...

    @abstractmethod
    def madd(self, t: np.array, v: np.array) -> np.array:
        ...

    @abstractmethod
    def del_range(self, t0: np.int64 | None = None, t1: np.int64 | None = None) -> int:
        ...

    @abstractmethod
    def get_range(self, t0: np.int64 = TMIN, t1: np.int64 = TMAX, convert: str = "frame", name: str | None = None, index:bool = True) -> Tuple[np.array, np.array] | pd.DataFrame:
        ...


class PersistedTimeSeries(TimeSeries):
    '''
    Abstract class for a persisted timeseries
    '''
    @abstractmethod
    def set_retention(self, time_ms: np.int64):
        '''
        Set a time window for how much data to keep in the persisted timeseries.

        :param time_ms np.int64. window size. any data older than 'now' - time_ms will be deleted
        '''
        ...


class RedisTs(PersistedTimeSeries):
    '''
    A redis ts module implementation of a persisted time series. 
    Manages the data using the Redis TS module.
    Note that Redis TS module operations are reasonable expensive (1s for a lookup of 10K value/pairs)
    '''
    def __init__(
        self,
        name: str,
        retention_period_ms: int = 0,
        delete_if_exists: bool = False,
        duplicates_policy: str = "LAST",
    ):
        """
        for duplicates policy use Redis acceptable values https://redis.io/commands/ts.create/
        """
        self._name = name
        self._retention = retention_period_ms
        self._duplicates = duplicates_policy

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

                # even if ts exists, provided retention period may be different, so set
                self.__set_retention()
                self.__set_duplicates()

        else:
            self.__create_redis_ts()

    def __create_redis_ts(self):
        self._ts_obj = self._ts_module.create(self._name, retention_msecs=self._retention, duplicate_policy=self._duplicates)

    def __set_retention(
        self,
    ):
        self._ts_module.alter(self._name, retention_msecs=self._retention)

    def __set_duplicates(
        self,
    ):
        self._ts_module.alter(self._name, duplicate_policy=self._duplicates)

    def set_retention(self, retention_period_ms: np.int64):
        self._retention = retention_period_ms
        self.__set_retention()

    def add(self, t: np.int64, v: float) -> int:
        """
        add a time series value
        """
        return self._ts_module.add(self._name, t, v)

    def madd(self, t: np.array, v: np.array) -> np.array:
        """
        add a time series value
        """
        N, M = len(t), len(v)
        if M != N:
            raise TsError("ERROR. Need same number of times and values. you passed {M} times and {N} values")
        if M == 0:
            return []

        ts_and_vs = [(self._name, int(t[i]), v[i]) for i in range(N)]
        retval = self._ts_module.madd(ts_and_vs)
        return np.array(retval).astype(np.int64)

    def del_range(self, t0: np.int64 | None = None, t1: np.int64 | None = None) -> int:
        """
        if t0 is None, set it to 0
        if t1 is None, set it to be same as t0
        """
        if t0 is None:
            t0 = 0
        if t1 is None:
            t1 = t0

        return self._ts_module.delete(self._name, t0, t1)

    def get_range_raw(self, t0: np.int64 = TMIN, t1: np.int64 = TMAX):
        return self._ts_module.range(self._name, t0, t1)

    def get_range(self, t0: int = TMIN, t1: int = TMAX, convert: str = "frame", name: str | None = None, index:bool = True) -> Tuple[np.array, np.array] | pd.DataFrame:
        entries = self.get_range_raw(t0, t1)
        times = np.array([x[0] for x in entries])
        vals = np.array([x[1] for x in entries])
        if convert == "frame":
            val_col = 'v' if name is None else name
            df = pd.DataFrame({"t": times, val_col: vals})
            if index:
                return df.set_index('t')
            else:
                return df
        elif convert == "vector":
            return (times, vals)
        else:
            raise TsError(f" convert parameter must be either frame or vector. you supplied: {convert}")
