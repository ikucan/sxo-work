# -*- coding: utf-8 -*-
from genericpath import exists
import os
import datetime as dt
import numpy as np
import json
import time
import datetime as dt
from typing import Any
from typing import Dict
from pathlib import Path

#from concurrent.futures import ProcessPoolExecutor as exec
from concurrent.futures import ThreadPoolExecutor as exec

from sxo.interface.client import SaxoClient
from sxo.util.quote import Quote

# ###
# # convenience forever loop
# ###
def foreva(sleep_period:int):
    while 1 < 2:
        print(f"{dt.datetime.now().strftime('%Y.%m.%d %H:%M:%S')}")
        time.sleep(10 if sleep_period is None else sleep_period)


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

    def __init__(self, out_dir: str, instr:str):
        '''
        check output details and crate output writer
        '''
        data_path = Path(out_dir)
        if not data_path.exists():
            raise DataWriterError(f"output location must exist: {out_dir}")

        self.out_path = data_path / instr
        Path(self.out_path).mkdir(parents=True, exist_ok=True)


        self.instrument = instr


        self._metadata_file = self.__make_output_file("metadata")
        self._data_file = self.__make_output_file()
        self._quote = None

    def __change_file(self,):
        '''
        check current date v date of current file
        '''
        return self.file_date < dt.datetime.now().date()

    def __make_output_file(self, pattern:str = None):
        '''
        create an output file 
        '''
        pattern_ext = "" if pattern is None else f"-{pattern}"
        self.file_date = dt.datetime.now().date()
        out_file = open(self.out_path / f"{self.instrument}{pattern_ext}-{self.file_date.strftime('%Y%m%d')}.csv", "a")
        return out_file

    def __update(self, update: Dict[str, Any]):
        '''
        write a tick to the output file
        '''
        if self.__change_file():
            self._data_file = self.__make_output_file()

        self._quote.update(update)
        self._data_file.write(self._quote.to_csv())
        self._data_file.write("\n")
        self._data_file.flush()

    def __update_snapshot(self, update: Dict[str, Any]):
        '''
        process a snapshot JSON message:
            1. write instrument to the metadata file
            2. also extract the quote and use it for the update
        '''
        if self._quote is None:
            self._quote = Quote(update)

        self.__update(update["Snapshot"])

        self._metadata_file.write(json.dumps(update))
        self._metadata_file.write("\n")
        self._metadata_file.flush()

    def __call__(self, update: Dict[str, Any]):
        '''
        callback handler for each update
        the update should contain either a Quote or Snapshot
        '''
        try:
            if "Quote" in update:
                self.__update(update)
            elif "Snapshot" in update:
                self.__update_snapshot(update)
        except Exception as e:
            print("============================")
            print(update)
            import traceback
            traceback.print_exc()
            print("============================")

# ###
# split the instruments out of the CSV env string
# ###
def parse_instruments(raw_instr_string:str):
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
    '''
    read the config from environemnt variables
    '''
    def read_env(var:str, raise_if_missing:bool = True, default_value=None) -> str:
        if var in os.environ:
            return  os.environ[var]
        elif raise_if_missing:
            raise ValueError(f"missing environment varialble '{var}'")
        else:
            return default_value

    token_file = read_env('TOKEN_FILE')
    target_dir = read_env('DATA_DIR')
    raw_instruments = read_env('INSTRUMENTS')
    loop_sleep = read_env('SLEEP_PERIOD', raise_if_missing= False)
    instruments = parse_instruments(raw_instruments)
    return token_file, target_dir, instruments, loop_sleep

# ###
# mainline
# ###
def mainline():
    # get config
    token_file, output_dir, instruments, loop_sleep = config()

    # make the thread pool and connect to sxo
    executor = exec(max_workers=10)   
    client = SaxoClient(token_file = token_file)

    # subscribe to each instrument and dispatch to the thread pool
    for instr in instruments:
        executor.submit(client.subscribe_fx_spot, instr,  DataWriter(output_dir, instr))

    # wait until stop
    foreva(loop_sleep)

if __name__ == "__main__":
    mainline()
