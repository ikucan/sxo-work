# -*- coding: utf-8 -*-
import json
from pathlib import Path
from typing import Dict
from typing import List
from typing import Set
from typing import Union


class JsonDataBase:
    def __init__(self, asset_type: str, _json: Union[Dict, str, Path, None]):
        if asset_type is None:
            raise ValueError("you must pass a valid asset_type parameter")

        self._asset_type = asset_type
        # if none, look for the asset class relevant json db
        if _json is None:
            _json = Path(__file__).parent / f"{self._asset_type}.json"
            if not _json.exists():
                raise ValueError("No asssed db json passed. Using default {self._asset_type}.json did not work.")

        if isinstance(_json, Dict):
            self._data = _json["Data"]
        elif isinstance(_json, str):
            self._data = json.loads(_json)["Data"]
        elif isinstance(_json, Path):
            self._data = json.load(open(_json.as_posix()))["Data"]
        else:
            raise ValueError(
                "parameter _json needs to be either a" " parsed json dict, a Path to file or a" " string containing unparsed json"
            )


class FxSpot(JsonDataBase):
    """
    a wrapper for the FxSpot entity reference data
    """

    def __init__(self, _json: Union[Dict, str, Path, None] = None):
        super().__init__(asset_type="FxSpot", _json=_json)
        self._by_pair = {x["Symbol"]: x for x in self._data}
        self._all_pairs = set(self._by_pair.keys())
        asset_types = {x["AssetType"] for x in self._data}
        if len(asset_types) != 1:
            raise ValueError(f"expected single asset type, got : {asset_types}")
        if self._asset_type not in asset_types:
            raise ValueError(f"expected FxSpot as the asset type, got : {asset_types}")

    def get_asset_type(
        self,
    ) -> str:
        return self._asset_type

    def all_pairs(
        self,
    ) -> Set[str]:
        return self._all_pairs

    def has_pair(
        self,
        pair: str,
    ) -> bool:
        return pair in self._all_pairs

    def get_pair(
        self,
        pair: str,
    ) -> Dict:
        if pair not in self._by_pair:
            raise ValueError(f"unknown pair: {pair}")
        return self._by_pair[pair]

    def get_instrument_id(
        self,
        pair: Union[str, List[str]],
    ) -> Union[int, List]:
        if isinstance(pair, List):
            return [self.get_instrument_id(p) for p in pair]

        instrument = self.get_pair(pair)
        if "Identifier" not in instrument:
            raise ValueError(f"unknown property: {pair}")
        return instrument["Identifier"]


# if __name__ == "__main__":
#     spot = FxSpot()
#     print(spot.get_instrument_id("GBPUSD"))
#     print(spot.get_instrument_id(["GBPUSD", "EURGBP","USDJPY"]))
