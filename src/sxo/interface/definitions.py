# -*- coding: utf-8 -*-
from enum import Enum


class AssetType(Enum):
    """
    https://www.developer.saxo/openapi/learn/core-business-concepts
    """

    Bond = 0
    CfdOnFutures = 1
    CfdOnIndex = 2
    CfdOnStock = 3
    ContractFutures = 4
    FuturesOption = 5
    FutureStrategies = 6
    FxSpot = 7
    FxForwards = 8
    FxVanillaOption = 9
    FxOneTouch = 10
    FxNoTouch = 11
    Stock = 12
    StockIndex = 13
    StockIndexOption = 14
    StockOption = 15


class OrderDirection(Enum):
    """
    enumeration class representing possible values for order direction
    """

    Buy = 0
    Sell = 1

    def flip(
        self,
    ):
        return OrderDirection((self.value + 1) % 2)


class OrderType(Enum):
    Market = 0
    Limit = 1
    Stop = 2
    StopIfBid = 3
    StopIfOffered = 4
    StopIfTraded = 5
    StopLimit = 6
    TrailingStop = 7
    TrailingStopIfBid = 8
    TrailingStopIfOffered = 9
    TrailingStopIfTraded = 10


class OrderDuration(Enum):
    ImmediateOrCancel = 0
    FillOrKill = 1
    DayOrder = 2
    GoodTillDate = 3
    GoodTillCancel = 4


class OrderReleation(Enum):
    OrderRelation = 0
    StandAlone = (1,)
    IfDoneMaster = 2
    IfDoneSlaveOco = 3
    Oco = 4


if __name__ == "__main__":
    print(OrderDirection.Buy.flip())
    print(OrderDirection.Buy.name)
