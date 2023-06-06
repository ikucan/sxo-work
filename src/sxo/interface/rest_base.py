# -*- coding: utf-8 -*-
import asyncio
from functools import cache
from typing import Dict

import aiohttp


class SaxoRestBase:
    @staticmethod
    def _refresh_24hr_token_from_file(fnm: str) -> str:
        """
        Read previously stored 24 hr token from a file
        """
        with open(fnm) as token_file:
            return token_file.read()

    def __init__(
        self,
        *,
        url_base: str,
        token_file: str,
    ):
        """
        Base for the saxo rest endpoint interaction:
            - encapsultes the base url
            - loads the 24 hr token from file
            - crates default headers, including the toekn encapsulation
            - creates the async processing loop
        """
        self.token24 = SaxoRestBase._refresh_24hr_token_from_file(token_file)
        self.token_header = f"Bearer {self.token24}"
        self.url_base = url_base

    @cache  # noqa
    def _make_default_headers(
        self,
    ) -> Dict[str, str]:
        return {"Authorization": self.token_header}

    #
    ##
    #
    async def _get_json_async(self, *, url: str, headers: Dict[str, str]):
        """
        return
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                # print("Status:", response.status)
                if response.ok:
                    return await response.json()
                raise Exception(f"a HTTP error occurred: {response.status}")

    def _GET_json(self, *, api_set: str, endpoint: str, api_ver: str, extra_headers: Dict[str, str] | None = None):
        url = f"{self.url_base}/{api_set}/v{api_ver}/{endpoint}"
        headers = self._make_default_headers() | ({} if extra_headers is None else extra_headers)
        # return self.aio_loop.run_until_complete(self._get_json_async(url=url, headers=headers))
        return asyncio.new_event_loop().run_until_complete(self._get_json_async(url=url, headers=headers))

    def _GET_drain_json(self, *, api_set: str, endpoint: str, api_ver: str, extra_headers: Dict[str, str] | None = None):
        """
        http get for the windowed data, get first window and drain subsequent if there
        """
        url = f"{self.url_base}/{api_set}/v{api_ver}/{endpoint}"
        headers = self._make_default_headers() | ({} if extra_headers is None else extra_headers)
        data = []
        while 1 < 2:
            # print(url)
            # data_window = self.aio_loop.run_until_complete(self._get_json_async(url=url, headers=headers))
            data_window = asyncio.new_event_loop().run_until_complete(self._get_json_async(url=url, headers=headers))

            data += data_window["Data"]
            if "__next" not in data_window:
                break
            else:
                url = data_window["__next"]
        return {"Data": data}

    #
    ##
    #
    async def _post_json_async(self, *, url: str, headers: Dict[str, str] | None, json: Dict[str, str] | None):
        """
        return
        """
        # url = "https://gateway.saxobank.com/sim/openapi/trade/v1/prices/subscriptions"

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=json) as response:
                # print("Status:", response.status)
                if response.ok:
                    return await response.json()
                raise Exception(f"a HTTP error occurred: {response.status}")

    def _post_json_wrapper(self, *, url: str, headers: Dict[str, str], json: Dict[str, str]):
        """
        an await wrapper for the async get
        """
        # return self.aio_loop.run_until_complete(self._post_json_async(url=url, headers=headers, json=json))
        return asyncio.new_event_loop().run_until_complete(self._post_json_async(url=url, headers=headers, json=json))

    def _POST_json(
        self, *, api_set: str, endpoint: str, api_ver: str, extra_headers: Dict[str, str] | None = None, json: Dict[str, str] | None = None
    ):
        url = f"{self.url_base}/{api_set}/v{api_ver}/{endpoint}"
        headers = self._make_default_headers() | ({} if extra_headers is None else extra_headers)
        return asyncio.new_event_loop().run_until_complete(self._post_json_async(url=url, headers=headers, json=json))

    async def _delete_json_async(self, *, url: str, headers: Dict[str, str]):
        """
        return
        """
        async with aiohttp.ClientSession() as session:
            async with session.delete(url, headers=headers) as response:
                if response.ok:
                    return await response.json()
                raise Exception(f"a HTTP error occurred: {response.status}")

    def _DELETE_json(self, *, api_set: str, endpoint: str, api_ver: str, extra_headers: Dict[str, str] | None = None):
        url = f"{self.url_base}/{api_set}/v{api_ver}/{endpoint}"
        headers = self._make_default_headers() | ({} if extra_headers is None else extra_headers)
        return asyncio.new_event_loop().run_until_complete(self._delete_json_async(url=url, headers=headers))

    def print_24hr_token(self):
        print("-----------------")
        print(self.token24)
        print("-----------------")


# import secrets
# if __name__ == "__main__":
#     url = "https://gateway.saxobank.com/sim/openapi/trade/v1/prices/subscriptions"

#     srb = SaxoRestBase(url_base="https://gateway.saxobank.com/sim/openapi")
#     headers = srb._make_default_headers()
#     json = {
#         "Arguments": {
#             "Uic": 17,
#             #'Uics': "17,21",
#             "AssetType": "FxSpot",
#         },
#         "ContextId": secrets.token_urlsafe(10),
#         "ReferenceId": secrets.token_urlsafe(5),
#         "RefreshRate": 1,
#     }

#     # res = srb._post_json_wrapper(url = url, headers = headers, json = json)
#     res = srb._POST_json(api_set="trade", endpoint="/prices/subscriptions", api_ver="v1", json=json)
#     print(123)
