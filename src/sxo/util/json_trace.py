# -*- coding: utf-8 -*-
import datetime as dt
from pathlib import Path


class JsonLogger:
    def __init__(self, *, trace_location: str, level: int = 0):
        if Path(trace_location).exists():
            raise ValueError(f"trace path does not exists: {trace_location}")
        pass

    def _now_str(
        self,
    ) -> str:
        return dt.datetime.now().strftime("%Y.%m.%d_%H.%M.%S.%f")
