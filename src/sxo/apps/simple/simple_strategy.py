# -*- coding: utf-8 -*-
from concurrent.futures import ThreadPoolExecutor as exec
from typing import Any
from typing import Callable
from typing import Dict

from sxo.apps.simple.config import config
from sxo.interface.client import SaxoClient
from sxo.interface.entities.instruments import Instrument
from sxo.interface.entities.instruments import InstrumentUtil
from sxo.util.runtime.heartbeat import HeartBeatMonitor


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

    def __call__(self, update: Dict[str, Any]):
        print(update)
        if self._heartbeat is not None:
            self._heartbeat(self.instrument)
        self._tick_count += 1
        # """
        # callback handler for each update
        # the update should contain either a Quote or Snapshot
        # """
        # try:
        #     if "Quote" in update:
        #         self.__update(update)
        #     elif "Snapshot" in update:
        #         self.__update_snapshot(update)
        # except Exception:
        #     print("============================")
        #     print(update)
        #     import traceback

        #     traceback.print_exc()
        #     print("============================")


# ###
# mainline
# ###
def mainline():
    global executor
    # get config
    token_file, output_dir, instruments, loop_sleep, hb_max_tolerance = config()

    executor = exec(max_workers=10)

    client = SaxoClient(token_file=token_file)
    hb_monitor = HeartBeatMonitor(executor, loop_sleep, hb_max_tolerance)

    # subscribe to each instrument and dispatch to the thread pool
    for i in instruments:
        instr = InstrumentUtil.parse(i)
        # executor.submit(client.subscribe_price, instr, SimpleStrat(instr, heartbeat))
        executor.submit(client.subscribe_price, instr, SimpleStrat(instr, hb_monitor))

    # wait until stop
    # heartbeat_monitor(loop_sleep, hb_max_tolerance)
    hb_monitor.start()


if __name__ == "__main__":
    mainline()
