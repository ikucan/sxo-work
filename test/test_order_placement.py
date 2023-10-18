# -*- coding: utf-8 -*-
from pprint import pprint

from sxo.interface.client import SaxoClient
from sxo.interface.definitions import OrderDirection

if __name__ == "__main__":
    client = SaxoClient(token_file = "/data/saxo_token")

    # oid = client.limit_order("FxSpot::GBPEUR", OrderDirection.Buy, 1.14, 1.152, 1000000)
    # print(oid)
    # pprint(client.order_details(oid["OrderId"]))

    oid = client.limit_order("FxSpot::GBPEUR", OrderDirection.Sell, 1.15476, 1.15465, 10000)
    
    print(oid)
    pprint(client.order_details(oid["OrderId"]))
