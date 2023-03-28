# -*- coding: utf-8 -*-
import asyncio
import json
import secrets
from pprint import pprint

import requests
import websockets


def get_token(fnm: str = "/tmp/saxo_token") -> str:
    with open(fnm) as token_file:
        return token_file.read()


TOKEN = get_token()

# create a random string for context ID and reference ID
CONTEXT_ID = secrets.token_urlsafe(10)
REF_ID = secrets.token_urlsafe(5)


def create_subscription(context_id, ref_id, token):
    response = requests.post(
        # 'https://gateway.saxobank.com/sim/openapi/trade/v1/infoprices/subscriptions',
        "https://gateway.saxobank.com/sim/openapi/trade/v1/prices/subscriptions",
        headers={"Authorization": "Bearer " + token},
        json={
            "Arguments": {
                "Uic": 17,
                # 'Uics': "17,21",
                "AssetType": "FxSpot",
            },
            "ContextId": context_id,
            "ReferenceId": ref_id,
            "RefreshRate": 1,
        },
    )

    if response.status_code == 201:
        print("Successfully created subscription")
        print("Snapshot data:")
        pprint(response.json()["Snapshot"])
        print("Now receiving delta updates:")
    elif response.status_code == 401:
        print("Error setting up subscription - check TOKEN value")
        exit()


def decode_message(message):
    # msg_id = int.from_bytes(message[0:8], byteorder="little")
    ref_id_length = message[10]
    # ref_id = message[11 : 11 + ref_id_length].decode()
    # payload_format = message[11 + ref_id_length]
    payload_size = int.from_bytes(message[12 + ref_id_length : 16 + ref_id_length], byteorder="little")  # noqa : pe203
    payload = message[16 + ref_id_length : 16 + ref_id_length + payload_size].decode()  # noqa : pe203
    return json.loads(payload)


async def streamer(context_id, ref_id, token):
    url = f"wss://streaming.saxobank.com/sim/openapi/streamingws/connect?contextId={context_id}"
    headers = {"Authorization": f"Bearer {token}"}

    async with websockets.connect(url, extra_headers=headers) as websocket:
        async for message in websocket:
            # print(message)
            pprint(decode_message(message))


# Only one app is entitled to receive realtime prices. This is handled via the primary session.
# More info on keeping the status: https://saxobank.github.io/openapi-samples-js/websockets/primary-monitoring/
def take_primary_session():
    requests.put(
        "https://gateway.saxobank.com/sim/openapi/root/v1/sessions/capabilities",
        headers={"Authorization": "Bearer " + TOKEN},
        json={"TradeLevel": "FullTradingAndChat"},
    )


if __name__ == "__main__":
    take_primary_session()
    try:
        create_subscription(CONTEXT_ID, REF_ID, TOKEN)
        asyncio.get_event_loop().run_until_complete(streamer(CONTEXT_ID, REF_ID, TOKEN))
    except KeyboardInterrupt:
        print("User interrupted the interpreter - closing connection.")
        exit()
