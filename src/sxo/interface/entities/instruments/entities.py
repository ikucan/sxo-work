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
                    symbology, typeClass = FxSpotInstruments, FxSpot
                case other:
                    raise Exception(f"unknown asset class {assetClass}. Must be one of: {Instrument.known_asset_classes}")
            if not symbology.has_instrument(symbol):
                raise Exception("XXXXX")
            else:
                instrMetadata = symbology.get_instrument(symbol)
                return typeClass(instrMetadata)
        except ValueError as ve:
            raise Exception("Error parsing instrument. Expecting string in form of <asset class>::<symbol>")
        #if assetClass is None:

    @staticmethod
    def find(uid:Union[str, int]) : # -> Instrument
        '''
        find an instrument if you have an id already... this is fairly stupid, just looks up the id in each databas
        we assume here that an instrument id ("Identifier") is globally unique. wlhen checked, this seems to hold 
        but have not seen it stated
        '''
        try:
            iid = int(uid)
            if FxSpotInstruments.has_id(iid):
                return FxSpot(FxSpotInstruments.get_by_id(iid))
            elif EquityInstruments.has_id(iid):
                return FxSpot(FxSpotInstruments.get_by_id(iid))
            else:
                raise Exception(f"Id {iid} does not exist in any known universe: [FxSpot, Equity]")
             
        except ValueError as ve:
            raise Exception("Error parsing instrument id. Expecting a integer (123) or a number string ('123')")
        #if assetClass is None:


    def __init__(self, json:List[Dict[Any, Any]]):
        self._json = json
        self._symbol = json[0]["Symbol"]
        self._canonical_asset_class = json[0]["AssetType"]
        self._uid = json[0]["Identifier"]
        self._descr = json[0]["Description"]

    @abstractmethod
    def uid(self) -> str:
        ...

    def symbol(self) -> str:
        return self._symbol

    def descr(self) -> str:
        return self._descr

    def asset_class(self) -> Dict[Any, Any]:
        return self._canonical_asset_class
    
    def __repr__(self) -> str:
        return pformat(self._json, indent=2)

    def __str__(self) -> str:
        return f"{self.asset_class()}::{self.symbol()}::{self.uid()}. {self.descr()}."

    
class FxSpot(Instrument):
    """
    a wrapper for the FxSpot reference data
    """
    def __init__(self, metadata:Dict[Any, Any]):
        super().__init__(metadata)
        if len(self._json) != 1:
            raise Exception(f"Expecting excactly one instrumetn entry (json record) for instrument {self._symbol}")

    
    def uid(self) -> str:
        return self._uid        



class Equity(Instrument):
    """
    a wrapper for the Equity reference data
    """
    def __init__(self, metadata:Dict[Any, Any]):
        super().__init__(metadata)

if __name__ == "__main__":
    for sym in ["Fx::GBPEUR", "Fx::GBPJPY" , "Fx::GBPUSD" , "Fx::USDJPY" , "Fx::EURAUD" , "Fx::EURGBP" , ]:
        s1 = Instrument.parse(sym)
        print(s1)
        s2 = Instrument.find(s1.uid())
        print(s2)
