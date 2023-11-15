# -*- coding: utf-8 -*-
from pprint import pprint

import numpy as np

from sxo.interface.client import SaxoClient
from sxo.interface.definitions import OrderDirection

if __name__ == "__main__":
    client = SaxoClient(token_file = "/data/saxo_token")

    t_exp = np.datetime64('now').astype('datetime64[m]').astype('datetime64[s]') + np.timedelta64(60, 's')

    oid = client.limit_order("FxSpot::GBPEUR",
                             OrderDirection.Sell,
                             1.18076,
                             1.15465,
                             10000,
                             reference_id= "xxx-yyy-zzz",
                             expiry_time = t_exp, )
    
    print(oid)
    pprint(client.order_details(oid["OrderId"]))
