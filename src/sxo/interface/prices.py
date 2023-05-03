# -*- coding: utf-8 -*-
# import re
import asyncio
import json
import secrets
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Union

import websockets
from sxo.interface.entities.instruments import FxSpotInstruments
from sxo.interface.factories import SaxoAPIClientBoundMethodMethodFactory
from sxo.interface.factories import SaxoAPISubscriptionClientMethodFactory
from sxo.interface.entities.instruments.symbology import Instrument
from sxo.interface.entities.instruments.symbology import InstrumentUtil

class InfoPrice(metaclass=SaxoAPIClientBoundMethodMethodFactory):
    """
    https://www.developer.saxo/openapi/referencedocs/trade/v1/infoprices/getinfopricelistasync/2eaaceb6373a7eff36c5f04f345cabe0

    """

    def __call__(
        self,
        instrument: Instrument,
    ):
        instr_ids = f"?Uic={instrument}"
        
        endpoint = (
            f"/infoprices/{instr_ids}&AssetType={FxSpotInstruments.get_asset_class()}"
            "&FieldGroups=Quote,Commissions"
            # "&FieldGroups=Quote,PriceInfoDetails,PriceInfo,MarketDepth,HistoricalChanges,Commissions"
        )

        price = self.rest_conn._GET_json(api_set="trade", endpoint=endpoint, api_ver=1)  # type: ignore
        return price


class InfoSpotFxPrices(metaclass=SaxoAPIClientBoundMethodMethodFactory):
    """
    https://www.developer.saxo/openapi/referencedocs/trade/v1/infoprices/getinfopricelistasync/2eaaceb6373a7eff36c5f04f345cabe0

    """

    def __call__(
        self,
        ccy_pair: Union[str, List[str]],
    ):
        if isinstance(ccy_pair, str):
            fx_spot = InstrumentUtil.parse(f"FxSpot::{ccy_pair}")
            instr_ids = f"?Uic={fx_spot.uid()}"
        elif isinstance(ccy_pair, list):
            instr_ids = f"list?Uics={','.join([str(FxSpotInstruments.get_instrument_id(p)) for p in ccy_pair])}"
        else:
            raise ValueError(f"unexpected type: {type(ccy_pair)}")

        endpoint = (
            f"/infoprices/{instr_ids}&AssetType={FxSpotInstruments.get_asset_class()}"
            "&FieldGroups=Quote,Commissions"
            # "&FieldGroups=Quote,PriceInfoDetails,PriceInfo,MarketDepth,HistoricalChanges,Commissions"
        )

        price = self.rest_conn._GET_json(api_set="trade", endpoint=endpoint, api_ver=1)  # type: ignore
        return price


class InfoSpotFxPriceSubscription(metaclass=SaxoAPISubscriptionClientMethodFactory):
    """
    initiate an info price suibscription
    """

    def __call__(
        self,
        ccy_pair: Union[str, List[str]],
        callback: Callable[[Dict[Any, Any]], Any],
    ):
        context_id = secrets.token_urlsafe(16)
        reference_id = secrets.token_urlsafe(8)

        json = {
            "Arguments": {
                "Uic": FxSpotInstruments.get_instrument_id(ccy_pair),
                "AssetType": "FxSpot",
            },
            "ContextId": context_id,
            "ReferenceId": reference_id,
            "RefreshRate": 1,
        }

        res = self.rest_conn._POST_json(api_set="trade", endpoint="/prices/subscriptions", api_ver=1, json=json)  # type: ignore
        callback(res)
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.streamer(context_id, callback))

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
