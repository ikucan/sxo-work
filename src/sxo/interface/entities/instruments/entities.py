# -*- coding: utf-8 -*-
import json
from abc import ABC
from abc import abstractmethod
from pathlib import Path
from typing import Dict
from typing import List
from typing import Set
from typing import Union
from sxo.interface.entities.instruments import AssetClassDb
from sxo.interface.entities.instruments import FxSpotInstruments

class Instrument(ABC):

    known_asset_classes = {"Fx", "FxSpot", "FxForward", "FxSpot", "FxOption", "Stock", "Equity", "Eq", "StockIndex", "StockIndexOption", "StockOption", "CfdOnFutures", "CfdOnIndex", "CfdOnStock"}

    @staticmethod
    def parse(sym:str) : # -> Instrument
        '''
        Static method to parse an instrument from a string description. String is expected
        to be of the form <Asset Class>::<Instrument Id Valid in that asset class>.
        If multiple "::" delineators are contained in the string, the first one is used
        to separate the asset class from instrument description. hence asset class ids cannot
        contain a "::"
        '''
        try:
            assetClass, symbol = sym.split("::")
            
            match assetClass:
                case "Fx" :
                    return FxSpot(symbol)
                case other:
                    raise Exception(f"unknown asset class {assetClass}. Must be one of: {known_asset_classes}")
        except ValueError as ve:
            raise Exception("Error parsing instrument. Expecting string in form of <asset class>::<symbol>")
        #if assetClass is None:

    def __init__(self, instr:str, symbology:AssetClassDb):
        if instr not in symbology.all_instruments():
            raise Exception(f"ERROR: Instrument {instr} not known in symbology for asset class {symbology.get_asset_class()}. Use one of {symbology.all_instruments()}")
        self._canonical_asset_class = symbology.get_asset_class()
        self._json = symbology.get_instrument()

    def __repr__(self):
        return "XXXX"

    
class FxSpot(Instrument):
    """
    a wrapper for the FxSpot entity reference data
    """
    def __init__(self, pair:str):
        super().__init__(pair, FxSpotInstruments)
        pass


class Equity(Instrument):
    pass

if __name__ == "__main__":
    for sym in ["Fx::GBPUSD"]:
        s = Instrument.parse(sym)
        print(s)

