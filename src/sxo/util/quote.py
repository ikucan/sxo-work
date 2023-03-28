from typing import Dict
from typing import Any

class QuoteError(Exception):
    pass

class Quote:

    @staticmethod
    def __check(expected_key:str, parent_key:str, data: Dict[str, Any]):
        if expected_key not in data:
            raise QuoteError(f"Constructor expecting element '{expected_key}' in '{parent_key}' dict")

    def __init__(self, update: Dict[str, Any]):
        Quote.__check("Snapshot", "<root>", update)

        snapshot = update['Snapshot']
        Quote.__check("LastUpdated", "Snapshot", snapshot)
        Quote.__check("Quote", "Snapshot", snapshot)

        quote = snapshot['Quote']
        Quote.__check("Bid", "Quote", quote)
        Quote.__check("BidSize", "Quote", quote)
        Quote.__check("Ask", "Quote", quote)
        Quote.__check("AskSize", "Quote", quote)

        self.update(snapshot)


    def update(self, snapshot: Dict[str, Any]):
        if "LastUpdated" in snapshot:
            self._t = snapshot["LastUpdated"]

        if "Quote" in snapshot:
            quote = snapshot['Quote']
            if "Bid" in quote:
                self._bid = quote["Bid"]
            if "BidSize" in quote:
                self._bsz = quote["BidSize"]
            if "Ask" in quote:
                self._ask = quote["Ask"]
            if "AskSize" in quote:
                self._asz = quote["AskSize"]

    def to_csv(self,):
        return f"{self._t},{self._bid},{self._bsz},{self._ask},{self._asz}"

# {
#     "ContextId": "a8G3iiMG_WB64Lut3E9MgQ",
#     "Format": "application/json",
#     "InactivityTimeout": 30,
#     "ReferenceId": "2SO2lVx9Opk",
#     "RefreshRate": 1000,
#     "Snapshot": {
#         "AssetType": "FxSpot",
#         "LastUpdated": "2023-03-20T19:40:12.897000Z",
#         "PriceSource": "SBFX",
#         "Quote": {
#             "Amount": 10000,
#             "Ask": 1.14499,
#             "AskSize": 873480.0,
#             "Bid": 1.14462,
#             "BidSize": 1747080.0,
#             "DelayedByMinutes": 0,
#             "ErrorCode": "None",
#             "MarketState": "Open",
#             "Mid": 1.144805,
#             "PriceSource": "SBFX",
#             "PriceSourceType": "Firm",
#             "PriceTypeAsk": "Tradable",
#             "PriceTypeBid": "Tradable",
#             "RFQState": "None"
#             },
#          "Uic": 3942
#     },
#     "State": "Active",
#     "_instrument": "GBPEUR"}
    