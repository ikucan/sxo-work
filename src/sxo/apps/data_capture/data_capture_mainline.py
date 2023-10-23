# # -*- coding: utf-8 -*-
from typing import List

from concurrent.futures import ThreadPoolExecutor as exec

# from sxo.apps.simple.data_feed import DataFeed
from sxo.interface.client import SaxoClient
# from sxo.interface.entities.instruments import Instrument
from sxo.interface.entities.instruments import InstrumentUtil
from sxo.util.runtime.config import ConfigBase
from sxo.util.runtime.config import SaxoClientConfig
from sxo.util.runtime.heartbeat import HeartBeatMonitor

class DataCaptureConfig(ConfigBase):
    INSTRUMENTS = "INSTRUMENTS"
    DATA_DIR = "DATA_DIR"
    SLEEP_PERIOD = "SLEEP_PERIOD"
    HB_TOLERANCE = "HB_TOLERANCE"
    NO_WORKERS = "NO_WORKERS"
 
    def __init__(self,):
        instr_str = self.get_str(DataCaptureConfig.INSTRUMENTS)
        self._instruments = self.parse_instruments(instr_str)

        self._data_dir = self.get_str(DataCaptureConfig.DATA_DIR)
        self._hb_sleep = self.get_int(DataCaptureConfig.SLEEP_PERIOD, False, 5)
        self._hb_tolerance = self.get_int(DataCaptureConfig.HB_TOLERANCE, False, 60)
        self._no_workers = self.get_int(DataCaptureConfig.NO_WORKERS, False, 10)


    def instruments(self,) -> List[str]:
        return self._instruments

    def data_dir(self,) -> int:
        return self._data_dir

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
    feed_config = DataCaptureConfig()
    saxo_config = SaxoClientConfig()

    executor = exec(max_workers=feed_config.workers())
    client = SaxoClient(token_file=saxo_config.token_file())
    hb_monitor = HeartBeatMonitor(executor, feed_config.hb_sleep(), feed_config.hb_tolearance())

    # subscribe to each instrument and dispatch to the thread pool
    for i in feed_config.instruments():
        instr = InstrumentUtil.parse(i)
        print(f"capture for instrument : {instr}")
        # executor.submit(client.subscribe_price, instr, DataFeed(instr, hb_monitor))

    # wait until stop
    hb_monitor.start()

if __name__ == "__main__":
    mainline()