# -*- coding: utf-8 -*-
# import re
import asyncio
import json
import secrets
from typing import Any
from typing import Callable
from typing import Dict
from typing import List

import websockets
from sxo.interface.entities.instruments import Instrument
from sxo.interface.entities.instruments import InstrumentGroup
from sxo.interface.entities.instruments import InstrumentUtil
from sxo.interface.factories import SaxoAPIClientBoundMethodMethodFactory
from sxo.interface.factories import SaxoAPISubscriptionClientMethodFactory


class InfoPrice(metaclass=SaxoAPIClientBoundMethodMethodFactory):
    """
    https://www.developer.saxo/openapi/referencedocs/trade/v1/infoprices/getinfopricelistasync/2eaaceb6373a7eff36c5f04f345cabe0

    """

    def __call__(
        self,
        instruments: str | List[str],
    ):
        instruments = InstrumentUtil.parse(instruments)
        if isinstance(instruments, InstrumentGroup):
            prices = []
            for ac in instruments.asset_classes():
                all_ac_instr = instruments.get_by_asset_class(ac)
                listOfIds = [i.uic() for i in all_ac_instr]
                uicsParam = f"list?Uics={','.join([str(id) for id in listOfIds])}"
                endpoint = f"/infoprices/{uicsParam}&AssetType={ac}" "&FieldGroups=Quote,Commissions"
                price = self.rest_conn._GET_json(api_set="trade", endpoint=endpoint, api_ver=1)  # type: ignore
                prices += price["Data"]
            return {"Data": prices}
        elif isinstance(instruments, Instrument):
            instr_id = f"?Uic={instruments.uic()}"
            endpoint = f"/infoprices/{instr_id}&AssetType={instruments.asset_class()}" "&FieldGroups=Quote,Commissions"
            return {"Data": self.rest_conn._GET_json(api_set="trade", endpoint=endpoint, api_ver=1)}  # type:ignore
        else:
            raise ValueError(f"unexpected parsed instrument type. {type(instruments)}")
