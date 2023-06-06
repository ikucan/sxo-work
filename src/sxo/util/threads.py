# -*- coding: utf-8 -*-
import ctypes
from concurrent.futures import ThreadPoolExecutor


def kill_thread(thread):
    """
    Terminates a python thread from another thread.

    :param thread: a threading.Thread instance
    """

    if not thread.is_alive():
        return

    exc = ctypes.py_object(SystemExit)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread.ident), exc)
    if res == 0:
        raise ValueError("nonexistent thread id")
    elif res > 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def kill_executor_threads(executor: ThreadPoolExecutor):
    for t in executor._threads:
        kill_thread(t)
