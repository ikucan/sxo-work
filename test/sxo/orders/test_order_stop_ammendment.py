# -*- coding: utf-8 -*-
from pprint import pprint

from sxo.interface.client import SaxoClient
from sxo.interface.definitions import OrderDirection

if __name__ == "__main__":
    client = SaxoClient(token_file = "/data/saxo_token")
    all_orders = client.list_orders()
    pprint(all_orders['Data'])
    for o in all_orders['Data']:
        stop_orders = [roo for roo in o['RelatedOpenOrders'] if roo['OpenOrderType'] == 'Stop']
        client.modify_order(
            order_id = stop_orders[0]['OrderId'],
            price = 1.1817,
            )


