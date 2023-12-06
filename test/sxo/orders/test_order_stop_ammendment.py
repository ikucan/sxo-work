# -*- coding: utf-8 -*-
from pprint import pprint

from sxo.interface.client import SaxoClient
from sxo.interface.definitions import OrderDirection

if __name__ == "__main__":
    client = SaxoClient(token_file = "/data/saxo_token")
    all_orders = client.list_orders()

    pprint(all_orders['Data'])
    for o in all_orders['Data']:
        if o['OpenOrderType'] == 'Stop' and o['Status'] == 'Working':
            res = client.modify_order(
                order = o,
                price = o['Price'] + 0.1,
            )
            print(f"modified: {res}")
