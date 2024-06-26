# -*- coding: utf-8 -*-
from typing import Any
from typing import Set
from typing import List

import redis
from sxo.util.runtime.config import RedisConfig

class RedisSet:
    ''' 
    set of values persisted in redis
    '''
    def __init__(
        self,
        key: str,
    ):
        """
        for duplicates policy use Redis acceptable values https://redis.io/commands/ts.create/
        """
        self._key = key
#
        (h, p, pwd) = RedisConfig().get_all()
        self._redis = redis.Redis(h, p, password=pwd)
 
    def __create_or_validate_redis_ts(self, delete_prev: bool):
        if self._redis.exists(self._key):
            if delete_prev:
                self._redis.delete(self._key)

    def __create_redis_ts(self):
        pass

    def add(self, value:Any):
        self._redis.sadd(self._key, value)

    def madd(self, values:List[Any]):
        for v in values:
            self.add(v)
 
    def rm(self, value:Any):
        self._redis.srem(self._key, value)

    def mrm(self, values:List[Any]):
        for v in values:
            self.rm(v)

    def get(self,) -> Set:
        vals = self._redis.smembers(self._key)
        strs = {str(x, 'utf-8') for x in vals}
        return strs

    def list(self,) -> List:
        return list(self.get())

    def delete(self,):
        self._redis.delete(self._key)

# if __name__ == "__main__":
#     set = RedisSet("<strat1>:<orders>:ENTRY2")
#     for x in range(20):
#         set.add(x)
#     for x in set.get():
#         if int(x) % 2 == 0:
#             set.rm(x)
#         if int(x)  > 50:
#             set.rm(x)
#     all = sorted(set.list())
#     print(all)
#     set.delete()
#     i = 123