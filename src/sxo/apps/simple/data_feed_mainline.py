# -*- coding: utf-8 -*-
from typing import List

from concurrent.futures import ThreadPoolExecutor as exec

from sxo.apps.simple.data_feed import DataFeed
from sxo.interface.client import SaxoClient
from sxo.interface.entities.instruments import Instrument
from sxo.interface.entities.instruments import InstrumentUtil
from sxo.util.runtime.config import ConfigBase
from sxo.util.runtime.config import SaxoClientConfig
from sxo.util.runtime.heartbeat import HeartBeatMonitor

class DataFeedConfig(ConfigBase):
    INSTRUMENTS = "INSTRUMENTS"
    SLEEP_PERIOD = "SLEEP_PERIOD"
    HB_TOLERANCE = "HB_TOLERANCE"
    NUM_WORKERS = "NUM_WORKERS"

    def __init__(self,):
        instr_str = self.get_str(DataFeedConfig.INSTRUMENTS)
        self._instruments = self.parse_instruments(instr_str)

        self._hb_sleep = self.get_int(DataFeedConfig.SLEEP_PERIOD, False, 5)
        self._hb_tolerance = self.get_int(DataFeedConfig.HB_TOLERANCE, False, 60)
        self._no_workers = self.get_int(DataFeedConfig.NUM_WORKERS, False, 5)

    def instruments(self,) -> List[str]:
        return self._instruments

    def hb_sleep(self,) -> int:
        return self._hb_sleep

    def hb_tolearance(self,) -> int:
        return self._hb_tolerance

    def workers(self,) -> int:
        return self._no_workers


# ###
# mainline
# ###
def mainline():
    global executor 
    # get config
    feed_config = DataFeedConfig()
    saxo_config = SaxoClientConfig()

    executor = exec(max_workers=feed_config.workers())
    client = SaxoClient(token_file=saxo_config.token_file())
    hb_monitor = HeartBeatMonitor(executor, feed_config.hb_sleep(), feed_config.hb_tolearance())

    # subscribe to each instrument and dispatch to the thread pool
    for i in feed_config.instruments():
        instr = InstrumentUtil.parse(i)
        executor.submit(client.subscribe_price, instr, DataFeed(instr, hb_monitor))

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