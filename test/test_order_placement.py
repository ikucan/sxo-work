# -*- coding: utf-8 -*-
from pprint import pprint

from sxo.interface.client import SaxoClient

if __name__ == "__main__":
    client = SaxoClient()

    #oid = client.buy_fx_spot("GBPEUR", 1.12, 10000)
    oid = client.buy_fx_spot("EURGBP", 0.88002, 1000000)
    print(oid)
    pprint(client.order_details(oid["OrderId"]))
