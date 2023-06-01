import redis

from sxo.util.runtime.timeseries import  TimeSeries
from sxo.util.runtime.timeseries import  RedisTs

class Test:
    def __init__(self,):
        self.tt = None


if __name__ == "__main__":
    print("--- start ---")
    ts = RedisTs('Ts1')
    # r = redis.Redis(password='boss')
    # r.ts().create('ts1')
    print("--- end ---")
