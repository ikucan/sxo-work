# -*- coding: utf-8 -*-
# import re
from typing import Any
from typing import Dict
from typing import List
from typing import Union

from sxo.interface.definitions import AssetType
from sxo.interface.definitions import OrderDirection
from sxo.interface.definitions import OrderDuration
from sxo.interface.definitions import OrderReleation
from sxo.interface.definitions import OrderType
from sxo.interface.entities.instruments import FxSpotInstruments
from sxo.interface.factories import SaxoAPIClientBoundMethodMethodFactory


class OrderCommandBase(metaclass=SaxoAPIClientBoundMethodMethodFactory):
    """
    base class for order commands
    """

    def string_or_list(self, ofg: Union[str, List[str]]) -> str:
        if isinstance(ofg, str):
            return ofg
        elif isinstance(ofg, list):
            return ",".join(ofg)
        else:
            raise ValueError(f"unexpected type for the order field group parameter: {type(ofg)}")

    def _make_order_json(
        self,
        *,
        instrument_id: Union[int, List],
        direction: OrderDirection,
        asset_class: AssetType,
        amount: float,
        price: float,
        order_type: OrderType,
        duration: OrderDuration = OrderDuration.GoodTillCancel,
        relation: OrderReleation = OrderReleation.StandAlone,
    ) -> Dict[str, Any]:
        order_json = {
            "Uic": instrument_id,
            "BuySell": direction.name,
            "AssetType": asset_class.name,
            "Amount": amount,
            "OrderPrice": price,
            "OrderType": order_type.name,
            "ManualOrder": True,
            "OrderDuration": {"DurationType": duration.name},
            "AccountKey": self.account_key,  # type: ignore
            "OrderRelation": relation.name,
        }

        return order_json


# class FxLimitOrder(OrderCommandBase):
#     """
#     https://www.developer.saxo/openapi/tutorial#/8
#     https://github.com/SaxoBank/openapi-samples-js/tree/master/orders

#     >>> https://github.com/SaxoBank/openapi-samples-js/blob/master/orders/stocks/demo.js
#     >>> lines 52 ono

#     """

#     def __call__(
#         self,
#         ccy_pair: str,
#         price: float,
#         amount: float,
#     ):
#         if isinstance(ccy_pair, str):
#             instr_id = FxSpotInstruments.get_instrument_id(ccy_pair)
#         else:
#             raise ValueError(f"unexpected type: {type(ccy_pair)}")

#         entry_order = self._make_order_json(
#             instrument_id=instr_id,
#             direction=OrderDirection.Buy,
#             asset_class=AssetType.FxSpot,
#             amount=amount,
#             price=price,
#             order_type=OrderType.Limit,
#         )
#         exit_order = self._make_order_json(
#             instrument_id=instr_id,
#             direction=OrderDirection.Buy.flip(),
#             asset_class=AssetType.FxSpot,
#             amount=amount,
#             price=1.23,
#             order_type=OrderType.Limit,
#         )

#         entry_order["Orders"] = [exit_order]
#         res = self.rest_conn._POST_json(api_set="trade", endpoint="orders", api_ver=2, json=entry_order)  # type: ignore
#         return res

class FxLimitOrder(OrderCommandBase):
    """
    https://www.developer.saxo/openapi/tutorial#/8
    https://github.com/SaxoBank/openapi-samples-js/tree/master/orders

    >>> https://github.com/SaxoBank/openapi-samples-js/blob/master/orders/stocks/demo.js
    >>> lines 52 ono

    """

    def __call__(
        self,
        ccy_pair: str,
        price: float,
        amount: float,
    ):
        if isinstance(ccy_pair, str):
            instr_id = FxSpotInstruments.get_instrument_id(ccy_pair)
        else:
            raise ValueError(f"unexpected type: {type(ccy_pair)}")

        entry_order = self._make_order_json(
            instrument_id=instr_id,
            direction=OrderDirection.Buy,
            asset_class=AssetType.FxSpot,
            amount=amount,
            price=price,
            order_type=OrderType.Limit,
        )
        exit_order = self._make_order_json(
            instrument_id=instr_id,
            direction=OrderDirection.Buy.flip(),
            asset_class=AssetType.FxSpot,
            amount=amount,
            price=1.23,
            order_type=OrderType.Limit,
        )

        entry_order["Orders"] = [exit_order]
        res = self.rest_conn._POST_json(api_set="trade", endpoint="orders", api_ver=2, json=entry_order)  # type: ignore

        return res


class GetOrderDetails(OrderCommandBase):
    """
    https://www.developer.saxo/openapi/referencedocs/port/v1/orders
    https://www.developer.saxo/openapi/referencedocs/port/v1/orders/getopenorder/3024791d13ad168eeb5729c6f65659a3

    prototype:
    https://gateway.saxobank.com/sim/openapi/port/v1/orders/{ClientKey}/{OrderId}/?FieldGroups={FieldGroups}

    """

    def __call__(
        self,
        order_id: str,
        *,
        field_groups: Union[str, List[str]] = ["DisplayAndFormat", "ExchangeInfo"],  # noqa:B006
    ):
        endpoint = f"orders/{self.client_key}/{order_id}/?FieldGroups={self.string_or_list(field_groups)}"  # type: ignore

        res = self.rest_conn._GET_json(api_set="port", endpoint=endpoint, api_ver=1)  # type: ignore
        return res


class ListAllOrders(OrderCommandBase):
    """
    https://www.developer.saxo/openapi/tutorial#/9
    https://www.developer.saxo/openapi/referencedocs/port/v1/orders/getopenorders/cae24349737ea6fef4f0e6d9c477794e

    prototype:
    https://gateway.saxobank.com/sim/openapi/port/v1/orders/me/?$top={$top}&$skip={$skip}&FieldGroups={FieldGroups}&Status={Status}&MultiLegOrderId={MultiLegOrderId}
    """

    def __call__(
        self,
        *,
        field_groups: Union[str, List[str]] = ["DisplayAndFormat", "ExchangeInfo"],  # noqa:B006
    ):
        endpoint = f"orders/me/?FieldGroups={self.string_or_list(field_groups)}"

        res = self.rest_conn._GET_json(api_set="port", endpoint=endpoint, api_ver=1)  # type: ignore
        return res


class DeleteOrders(OrderCommandBase):
    """
    https://www.developer.saxo/openapi/referencedocs/trade/v2/orders/cancelorder/a1fd2fffa62f21901f23318f65fe8147

    prototype:
    https://gateway.saxobank.com/sim/openapi/trade/v2/orders/{OrderIds}/?AccountKey={AccountKey}
    """

    def __call__(
        self,
        order_id: Union[str, List[str]] = ["DisplayAndFormat", "ExchangeInfo"],  # noqa:B006
    ):
        endpoint = f"orders/{self.string_or_list(order_id)}/?AccountKey={self.account_key}"  # type: ignore

        res = self.rest_conn._DELETE_json(api_set="trade", endpoint=endpoint, api_ver=2)  # type: ignore
        return res
