# -*- coding: utf-8 -*-
import datetime as dt
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor as exec
from pathlib import Path
from typing import Any
from typing import Callable
from typing import Dict

from sxo.interface.client import SaxoClient
from sxo.interface.entities.instruments import Instrument
from sxo.interface.entities.instruments import InstrumentUtil
from sxo.util.quote import Quote
from sxo.util.threads import kill_executor_threads


# ###
# # TODO:>>  try one loop per thread
# # https://docs.python.org/3/library/asyncio-eventloop.html
# ###
class DataWriterError(BaseException):
    pass


# ###
# # tick data writer class for each instrument
# ###
class DataWriter:
    def __init__(self, out_dir: str, instr: str, heartbeat: Callable = None):
        """
        check output details and crate output writer
        """
        data_path = Path(out_dir)
        if not data_path.exists():
            raise DataWriterError(f"output location must exist: {out_dir}")

        self.out_path = data_path / instr.asset_class() / instr.symbol()
        Path(self.out_path).mkdir(parents=True, exist_ok=True)

        self.instrument = instr

        self._metadata_file = self.__make_output_file("metadata")
        self._data_file = self.__make_output_file()
        self._quote = None
        self._heartbeat = heartbeat
        self._tick_count = 0

    def __change_file(
        self,
    ):
        """
        check current date v date of current file
        """
        return self.file_date < dt.datetime.now().date()

    def __make_output_file(self, pattern: str = None):
        """
        create an output file
        """
        pattern_ext = "" if pattern is None else f"-{pattern}"
        self.file_date = dt.datetime.now().date()
        out_file = open(self.out_path / f"{self.instrument.symbol()}{pattern_ext}-{self.file_date.strftime('%Y%m%d')}.csv", "a")
        return out_file

    def __update(self, update: Dict[str, Any]):
        """
        write a tick to the output file
        """
        if self.__change_file():
            self._data_file = self.__make_output_file()

        self._quote.update(update)
        self._data_file.write(self._quote.to_csv())
        self._data_file.write("\n")
        self._data_file.flush()
        if self._heartbeat is not None:
            self._heartbeat(self.instrument)
        self._tick_count += 1

    def __update_snapshot(self, update: Dict[str, Any]):
        """
        process a snapshot JSON message:
            1. write instrument to the metadata file
            2. also extract the quote and use it for the update
        """
        if self._quote is None:
            self._quote = Quote(update)

        self.__update(update["Snapshot"])

        self._metadata_file.write(json.dumps(update))
        self._metadata_file.write("\n")
        self._metadata_file.flush()

    def __call__(self, update: Dict[str, Any]):
        """
        callback handler for each update
        the update should contain either a Quote or Snapshot
        """
        try:
            if "Quote" in update:
                self.__update(update)
            elif "Snapshot" in update:
                self.__update_snapshot(update)
        except Exception:
            print("============================")
            print(update)
            import traceback

            traceback.print_exc()
            print("============================")


# ###
# split the instruments out of the CSV env string
# ###
def parse_instruments(raw_instr_string: str):
    instrs = []
    for entry in raw_instr_string.split(","):
        clean_str = entry.strip()
        if len(clean_str) > 0:
            instrs.append(entry.strip())
    return instrs


# ###
# # read and check config to make sure everything is sensible
# ###
def config():
    """
    read the config from environemnt variables
    """

    def read_env(var: str, raise_if_missing: bool = True, default_value=None) -> str:
        if var in os.environ:
            return os.environ[var]
        elif raise_if_missing:
            raise ValueError(f"missing environment varialble '{var}'")
        else:
            return default_value

    token_file = read_env("TOKEN_FILE")
    target_dir = read_env("DATA_DIR")
    raw_instruments = read_env("INSTRUMENTS")
    loop_sleep = read_env("SLEEP_PERIOD", raise_if_missing=False)
    hb_tolerrance = read_env("HB_TOLERANCE", raise_if_missing=False)
    if loop_sleep is None:
        loop_sleep = 5
    if hb_tolerrance is None:
        hb_tolerrance = 15
    instruments = parse_instruments(raw_instruments)
    return token_file, target_dir, instruments, loop_sleep, hb_tolerrance


# ####
# a heartbeat function for data readers to
# report they are still receiving data
# ####
last_tick = dt.datetime.now()
tick_info = {}


def heartbeat(instr: Instrument = None, n: int = None):
    # assignment is atomic in python
    global last_tick, tick_info
    last_tick = dt.datetime.now()

    if instr is not None:
        if instr.symbol() in tick_info:
            tick_info[instr.symbol()] += 1
        else:
            tick_info[instr.symbol()] = 0


executor = None


# ###
# # convenience forever loop
# ###
def heartbeat_monitor(sleep_period: int, hb_tol_s: int):
    global last_tick, executor, tick_info
    while 1 < 2:
        now = dt.datetime.now()
        hb_lag = now - last_tick
        print(
            f"{now.strftime('%Y.%m.%d %H:%M:%S')} last hb was  {hb_lag.seconds}.{hb_lag.microseconds:06d}s "
            f"ago (tolerance is {hb_tol_s}s). #s: {tick_info}"
        )
        if hb_lag.seconds > hb_tol_s:
            print(f"ERROR. Heartbeat older than {hb_tol_s}s. Exiting")
            kill_executor_threads(executor)
            sys.exit(-1)
        else:
            time.sleep(sleep_period)


# ###
# mainline
# ###
def mainline():
    global executor
    # get config
    token_file, output_dir, instruments, loop_sleep, hb_max_tolerance = config()

    executor = exec(max_workers=10)

    client = SaxoClient(token_file=token_file)

    # subscribe to each instrument and dispatch to the thread pool
    for i in instruments:
        instr =  InstrumentUtil.parse(i)
        executor.submit(client.subscribe_price, instr, DataWriter(output_dir, instr, heartbeat))

    # wait until stop
    heartbeat_monitor(loop_sleep, hb_max_tolerance)


if __name__ == "__main__":
    mainline()
