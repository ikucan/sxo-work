# -*- coding: utf-8 -*-
from pprint import pprint
from sxo.interface.definitions import OrderDirection

from sxo.interface.client import SaxoClient

if __name__ == "__main__":
    client = SaxoClient()

    oid = client.limit_order("FxSpot::GBPEUR", OrderDirection.Buy, 1.12, 1.13, 10000)
    #oid = client.buy_fx_spot("EURGBP", 0.88002, 1000000)
    print(oid)
    pprint(client.order_details(oid["OrderId"]))
