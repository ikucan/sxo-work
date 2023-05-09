# -*- coding: utf-8 -*-
import time
from concurrent.futures import ThreadPoolExecutor as exec
from functools import partial
from pprint import pprint

from sxo.interface.client import SaxoClient


def foreva():
    while 1 < 2:
        print("4eva")
        time.sleep(10)


exectr = exec(max_workers=10)

# ###
# # TODO:>>  try one loop per thread
# # https://docs.python.org/3/library/asyncio-eventloop.html
# ###


class tick_handler:
    def __init__(self, instr: str):
        self.instr = instr

    def __call__(self, msg: str):
        msg["_instrument"] = self.instr
        pprint(msg)


if __name__ == "__main__":
    client = SaxoClient()

    def subscribe(instr: str):
        handler = tick_handler(instr)
        client.subscribe_fx_spot(instr, handler)

    def print_price(instr, quote):
        quote["_instr"] = instr
        print(quote)

    # # f1 = exectr.submit(client.subscribe_fx_spot, "EURGBP", lambda x :print(f"EURGBP:>> {x}"))
    # # f2 = exectr.submit(client.subscribe_fx_spot, "GBPEUR", lambda x :print(f"GBPEUR:>> {x}"))
    f1 = exectr.submit(client.subscribe_fx_spot, "EURGBP", partial(print_price, "EURGBP"))
    # f2 = exectr.submit(client.subscribe_fx_spot, "GBPEUR", partial(print_price, "GBPEUR"))
    # f3 = exectr.submit(client.subscribe_fx_spot, "GBPUSD", partial(print_price, "GBPUSD"))
    # f4 = exectr.submit(client.subscribe_fx_spot, "USDJPY", partial(print_price, "USDJPY"))

    # # f3 = exectr.submit(client.subscribe_fx_spot, "GBPUSD", lambda x :print(x))
    # # f4 = exectr.submit(client.subscribe_fx_spot, "USDJPY", lambda x :print(x))

    # subscribe("EURGBP")
    # subscribe("GBPEUR")
    # subscribe("GBPEUR")
    # subscribe("GBPEUR")

    # # #exec.submit(foreva)
    pass
    foreva()
    pass
