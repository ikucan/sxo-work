# -*- coding: utf-8 -*-
import datetime as dt
import re
from abc import ABC
from abc import abstractmethod
from io import StringIO
from pathlib import Path
from pprint import pformat
from typing import Any
from typing import Dict
from typing import List
from typing import Set
from typing import Type

from sxo.interface.definitions import AssetType
from sxo.interface.entities.instruments import AssetClassDb
from sxo.interface.entities.instruments import EquityInstruments
from sxo.interface.entities.instruments import FxSpotInstruments

# from sxo.interface.entities.instruments import AssetClassDb


class Instrument(ABC):
    def __init__(self, json: Dict[Any, Any]):
        # assume a single dict or list of dicts, treat all as a list
        self._json = json
        self.__set_detail()
        self.__check_detail()

    def __set_detail(self):
        self._symbol = self._json["Symbol"]
        self._canonical_asset_class = self._json["AssetType"]
        self._uid = self._json["Identifier"]
        self._gid = self._json["GroupId"]
        self._descr = self._json["Description"]

    def __check_detail(self):
        assert self._canonical_asset_class == self.asset_type().name

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

    def asset_class(self) -> str:
        return self._canonical_asset_class

    @abstractmethod
    def asset_type(self) -> AssetType:
        ...

    def path(self, root: str | Path | None = None, ext: str | None = None, dated: bool = False):
        base = Path(self.asset_class())
        fname = re.sub(":", "_", self.symbol())
        ext = f".{ext}" if ext is not None else ""
        ext = f"_{dt.datetime.now().strftime('%Y%m%d')}{ext}" if dated else ext
        rel = base / f"{fname}{ext}"
        return rel if root is None else root / rel

    def __repr__(self) -> str:
        return pformat(self._json, indent=2)

    def __str__(self) -> str:
        return f"{self.asset_class()} # {self.symbol()} # {self.uid()} # {self.descr()}."

    def __eq__(self, other):
        return isinstance(other, Instrument) and self.uid() == other.uid()

    def __ne__(self, other):
        return not self == other


class FxSpot(Instrument):
    """
    a wrapper for the FxSpot reference data
    """

    def __init__(self, metadata: Dict[Any, Any]):
        super().__init__(metadata)

    def asset_type(self) -> AssetType:
        return AssetType.FxSpot


class Equity(Instrument):
    def __init__(self, metadata: Dict[Any, Any]):
        super().__init__(metadata)

    def asset_type(self) -> AssetType:
        return AssetType.Stock

    def exchange(self) -> str:
        return self._json["ExchangeId"]

    def primary_listing_id(self) -> str:
        return self._json["PrimaryListing"]

    def __str__(self) -> str:
        return (
            f"{self.asset_class()} # {self.symbol()} # {self.exchange()} # "
            f"{self.uid()}/{self.primary_listing_id()} # {self.gid()} # {self.descr()}."
        )


class InstrumentGroup:
    def __init__(self, instruments: List[str]):
        self._instruments = [InstrumentUtil.parse(i) for i in instruments]
        self._by_asset_class: Dict[str, Any] = {}
        for i in self._instruments:
            self._by_asset_class.setdefault(i.asset_class(), []).append(i)

    def asset_classes(self) -> Set[str]:
        return set(self._by_asset_class.keys())

    def get_by_asset_class(self, asset_class: str):
        if asset_class in self._by_asset_class:
            return self._by_asset_class[asset_class]
        else:
            raise ValueError(f"Unknown asset class: {asset_class}")

    def all(
        self,
    ):
        return self._instrumennts

    def __repr__(self) -> str:
        buffer = StringIO()
        for ac in self.asset_classes():
            buffer.write(f"{ac}\n")
            for instr in self.get_by_asset_class(ac):
                buffer.write(f"  {instr} \n")
            pass
        return buffer.getvalue()


class InstrumentUtil:
    known_asset_classes = {
        "FxSpot",
        "FxForward",
        "FxSpot",
        "FxOption",
        "Stock",
        "StockIndex",
        "StockIndexOption",
        "StockOption",
        "CfdOnFutures",
        "CfdOnIndex",
        "CfdOnStock",
    }

    @staticmethod
    def __parse_one(sym: str):  # -> Instrument
        """
        Static method to parse an instrument from a string description. String is expected
        to be of the form <Asset Class>::<Instrument Id Valid in that asset class>.
        If multiple "::" delineators are contained in the string, the first one is used
        to separate the asset class from instrument description. hence asset class ids cannot
        contain a "::"
        """
        try:
            asset_class, symbol = sym.split("::")

            symbology: AssetClassDb
            type_class: Type[Instrument]

            match asset_class:
                case "FxSpot":
                    symbology, type_class = FxSpotInstruments, FxSpot
                case "Equity" | "Stock":
                    symbology, type_class = EquityInstruments, Equity
                case _:
                    raise Exception(f"unknown asset class {asset_class}. Must be one of: {InstrumentUtil.known_asset_classes}")
            if not symbology.has_instrument(symbol):
                raise Exception(f"Instrument {symbol} is not known in (known) asset class {asset_class}")
            else:
                instrMetadata = symbology.get_instrument(symbol)
                return type_class(instrMetadata)
        except ValueError:
            raise Exception("Error parsing instrument. Expecting string in form of <asset class>::<symbol>")

    @staticmethod
    def parse(sym: str | List[str]):  # -> Instrument
        if isinstance(sym, str):
            return InstrumentUtil.__parse_one(sym)
        elif isinstance(sym, list):
            return InstrumentGroup(sym)
        else:
            raise ValueError(f"sym parameter must be a string or a list. you passed: {type(sym)}")

    @staticmethod
    def parse_grp(sym: str | List[str]):  # -> Instrument
        if isinstance(sym, str):
            return InstrumentGroup([sym])
        elif isinstance(sym, list):
            return InstrumentGroup(sym)
        else:
            raise ValueError(f"sym parameter must be a string or a list. you passed: {type(sym)}")

    @staticmethod
    def find(uid: int):  # -> Instrument
        """
        find an instrument if you have an id already... this is fairly stupid, just looks up the id in each databas
        we assume here that an instrument id ("Identifier") is globally unique. wlhen checked, this seems to hold
        but have not seen it stated
        """
        try:
            iid = int(uid)
            if FxSpotInstruments.has_id(iid):
                return FxSpot(FxSpotInstruments.get_by_id(iid))
            elif EquityInstruments.has_id(iid):
                return Equity(EquityInstruments.get_by_id(iid))
            else:
                raise Exception(f"Id {iid} does not exist in any known universe: [FxSpot, Equity]")

        except ValueError:
            raise Exception("Error parsing instrument id. Expecting a integer (123) or a number string ('123')")
        # if assetClass is None:


if __name__ == "__main__":
    for sym in [
        "FxSpot::GBPEUR",
        "FxSpot::GBPJPY",
        "FxSpot::GBPUSD",
        "FxSpot::USDJPY",
        "FxSpot::EURAUD",
        "FxSpot::EURGBP",
    ]:
        print("----------")
        s1 = InstrumentUtil.parse(sym)
        print(s1)
        s2 = InstrumentUtil.find(s1.uid())
        print(s2)
        print(s2.path(root="/data", ext="ccsv"))
        print(s1 != s2)

    # # for sym in ["Equity::TSLA:xmil", "Stock::TL0:xetr", ]:
    # #     print("----------")
    # #     s1 = InstrumentUtil.parse(sym)
    # #     print(s1)
    # #     s2 = InstrumentUtil.find(s1.uid())
    # #     print(s2)
    # #     print(s2.path(root="/data", ext="ccsv", dated=True))
    # #     assert(s1 == s2)

    # group = InstrumentUtil.parse(
    #     [
    #         "FxSpot::GBPEUR",
    #         "FxSpot::GBPJPY",
    #         "Equity::TSLA:xmil",
    #         "Stock::TL0:xetr",
    #     ]
    # )
    # print(group)
