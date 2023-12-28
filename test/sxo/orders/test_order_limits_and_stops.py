# -*- coding: utf-8 -*-
from pprint import pprint

from sxo.interface.client import SaxoClient
from sxo.interface.definitions import OrderDirection

if __name__ == "__main__":
    client = SaxoClient(token_file = "/data/saxo_token")

    oid = client.limit_order("FxSpot::GBPEUR",
                             OrderDirection.Sell,
                             1.18069,
                             1.15465,
                             10000,
                             stop_price =1.18070,
                             reference_id= "123",
    )
    
    print(oid)
    order_json = client.order_details(oid["OrderId"])
    pprint(order_json)
    related_stop = [o for o in order_json['Data'] if o['OpenOrderType'] == 'Stop'][0]

