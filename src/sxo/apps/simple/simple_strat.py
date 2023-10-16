# -*- coding: utf-8 -*-
from concurrent.futures import ThreadPoolExecutor as exec
from typing import Any
from typing import Callable
from typing import Dict

from sxo.apps.simple.config import config
from sxo.apps.simple.persisted_quote import RedisQuote
from sxo.apps.simple.strategy_impl import StrategyImpl
from sxo.interface.entities.instruments import Instrument
from sxo.interface.entities.instruments import InstrumentUtil
from sxo.util.runtime.cache import Cache


class SimpleStratError(BaseException):
    pass


# ###
# # tick data writer class for each instrument
# ###
class SimpleStrat:
    def __init__(self, instr: Instrument, sxo_client:int, heartbeat: Callable | None = None):

        self._instrument = instr
        self._heartbeat = heartbeat
        self._tick_count = 0
        self._tick_db = RedisQuote(instr)
        # self._cache = Cache.make_redis_cache()
        # self._cache.add_instrument_def(instr)
        self._strat = StrategyImpl(instr, sxo_client)

    def __call__(self, update: Dict[str, Any]):
        print(update)
        if self._heartbeat is not None:
            self._heartbeat()
        # """
        # callback handler for each update
        # the update should contain either a Quote or Snapshot
        # """
        try:
            self._tick_count += 1
            # if "Quote" in update:
            self.__update(update)

        except Exception:
            print("============================")
            print(update)
            import traceback

            traceback.print_exc()
            print("============================")

    def __update(self, update: Dict[str, Any]):
        tick = self._tick_db.update(update)
        print(tick)
        self._strat(tick )
