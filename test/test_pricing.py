# -*- coding: utf-8 -*-
'''
this is a legacy test for a legacy function
use client.info_price instead
'''

import time
from pprint import pprint

from sxo.interface.client import SaxoClient

if __name__ == "__main__":
    client = SaxoClient()

    while 1 < 2:
        pprint(client.info_spotfx_prices("GBPEUR"))
        time.sleep(2)
    pass
    # pprint(client.info_spotfx_prices(["GBPEUR", "GBPUSD", "USDJPY"]))

