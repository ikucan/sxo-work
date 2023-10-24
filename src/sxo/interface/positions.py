# -*- coding: utf-8 -*-
# import re
from typing import Any
from typing import Dict
from typing import List

from sxo.interface.definitions import AssetType
from sxo.interface.definitions import OrderDirection
from sxo.interface.definitions import OrderDuration
from sxo.interface.definitions import OrderReleation
from sxo.interface.definitions import OrderType
from sxo.interface.entities.instruments import Instrument
from sxo.interface.entities.instruments import InstrumentUtil
from sxo.interface.factories import SaxoAPIClientBoundMethodMethodFactory


class PositionsError(Exception):
    pass

class PossitionsCommandBase(metaclass=SaxoAPIClientBoundMethodMethodFactory):
    """
    ik:>> TODO:>> this is a placeholder
    base class for order commands
    """
    pass


class ListPositions(PossitionsCommandBase):
    """
        https://www.developer.saxo/openapi/learn/orders-and-positions
    """

    def __call__(
        self,
    ):
        endpoint = f"positions?ClientKey={self.client_key}"
        res = self.rest_conn._GET_json(api_set="port", endpoint=endpoint, api_ver=1)  # type: ignore
        return res

