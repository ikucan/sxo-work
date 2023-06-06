# -*- coding: utf-8 -*-
import json
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Set


class InstrumentDb:
    def __init__(self, asset_type: str, _json: Dict | str | Path | None):
        if asset_type is None:
            raise ValueError("you must pass a valid asset_type parameter")

        self._asset_class = asset_type
        # if none, look for the asset class relevant json db
        if _json is None:
            _json = Path(__file__).parent / f"{self._asset_class}.json"
            if not _json.exists():
                raise ValueError("No asssed db json passed. Using default {self._asset_type}.json did not work.")

        if isinstance(_json, Dict):
            self._database = _json["Data"]
        elif isinstance(_json, str):
            self._database = json.loads(_json)["Data"]
        elif isinstance(_json, Path):
            self._database = json.load(open(_json.as_posix()))["Data"]
        else:
            raise ValueError(
                "parameter _json needs to be either a" " parsed json dict, a Path to file or a" " string containing unparsed json"
            )

        self._by_symbol = {x["Symbol"]: x for x in self._database}

        # arrange instruments by symbol. must allow for mutliple instrumetns per symbol. e.g. mutiple
        # listings for an equity. keep a list of instruments indexed by symbol
        # self._by_symbol = dict()
        # symbols should be unique
        # for instr in self._database:
        #     sym = instr["Symbol"]
        #     self._by_symbol.setdefault(sym, []).append(instr)

        self._by_id = {x["Identifier"]: x for x in self._database}

        asset_types = {x["AssetType"] for x in self._database}
        if len(asset_types) != 1:
            raise ValueError(f"expected single asset type, got : {asset_types}")
        if self._asset_class not in asset_types:
            raise ValueError(f"expected {self._asset_class} as the asset type, got : {asset_types}")

    def get_asset_class(
        self,
    ) -> str:
        return self._asset_class

    def all_instruments(
        self,
    ) -> Set[str]:
        return set(self._by_symbol.keys())

    def has_instrument(
        self,
        instrument: str,
    ) -> bool:
        return instrument in self.all_instruments()

    def all_ids(
        self,
    ) -> Set[str]:
        return set(self._by_id.keys())

    def has_id(
        self,
        id: int,
    ) -> bool:
        return id in self.all_ids()

    def get_instrument(
        self,
        instrument: str,
    ) -> Dict[Any, Any]:
        if not self.has_instrument(instrument):
            raise ValueError(f"unknown instrument: {instrument}")
        return self._by_symbol[instrument]

    def get_by_id(
        self,
        id: int,
    ) -> Dict:
        if not self.has_id(id):
            raise ValueError(f"unknown instrument ID: {id}")
        return self._by_id[id]


# TODO:>> ik:>> make singleton, ensure thread safety
# from singleton_decorator import singleton
# @singleton
class FxSpotSyms(InstrumentDb):
    """
    a wrapper for the FxSpot entity reference data
    """

    def __init__(self, _json: Dict | str | Path | None = None):
        super().__init__(asset_type="FxSpot", _json=_json)


# EQUITY symbology
class EquitySyms(InstrumentDb):
    """
    a wrapper for the FxSpot entity reference data
    """

    def __init__(self, _json: Dict | str | Path | None = None):
        super().__init__(asset_type="Stock", _json=_json)
