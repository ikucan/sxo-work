# -*- coding: utf-8 -*-
import random as r
from sxo.util.runtime.timeseries import RedisTs
from sxo.util.runtime.timeseries import TimeSeries
import numpy as np
import time

class Test:
    def __init__(
        self,
    ):
        self.tt = None


def ms_now():
    return int(np.datetime64('now').astype('datetime64[ms]').astype(np.int64))

# if __name__ == "__main__":
#     print("--- start ---")
#     ts = RedisTs[np.float32]('ts1', retention_period_ms=50000, delete_if_exists=True)
#     #ts = RedisTs[np.float32]('ts1', retention_period_ms=50000)
    
#     for i in range(1000):
#         k, v = ms_now(), 10 + r.random()
#         print(f'inserting values {k}:{v} into timeseries {ts._name}')
#         ts.add(ms_now(), 10 + r.random())
#         time.sleep(1)
#     # r = redis.Redis(password='boss')
#     # r.ts().create('ts1')
#     print("--- end ---")


if __name__ == "__main__":
    print("--- start ---")
    ts = RedisTs[np.float32]('ts1', retention_period_ms=50000, delete_if_exists=True)
    
    k, v = ms_now(), 10 + r.random()
    print(f'inserting values {k}:{v} into timeseries {ts._name}')
    for i in range(1,11):
        ts.add(i, 10 + i)
    ts.del_range(10)

    ts.del_range(t1 = 4)

    ts.del_range(6,7)


    print("--- end ---")
