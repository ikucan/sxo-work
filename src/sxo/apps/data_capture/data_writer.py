# -*- coding: utf-8 -*-
import datetime as dt
import json
import os
import sys
import time
from pathlib import Path
from typing import Any
from typing import Callable
from typing import Dict
from sxo.interface.entities.instruments import Instrument
from sxo.util.quote import Quote
from sxo.util.threads import kill_executor_threads


class DataWriterError(BaseException):
    pass

# ###
# # tick data writer class for each instrument
# ###
class DataWriter:
    def __init__(self, out_dir: str, instr: Instrument, heartbeat: Callable | None = None):
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
        self._quote: Quote | None = None
        self._heartbeat = heartbeat
        self._tick_count = 0

    def __change_file(
        self,
    ):
        """
        check current date v date of current file
        """
        return self.file_date < dt.datetime.now().date()

    def __make_output_file(self, pattern: str | None = None):
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

        self._quote.update(update)  # type: ignore
        self._data_file.write(self._quote.to_csv())  # type: ignore
        self._data_file.write("\n")
        self._data_file.flush()
        if self._heartbeat is not None:
            self._heartbeat()
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

