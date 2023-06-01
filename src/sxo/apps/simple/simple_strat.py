# -*- coding: utf-8 -*-
from concurrent.futures import ThreadPoolExecutor as exec
from typing import Any
from typing import Callable
from typing import Dict

from sxo.apps.simple.config import config
from sxo.apps.simple.quote import Quote
from sxo.interface.entities.instruments import Instrument
from sxo.interface.entities.instruments import InstrumentUtil
from sxo.util.runtime.cache import Cache


class SimpleStratError(BaseException):
    pass


# ###
# # tick data writer class for each instrument
# ###
class SimpleStrat:
    def __init__(self, instr: Instrument, heartbeat: Callable | None = None):
        self._instrument = instr
        self._heartbeat = heartbeat
        self._tick_count = 0
        self._qoute = Quote(instr)
        self._cache = Cache.make_redis_cache()
        self._cache.add_instrument_def(instr)

    def __call__(self, update: Dict[str, Any]):
        print(update)
        if self._heartbeat is not None:
            self._heartbeat()
        self._tick_count += 1
        # """
        # callback handler for each update
        # the update should contain either a Quote or Snapshot
        # """
        try:
            # if "Quote" in update:
            self.__update(update)

        except Exception:
            print("============================")
            print(update)
            import traceback

            traceback.print_exc()
            print("============================")

    def __update(self, update: Dict[str, Any]):
        self._qoute.update(update)
        print(self._qoute)
        self.__test_cache()

    def __test_cache(
        self,
    ):
        ts_name = f"ts_{self._instrument.uid()}_quotes"
        # score = self._qoute.time_as_str()
        time = int(self._qoute._time.astype("datetime64[ms]").astype(int))
        value = self._qoute.__str__()

        self._cache._r.lpush(ts_name, self._qoute.__str__())
