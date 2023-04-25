# -*- coding: utf-8 -*-
import json
from abc import ABC
from abc import abstractmethod
from pathlib import Path
from typing import Dict
from typing import List
from typing import Set
from typing import Union

class Instrument(ABC):
    @staticmethod
    def parse(sym:str):
        try:
            assetClass, symbol = sym.split("::")
        except ValueError as ve:
            raise Exception("Error parsing instrument. Expecting string in form of <asset class>::<symbol>")
        #if assetClass is None:

    
    @abstractmethod
    def make_from_symbol():
        pass

class FxSpot(Instrument):
    """
    a wrapper for the FxSpot entity reference data
    """
#
    def get_asset_class():
        return "xxx"

# EQUITY symbology
class Equity(Instrument):

    def get_asset_class():
        return "xxx"


if __name__ == "__main__":
    for sym in ["Fx::USDGBP", ""]:
        s = Instrument.parse(sym)
        print(s)

