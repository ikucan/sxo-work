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
        self.instrument = instr
        self._heartbeat = heartbeat
        self._tick_count = 0
        self._qoute = Quote(instr)

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
            if "Quote" in update:
                self.__update(update)
        except Exception:
            print("============================")
            print(update)
            import traceback
            traceback.print_exc()
            print("============================")

    def __update(self, update: Dict[str, Any]):
        print(update)
        self._qoute.update(update)
        print(self._qoute)
        

