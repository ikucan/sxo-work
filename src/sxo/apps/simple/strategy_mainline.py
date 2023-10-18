# -*- coding: utf-8 -*-
import time

from sxo.apps.simple.strategy_impl import StrategyImpl

def mainline():
    strategy = StrategyImpl()
    
    while 1 < 2:
        strategy()
        time.sleep(1)

if __name__ == "__main__":
    mainline()




