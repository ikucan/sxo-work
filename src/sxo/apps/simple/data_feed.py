# -*- coding: utf-8 -*-
from concurrent.futures import ThreadPoolExecutor as exec
from typing import Any
from typing import Callable
from typing import Dict

#from sxo.apps.simple.config import config
from sxo.apps.simple.persisted_quote import RedisQuote
from sxo.interface.entities.instruments import Instrument

class DataFeedError(BaseException):
    pass

# ###
# # tick data writer class for each instrument
# ###
class DataFeed:
    def __init__(self, instr: Instrument, heartbeat: Callable | None = None):

        self._instrument = instr
        self._heartbeat = heartbeat
        self._tick_count = 0
        self._tick_db = RedisQuote(instr)

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
