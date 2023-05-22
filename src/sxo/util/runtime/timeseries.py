# -*- coding: utf-8 -*-
from abc import ABC
from abc import abstractmethod
from typing import Tuple

import redis

class TsError(Exception):
    pass

class TimeSeries:
    pass

class PersistedTimeSeries(TimeSeries):
    pass

class RedisTS(PersistedTimeSeries):
    def __init__(
        self,
        name:str,
        redis_client:redis.Redis,
    ):
        self._name = name
        self._redis = redis_client