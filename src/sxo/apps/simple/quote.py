# # -*- coding: utf-8 -*-
# import json
# from typing import Any
# from typing import Dict

# import numpy as np
# from sxo.interface.entities.instruments import Instrument


# class Quote:
#     def __init__(self, instr: Instrument):
#         self._instrument = instr
#         self._time = np.datetime64()
#         self._bid = np.nan
#         self._bsz = np.nan
#         self._ask = np.nan
#         self._asz = np.nan
#         self._mid = np.nan

#     def time_as_str(
#         self,
#     ) -> str:
#         return self._time.astype("datetime64[ms]").astype(str)

#     def update(self, json: Dict[Any, Any]):
#         if "LastUpdated" in json:
#             self._time = np.datetime64(json["LastUpdated"])

#         if "Quote" in json:
#             quote = json["Quote"]
#             if "Bid" in quote:
#                 self._bid = quote["Bid"]
#             if "BidSize" in quote:
#                 self._bsz = quote["BidSize"]
#             if "Ask" in quote:
#                 self._ask = quote["Ask"]
#             if "AskSize" in quote:
#                 self._asz = quote["AskSize"]
#             if "Mid" in quote:
#                 self._mid = quote["Mid"]

#     def to_json(
#         self,
#     ) -> Dict[Any, Any]:
#         i = self._instrument
#         return {
#             # 'instrument': f"{i.asset_type()}::{i.symbol()}",
#             "uic": f"{i.uid()}",
#             "t": f"{self._time}",
#             "bid": f"{self._bid}",
#             "bsz": f"{self._bsz}",
#             "ask": f"{self._ask}",
#             "asz": f"{self._asz}",
#             "mid": f"{self._mid}",
#         }

#     def __str__(
#         self,
#     ):
#         return json.dumps(self.to_json())
