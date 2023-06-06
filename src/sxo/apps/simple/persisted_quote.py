# -*- coding: utf-8 -*-
import json
from typing import Any
from typing import Dict

import numpy as np
from sxo.interface.entities.instruments import Instrument
from sxo.util.runtime.timeseries import RedisTs


class RedisQuote:
    def __init__(self, instr: Instrument):
        self._instrument = instr
        self._time = None
        self._bid = np.nan
        self._bsz = np.nan
        self._ask = np.nan
        self._asz = np.nan
        self._mid = np.nan

        self._bid_ts = RedisTs(f'ts_bid_{instr.gid()}')
        self._bsz_ts = RedisTs(f'ts_bsz_{instr.gid()}')
        self._ask_ts = RedisTs(f'ts_ask_{instr.gid()}')
        self._asz_ts = RedisTs(f'ts_asz_{instr.gid()}')
        self._mid_ts = RedisTs(f'ts_mid_{instr.gid()}')


    def update(self, json: Dict[Any, Any]):
        if "LastUpdated" in json:
            self._time = int(np.datetime64(json["LastUpdated"]).astype("datetime64[ms]").astype(np.int64))

        if "Quote" in json:
            quote = json["Quote"]
            if "Bid" in quote:
                self._bid = float(quote["Bid"])
            if "BidSize" in quote:
                self._bsz = float(quote["BidSize"])
            if "Ask" in quote:
                self._ask = float(quote["Ask"])
            if "AskSize" in quote:
                self._asz = float(quote["AskSize"])
            if "Mid" in quote:
                self._mid = float(quote["Mid"])
            
            print(f'writing : {self._time}  :: {self._bid}')

            self.__persist()

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


    def to_json(
        self,
    ) -> Dict[Any, Any]:
        i = self._instrument
        return {
            # 'instrument': f"{i.asset_type()}::{i.symbol()}",
            "uic": f"{i.uid()}",
            "t": f"{self._time}",
            "bid": f"{self._bid}",
            "bsz": f"{self._bsz}",
            "ask": f"{self._ask}",
            "asz": f"{self._asz}",
            "mid": f"{self._mid}",
        }

    def __str__(
        self,
    ):
        return json.dumps(self.to_json())
