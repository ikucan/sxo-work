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
                listOfIds = [i.uid() for i in all_ac_instr]
                uicsParam = f"list?Uics={','.join([str(id) for id in listOfIds])}"
                endpoint = f"/infoprices/{uicsParam}&AssetType={ac}" "&FieldGroups=Quote,Commissions"
                price = self.rest_conn._GET_json(api_set="trade", endpoint=endpoint, api_ver=1)  # type: ignore
                prices += price["Data"]
            return {"Data": prices}
        elif isinstance(instruments, Instrument):
            instr_id = f"?Uic={instruments.uid()}"
            endpoint = f"/infoprices/{instr_id}&AssetType={instruments.asset_class()}" "&FieldGroups=Quote,Commissions"
            return {"Data": self.rest_conn._GET_json(api_set="trade", endpoint=endpoint, api_ver=1)}  # type:ignore
        else:
            raise ValueError(f"unexpected parsed instrument type. {type(instruments)}")


class InfoPriceSubscription(metaclass=SaxoAPISubscriptionClientMethodFactory):
    """
    initiate an info price suibscription
    https://www.developer.saxo/openapi/referencedocs/trade/v1/prices/addsubscriptionasync/e1dbfa7d3e2ef801a7c4ade9e57f8812
    https://www.developer.saxo/openapi/learn/streaming

    """

    def __call__(
        self,
        instrument: str,
        callback: Callable[[Dict[Any, Any]], Any],
    ):
        try:
            context_id = secrets.token_urlsafe(16)
            reference_id = secrets.token_urlsafe(8)

            if isinstance(instrument, Instrument):
                instr = instrument
            elif isinstance(instrument, str):
                instr = InstrumentUtil.parse(instrument)
            else:
                raise ValueError(f"the instrument spec {instrument} needs to be either a str or Instrument type: {type(instrument)}")

            json = {
                "Arguments": {
                    "Uic": instr.uid(),
                    "AssetType": instr.asset_class(),
                },
                "ContextId": context_id,
                "ReferenceId": reference_id,
                "RefreshRate": 1,
            }

            res = self.rest_conn._POST_json(api_set="trade", endpoint="/prices/subscriptions", api_ver=1, json=json)  # type: ignore
            callback(res)
            loop = asyncio.new_event_loop()
            loop.run_until_complete(self.streamer(context_id, callback))
        except Exception as e:
            print(f"error trying to initiate a subscription for :{instrument}. {e}")
            raise e


    # ik:>> TODO:>> see if this is a general steraming function
    async def streamer(
        self,
        context_id: str,
        callback: Callable[[Dict[Any, Any]], Any],
    ):
        print(f"starting streamer for context {context_id} on loop :>> {asyncio.get_event_loop().__hash__()}")

        url = f"wss://streaming.saxobank.com/sim/openapi/streamingws/connect?contextId={context_id}"
        headers = {"Authorization": f"Bearer {self.rest_conn.token24}"}  # type: ignore

        async with websockets.connect(url, extra_headers=headers) as websocket:
            async for message in websocket:
                # print(message)
                # print(f"update for {pair} on loop :>> {asyncio.get_event_loop().__hash__()} \n   --> {self.decode_message(message)}")
                callback(self.decode_message(message))
                # pprint(self.decode_message(message))

    def decode_message(self, message):
        # msg_id = int.from_bytes(message[0:8], byteorder="little")
        ref_id_length = message[10]
        # ref_id = message[11 : 11 + ref_id_length].decode()
        # payload_format = message[11 + ref_id_length]
        payload_size = int.from_bytes(message[12 + ref_id_length : 16 + ref_id_length], byteorder="little")  # noqa: E203
        payload = message[16 + ref_id_length : 16 + ref_id_length + payload_size].decode()  # noqa: E203
        return json.loads(payload)
