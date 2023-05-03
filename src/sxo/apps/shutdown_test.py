# -*- coding: utf-8 -*-
from genericpath import exists
import os, sys, signal
import datetime as dt
from threading import current_thread
import numpy as np
from sxo.util.threads import kill_thread
from sxo.util.threads import kill_executor_threads
import time
import datetime as dt
from typing import Any
from typing import Dict
from typing import Callable
from pathlib import Path

from concurrent.futures import ThreadPoolExecutor as exec


# ####
# a heartbeat function for data readers to
# report they are still receiving data
# ####
last_tick = dt.datetime.now()    

def heartbeat():
    # assignment is atomic in python
    global last_tick
    last_tick = dt.datetime.now()

executor = None
futures = []

def heartbeat_monitor():
    global last_tick, executor, writers
    print(f" --- EXIT ---")
    sys.exit(0)

# ######
#
# ######

# ###
# mainline
# ###
def mainline():
    global executor, writers
    # get config

    executor = exec(max_workers=10)

    def foo(i):
        for j in range(10):
            time.sleep(1)
            print(f"{i} : {j}")

    # subscribe to each instrument and dispatch to the thread pool
    for i in range(5):
        fut = executor.submit(foo, i)
        futures.append(fut)


    print(f" === PRE ===")
    time.sleep(5)
    print(f" === POST ===")

    kill_executor_threads(executor)
    
    # wait until stop
    heartbeat_monitor()

if __name__ == "__main__":
    mainline()