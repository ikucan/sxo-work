# -*- coding: utf-8 -*-
from pprint import pprint

from sxo.interface.client import SaxoClient

if __name__ == "__main__":
    client = SaxoClient(token_file="/data/saxo_token")

    orders = client.list_orders()
    pprint(orders)
    order_ids = [o["OrderId"] for o in orders["Data"]]
    for oid in order_ids:
        print(oid)
        client.delete_orders(oid)
