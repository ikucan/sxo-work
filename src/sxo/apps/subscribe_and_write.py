# -*- coding: utf-8 -*-
import asyncio
import datetime as dt
import json
import time
from pprint import pprint
from typing import Any
from typing import Dict

import numpy as np
from apps.order_manager import StupidStrategy
from sxo.interface.client import SaxoClient


def foreva():
    while 1 < 2:
        print("4eva")
        time.sleep(10)


# ###
# # TODO:>>  try one loop per thread
# # https://docs.python.org/3/library/asyncio-eventloop.html
# ###


class DataWriter:
    def __init__(self, out_file: str, strategy):
        self._out_file = open(out_file, "a")
        self._t = np.datetime64()
        self.strategy = strategy
        pass

    def __call__(self, update: Dict[str, Any]):
        self._out_file.write(json.dumps(update))
        self._out_file.write("\n")
        self._out_file.flush()
        print("======================")
        pprint(update)
        print("----------------------")
        asyncio.get_event_loop().create_task(self.strategy(update))


if __name__ == "__main__":
    client = SaxoClient()

    date_str = dt.datetime.now().strftime("%Y%m%d")
    instrument = "GBPEUR"
    raw_data_file = f"/data/{instrument}_raw_{date_str}.json"

    strategy = StupidStrategy(instrument)
    client.subscribe_fx_spot(instrument, DataWriter(raw_data_file, strategy))

    # from concurrent.futures import ProcessPoolExecutor as exec
    # exectr = exec(max_workers=10)
    # f1 = exectr.submit(client.subscribe_fx_spot, "USDJPY", lambda x :print(x))
    # f2 = exectr.submit(client.subscribe_fx_spot, "EURGBP", lambda x :print(x))
    # f3 = exectr.submit(client.subscribe_fx_spot, "GBPUSD", lambda x :print(x))
    # # #exec.submit(foreva)
    foreva()
