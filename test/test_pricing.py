# -*- coding: utf-8 -*-
'''
this is a legacy test for a legacy function
use client.info_price instead
'''

import time
from pprint import pprint

from sxo.interface.client import SaxoClient

# if __name__ == "__main__":
#     client = SaxoClient()

#     while 1 < 2:
#         l1 = client.info_spotfx_prices(["GBPEUR",])
#         l2 = client.info_spotfx_prices(["USDJPY"])
# #        # pprint(client.info_spotfx_prices("GBPEUR"))
#         time.sleep(2)
#     pass
#     # pprint(client.info_spotfx_prices(["GBPEUR", "GBPUSD", "USDJPY"]))



if __name__ == "__main__":
    client = SaxoClient()

    #l1 = client.info_price(["FxSpot::GBPEUR", "FxSpot::GBPJPY" , "Equity::TSLA:xmil", "Stock::TL0:xetr",])
    l1 = client.info_price(["FxSpot::GBPEUR"])
    i = 123
