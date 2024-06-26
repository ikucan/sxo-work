# -*- coding: utf-8 -*-
# import re
import asyncio
import json
import secrets

from typing import Any
from typing import Dict
from typing import List
from typing import Callable

import websockets

from sxo.interface.entities.instruments import Instrument
from sxo.interface.entities.instruments import InstrumentUtil
from sxo.interface.factories import SaxoAPISubscriptionClientMethodFactory



class StreamingError(Exception):
    pass


class WebSocketSubscriptionBase:

    def decode_message(self, message):
        # msg_id = int.from_bytes(message[0:8], byteorder="little")
        ref_id_length = message[10]
        # ref_id = message[11 : 11 + ref_id_length].decode()
        # payload_format = message[11 + ref_id_length]
        payload_size = int.from_bytes(message[12 + ref_id_length : 16 + ref_id_length], byteorder="little")  # noqa: E203
        payload = message[16 + ref_id_length : 16 + ref_id_length + payload_size].decode()  # noqa: E203
        return json.loads(payload)

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


class InfoMessageSubscription(WebSocketSubscriptionBase, metaclass=SaxoAPISubscriptionClientMethodFactory):
    """
    initiate an info price suibscription
    https://www.developer.saxo/openapi/referencedocs/trade/v1/prices/addsubscriptionasync/e1dbfa7d3e2ef801a7c4ade9e57f8812
    https://www.developer.saxo/openapi/learn/streaming
    https://www.developer.saxo/openapi/learn/messages
    https://saxobank.github.io/openapi-samples-js/websockets/trade-messages/
    """

    def __call__(
        self,
        callback: Callable[[Dict[Any, Any]], Any],
    ):
        try:
            context_id = secrets.token_urlsafe(16)
            reference_id = secrets.token_urlsafe(8)

            json = {
                "ContextId": context_id,
                "ReferenceId": reference_id,
                "RefreshRate": 1,
            }

            res = self.rest_conn._POST_json(api_set="trade", endpoint="/messages/subscriptions", api_ver=1, json=json)  # type: ignore
            callback(res)
            loop = asyncio.new_event_loop()
            loop.run_until_complete(self.streamer(context_id, callback))
        except Exception as e:
            print(f"error trying to initiate a POSITIONs subscription {e}")
            raise e


class InfoPriceSubscription(WebSocketSubscriptionBase, metaclass=SaxoAPISubscriptionClientMethodFactory):
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
                    "Uic": instr.uic(),
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
