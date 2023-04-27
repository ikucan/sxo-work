# -*- coding: utf-8 -*-
import json
from abc import ABC
from abc import abstractmethod
from pathlib import Path
from typing import Dict
from typing import List
from typing import Set
from typing import Any
from typing import Union
from sxo.interface.entities.instruments import AssetClassDb
from sxo.interface.entities.instruments import FxSpotInstruments
from sxo.interface.entities.instruments import EquityInstruments
from pprint import pformat

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
                    raise Exception(f"unknown asset class {assetClass}. Must be one of: {Instrument.known_asset_classes}")
        except ValueError as ve:
            raise Exception("Error parsing instrument. Expecting string in form of <asset class>::<symbol>")
        #if assetClass is None:

    @staticmethod
    def find(uid:Union[str, int]) : # -> Instrument
        '''
        find an instrument if you have an id already... this is fairly stupid, just looks up the id in each database
        we assume here that an instrument id ("Identifier") is globally unique. wlhen checked, this seems to hold 
        but have not seen it stated
        '''
        try:
            iid = int(uid)
            if FxSpotInstruments.has_id(iid):
                json = FxSpotInstruments.get_by_id(iid)
                return FxSpot(json['Symbol'])
            elif EquityInstruments.has_id(iid):
                json = EquityInstruments.get_by_id(iid)
                return EquityInstruments(json['Symbol'])
            else:
                raise Exception(f"Id {iid} does not exist in any known universe: [FxSpot, Equity]")
             
        except ValueError as ve:
            raise Exception("Error parsing instrument id. Expecting a integer (123) or a number string ('123')")
        #if assetClass is None:


    def __init__(self, symbol:str, symbology:AssetClassDb):
        if symbol not in symbology.all_instruments():
            raise Exception(f"ERROR: Instrument {symbol} not known in symbology for asset class {symbology.get_asset_class()}. Use one of {symbology.all_instruments()}")
        self._symbol = symbol
        self._canonical_asset_class = symbology.get_asset_class()
        self._json = symbology.get_instrument(symbol)

    def uid(self) -> str:
        return self._json['Identifier']

    def symbol(self) -> str:
        return self._symbol

    def descr(self) -> str:
        return self._json['Description']

    def asset_class(self) -> Dict[Any, Any]:
        return self._canonical_asset_class
    
    def __repr__(self) -> str:
        return pformat(self._json, indent=2)

    def __str__(self) -> str:
        return f"{self.asset_class()}::{self.symbol()}::{self.uid()}. {self.descr()}."

    
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
    for sym in ["Fx::GBPEUR", "Fx::GBPJPY" , "Fx::GBPUSD" , "Fx::USDJPY" , "Fx::EURAUD" , "Fx::EURGBP" , ]:
        s1 = Instrument.parse(sym)
        print(s1)
        s2 = Instrument.find(s1.uid())
        print(s2)

