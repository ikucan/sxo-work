# -*- coding: utf-8 -*-
import json
import time
from typing import Any
from typing import Dict

import numpy as np
import pandas as pd

from sxo.interface.entities.instruments import Instrument
from sxo.util.runtime.timeseries import RedisTs
from sxo.util.runtime.timeseries import TMIN, TMAX
from sxo.apps.simple.quote import Quote


class RedisQuote(Quote):
    def __init__(self, instr: Instrument):
        super().__init__(instr)
        self._instrument = instr
    
        self._bid_ts = RedisTs(f'ts_bid_{instr.canonical_symbol()}')
        self._bsz_ts = RedisTs(f'ts_bsz_{instr.canonical_symbol()}')
        self._ask_ts = RedisTs(f'ts_ask_{instr.canonical_symbol()}')
        self._asz_ts = RedisTs(f'ts_asz_{instr.canonical_symbol()}')
        self._mid_ts = RedisTs(f'ts_mid_{instr.canonical_symbol()}')


    def update(self, json: Dict[Any, Any]) -> Dict[Any, Any] | None:
        update = super().update(json)
        self.__persist()
        return update

    def __persist(self):
        if self._time is None:
            return
                
        if not np.isnan(self._bid):
             self._bid_ts.add(t=self._time, v=self._bid)
        if not np.isnan(self._ask):
             self._ask_ts.add(t=self._time, v=self._ask)
        if not np.isnan(self._bsz):
            self._bsz_ts.add(t=self._time, v=self._bsz)
        if not np.isnan(self._asz):
             self._asz_ts.add(t=self._time, v=self._asz)
        if not np.isnan(self._mid):
             self._mid_ts.add(t=self._time, v=self._mid)


    def get_range(self, t0: int = TMIN, t1: int = TMAX) -> pd.DataFrame:
        tt0 = time.time()
        bid = self._bid_ts.get_range(name='bid', t0=t0, t1=t1)
        ask = self._ask_ts.get_range(name='ask', t0=t0, t1=t1)
        bsz = self._bsz_ts.get_range(name='bsz', t0=t0, t1=t1)  
        asz = self._asz_ts.get_range(name='asz', t0=t0, t1=t1)
        tt1 = time.time()
        bid_ask = bid.join(ask, how='inner').join(bsz, how='inner').join(asz, how='inner').reset_index()
        tt2 = time.time()
        bid_ask['t'] = bid_ask['t'].values.astype('datetime64[ms]').astype('datetime64[ns]')
        tt3 = time.time()
        # print(f"lookup stage: {len(bid_ask)} -> time {tt1-tt0}")
        # print(f"join   stage: {len(bid_ask)} -> time {tt2-tt1}")
        # print(f"conv   stage: {len(bid_ask)} -> time {tt3-tt2}")
        return bid_ask

    def tail(self, window = np.timedelta64) -> pd.DataFrame:
        t1 = np.datetime64('now')
        t0 = t1 - window
        t0, t1 = int(t0.astype('datetime64[ms]').astype(np.int64)), int(t1.astype('datetime64[ms]').astype(np.int64))
        return self.get_range(t0, t1)


# if __name__ == "__main__":
#     import time
#     from sxo.interface.entities.instruments import InstrumentUtil

#     instr = InstrumentUtil.parse("FxSpot::GBPEUR")
#     q =  RedisQuote(instr)
#     t0 = time.time()
#     df1 = q.get_range()
#     t1 = time.time()
#     df2 = q.tail(np.timedelta64(2, 'h'))
#     t2 = time.time()
#     print(f"all data: {len(df1)} -> time {t1-t0}")
#     print(f"2hrs data: {len(df2)} -> time {t2-t1}")
#     i = 123
