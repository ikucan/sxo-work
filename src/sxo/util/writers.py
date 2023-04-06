# -*- coding: utf-8 -*-
import json
from typing import Any
from typing import Dict

import numpy as np


class DataWriter:
    def __init__(self, out_file: str, strategy):
        self._out_file = open(out_file, "a")
        self._t = np.datetime64()
        self.strategy = strategy
        pass

    def __call__(self, update: Dict[str, Any], flush: bool = True):
        self._out_file.write(json.dumps(update))
        self._out_file.write("\n")
        if flush:
            self._out_file.flush()
