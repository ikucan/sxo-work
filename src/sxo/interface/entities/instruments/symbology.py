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
#from sxo.interface.entities.instruments import AssetClassDb
from sxo.interface.entities.instruments import FxSpotInstruments
from sxo.interface.entities.instruments import EquityInstruments
from pprint import pformat

class Instrument(ABC):

    def __init__(self, json:Dict[Any, Any]):
        # assume a single dict or list of dicts, treat all as a list        
        self._json = json
        self.__set_detail()

    def __set_detail(self):
        self._symbol = self._json["Symbol"]
        self._canonical_asset_class = self._json["AssetType"]
        self._uid = self._json["Identifier"]
        self._gid = self._json["GroupId"]
        self._descr = self._json["Description"]

    # @abstractmethod
    # def uid(self) -> str:
    #     ...
    def uid(self) -> str:
        return self._uid        

    def gid(self) -> str:
        return self._gid        

    def symbol(self) -> str:
        return self._symbol

    def descr(self) -> str:
        return self._descr

    def asset_class(self) -> Dict[Any, Any]:
        return self._canonical_asset_class
    
    def __repr__(self) -> str:
        return pformat(self._json, indent=2)

    def __str__(self) -> str:
        return f"{self.asset_class()} # {self.symbol()} # {self.uid()} # {self.descr()}."
    
    def __eq__(self, other) :
        return isinstance(other, Instrument) and \
            self.uid() == other.uid()

    def __ne__(self, other) :
        return not self == other
    
class FxSpot(Instrument):
    """
    a wrapper for the FxSpot reference data
    """
    def __init__(self, metadata:Dict[Any, Any]):
        super().__init__(metadata)


class Equity(Instrument):
    def __init__(self, metadata:Dict[Any, Any]):
        super().__init__(metadata)

    def exchange(self) -> str:
        return self._json['ExchangeId']

    def primary_listing_id(self) -> str:
        return self._json['PrimaryListing']

    def __str__(self) -> str:
        return f"{self.asset_class()} # {self.symbol()} # {self.exchange()} # {self.uid()}/{self.primary_listing_id()} # {self.gid()} # {self.descr()}."

class InstrumentGroup():
    def __init__(self, json:List[Dict[Any, Any]]):
        self._instruments = [j for j in json]
        self._instruments = [j for j in json]



    def exchange(self) -> str:
        return self._json['ExchangeId']

    def primary_listing_id(self) -> str:
        return self._json['PrimaryListing']

    def __str__(self) -> str:
        return f"{self.asset_class()} # {self.symbol()} # {self.exchange()} # {self.uid()}/{self.primary_listing_id()} # {self.gid()} # {self.descr()}."


class InstrumentUtil:

    known_asset_classes = {"FxSpot", "FxForward", "FxSpot", "FxOption", "Stock", "StockIndex", "StockIndexOption", "StockOption", "CfdOnFutures", "CfdOnIndex", "CfdOnStock"}

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
            asset_class, symbol = sym.split("::")
            
            match asset_class:
                case "FxSpot" :
                    symbology, type_class = FxSpotInstruments, FxSpot
                case "Equity" | "Stock" :
                    symbology, type_class = EquityInstruments, Equity
                case other:
                    raise Exception(f"unknown asset class {asset_class}. Must be one of: {Instrument.known_asset_classes}")
            if not symbology.has_instrument(symbol):
                raise Exception(f"Instrument {symbol} is not known in (known) asset class {asset_class}")
            else:
                instrMetadata = symbology.get_instrument(symbol)
                return type_class(instrMetadata)
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
                return Equity(EquityInstruments.get_by_id(iid))
            else:
                raise Exception(f"Id {iid} does not exist in any known universe: [FxSpot, Equity]")
             
        except ValueError as ve:
            raise Exception("Error parsing instrument id. Expecting a integer (123) or a number string ('123')")
        #if assetClass is None:


if __name__ == "__main__":
    for sym in ["Fx::GBPEUR", "Fx::GBPJPY" , "Fx::GBPUSD" , "Fx::USDJPY" , "Fx::EURAUD" , "Fx::EURGBP" , ]:
        print("----------")
        s1 = InstrumentUtil.parse(sym)
        print(s1)
        s2 = InstrumentUtil.find(s1.uid())
        print(s2)
        print(s1 != s2)

    for sym in ["Equity::TSLA:xmil", "Stock::TL0:xetr", ]:
        print("----------")
        s1 = InstrumentUtil.parse(sym)
        print(s1)
        s2 = InstrumentUtil.find(s1.uid())
        print(s2)
        assert(s1 == s2)    