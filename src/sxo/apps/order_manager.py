# -*- coding: utf-8 -*-
import asyncio
import json
from pprint import pprint
from typing import Any
from typing import Dict

import numpy as np
import pandas as pd


class StupidStrategy:
    def __init__(self, instr: str, frequency_s: int = 60):
        self.instrument = instr
        # self._t = np.datetime64(dt.datetime.now().date().strftime("%Y-%m-%d"))
        self._t = np.datetime64("2000-01-01")
        self._data_block = pd.DataFrame()

    async def __call__(self, price_update: Dict[str, Any]):
        print(f"STRATEGY for instrument :>> {self.instrument}")
        pprint(price_update)
        if "LastUpdated" in price_update:
            time_string = price_update["LastUpdated"]
            self._t = np.datetime64(time_string[:-1])
        if "Quote" in price_update:
            quote = price_update["Quote"]
            self._a, self._b, self._m = quote["Ask"], quote["Bid"], quote["Mid"]

        # pd.concat(objs = [self._data_block])
        # pprint(update)
        # print(f"{self._t} :: {self._a} : {self._b} : {self._m}")


if __name__ == "__main__":
    instrument, date = "GBPEUR", "20220527"
    raw_data_file = f"/data/{instrument}_raw_{date}.json"

    strategy = StupidStrategy(instrument)

    with open(raw_data_file) as file:
        line = file.readline()
        while line is not None and len(line) > 0:
            update = json.loads(line)
            # pprint(update)

            asyncio.new_event_loop().run_until_complete(strategy(update))

            line = file.readline()
