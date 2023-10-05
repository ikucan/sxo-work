# -*- coding: utf-8 -*-
import datetime as dt
import sys
import time

from sxo.util.threads import kill_executor_threads


class HeartBeatMonitor:
    def __init__(self, executor, sleep_period: int, tolerance: int):
        self._executor = executor
        self._sleep = sleep_period
        self._hb_tolerance = tolerance

    def __loop(self):
        self._last_tick = dt.datetime.now() 
        while 1 < 2:
            now = dt.datetime.now()
            hb_lag = now - self._last_tick
            if hb_lag.seconds > self._hb_tolerance:
                print(f"ERROR. Heartbeat older than {self._hb_tolerance}s. Exiting")
                kill_executor_threads(self._executor)  # type: ignore
                sys.exit(-1)
            else:
                print(
                    f"{now.strftime('%Y.%m.%d %H:%M:%S')} last hb was  {hb_lag.seconds}.{hb_lag.microseconds:06d}s "
                    f"ago (tolerance is {self._hb_tolerance}s)."
                )
                time.sleep(self._sleep)

    def __call__(self):
        # assignment is atomic in python
        self._last_tick = dt.datetime.now()

    def start(self):
        self.__loop()
