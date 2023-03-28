# -*- coding: utf-8 -*-
from pprint import pprint

from sxo.interface.client import SaxoClient

if __name__ == "__main__":
    client = SaxoClient()

    orders = client.list_orders()
    pprint(orders)
    order_ids = [o["OrderId"] for o in orders["Data"]]
    for oid in order_ids:
        client.delete_orders(oid)
