# -*- coding: utf-8 -*-
from concurrent.futures import ThreadPoolExecutor as exec
from typing import Any
from typing import Callable
from typing import Dict

from sxo.apps.simple.config import config
from sxo.apps.simple.simple_strat import SimpleStrat
from sxo.interface.client import SaxoClient
from sxo.interface.entities.instruments import InstrumentUtil
from sxo.util.runtime.cache import Cache
from sxo.util.runtime.heartbeat import HeartBeatMonitor

# ###
# mainline
# ###
def mainline():
    global executor
    # get config
    token_file, instruments, loop_sleep, hb_max_tolerance = config()

    executor = exec(max_workers=10)
    client = SaxoClient(token_file=token_file)
    hb_monitor = HeartBeatMonitor(executor, loop_sleep, hb_max_tolerance)

    # subscribe to each instrument and dispatch to the thread pool
    for i in instruments:
        instr = InstrumentUtil.parse(i)
        executor.submit(client.subscribe_price, instr, SimpleStrat(instr, hb_monitor))

    # wait until stop
    hb_monitor.start()
    

if __name__ == "__main__":
    for i in range(1000):
        try:
            mainline()
        except Exception:
            print("============================")
            import traceback

            traceback.print_exc()
            print("============================")