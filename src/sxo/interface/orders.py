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


class OrderError(Exception):
    pass

class OrderCommandBase(metaclass=SaxoAPIClientBoundMethodMethodFactory):
    """
    base class for order commands
    """

    def string_or_list(self, ofg: str | List[str]) -> str:
        if isinstance(ofg, str):
            return ofg
        elif isinstance(ofg, list):
            return ",".join(ofg)
        else:
            raise ValueError(f"unexpected type for the order field group parameter: {type(ofg)}")

    def _make_order_json(
        self,
        *,
        instrument_id: int,
        direction: OrderDirection,
        asset_class: AssetType,
        amount: float,
        price: float,
        order_type: OrderType,
        duration: OrderDuration = OrderDuration.GoodTillCancel,
        relation: OrderReleation = OrderReleation.StandAlone,
        extern_order_ref:str = None,
        expiry_time:str = None,
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
        if extern_order_ref:
            extern_order_ref_str = str(extern_order_ref)
            if len(extern_order_ref_str) > 50:
                raise OrderError(f"ERROR, 'ExternalReference' is too large. It is {len(extern_order_ref_str)} but can only be 50 chars.")
            order_json['ExternalReference'] = extern_order_ref
        if expiry_time:
            order_json['OrderDuration'] = {
                    "DurationType": OrderDuration.GoodTillDate.name,
                    "ExpirationDateContainsTime": True,
                    "ExpirationDateTime": str(expiry_time) }


        return order_json

    def order_mods_from_order(self, order:Dict[Any, Any]) :
        order_mods = {
            "AccountKey": order['AccountKey'],
            "Uic": order['Uic'],
            "AssetType":  order['AssetType'],
            "Amount": order['Amount'],
            "BuySell": order['BuySell'],
            "OrderPrice":  order['Price'],
            "OrderType": order['OpenOrderType'],
            "OrderId": order['OrderId'],
        }

        if  "Duration" in order:
            order_mods["OrderDuration"] = order['Duration']
        elif  "OrderDuration" in order:
            order_mods["OrderDuration"] = order['OrderDuration']
        elif 'RelatedOpenOrders' in order:
            for related_order in order['RelatedOpenOrders']:
                if  "Duration" in related_order:
                    order_mods["OrderDuration"] = related_order['Duration']
                    break                    

        return order_mods


class LimitOrder(OrderCommandBase):
    """
    https://www.developer.saxo/openapi/tutorial#/8
    https://github.com/SaxoBank/openapi-samples-js/tree/master/orders

    >>> https://github.com/SaxoBank/openapi-samples-js/blob/master/orders/stocks/demo.js
    >>> lines 52 ono

    """

    def __call__(
        self,
        instrument: Instrument,
        direction: OrderDirection,
        price: float,
        limit_price: float,
        amount: float,
        stop_price: float = None,
        reference_id: str = None,
        expiry_time:str = None,
    ):
        if isinstance(instrument, Instrument):
            instr = instrument
        elif isinstance(instrument, str):
            instr = InstrumentUtil.parse(instrument)
        else:
            raise ValueError(f"the instrument spec {instrument} needs to be either a str or Instrument type: {type(instrument)}")

        entry_ref = f"{reference_id}:<en>" if reference_id else ":<entry>"
        exit_ref = f"{reference_id}:<ex>" if reference_id else ":<exix>"

        entry_order = self._make_order_json(
            instrument_id=instr.uid(),
            direction=direction,
            asset_class=instr.asset_type(),
            amount=amount,
            price=price,
            order_type=OrderType.Limit,
            extern_order_ref= entry_ref,
            expiry_time=expiry_time,
        )
        exit_order = self._make_order_json(
            instrument_id=instr.uid(),
            direction=direction.flip(),
            asset_class=instr.asset_type(),
            amount=amount,
            price=limit_price,
            order_type=OrderType.Limit,
            extern_order_ref= exit_ref,
        )
        entry_order["Orders"] = [exit_order]
        if stop_price:
            stop_ref = f"{reference_id}:<stop>" if reference_id else ":<stop>"

            stop_order = self._make_order_json(
                instrument_id=instr.uid(),
                direction=direction.flip(),
                asset_class=instr.asset_type(),
                amount=amount,
                price=stop_price,
                order_type=OrderType.Stop,
                extern_order_ref= stop_ref,
            )
            entry_order["Orders"].append(stop_order)
                
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
        field_groups: str | List[str] = ["DisplayAndFormat", "ExchangeInfo"],  # noqa:B006
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
        field_groups: str | List[str] = ["DisplayAndFormat", "ExchangeInfo"],  # noqa:B006
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
        order_id: str | List[str],  # noqa:B006
    ):
        endpoint = f"orders/{self.string_or_list(order_id)}/?AccountKey={self.account_key}"  # type: ignore

        res = self.rest_conn._DELETE_json(api_set="trade", endpoint=endpoint, api_ver=2)  # type: ignore
        return res




class ModifyOrder(OrderCommandBase):
    """
    https://www.developer.saxo/openapi/referencedocs/trade/v2/orders

    prototype URL : PATCH https://gateway.saxobank.com/sim/openapi/trade/v2/orders
    """

    def __call__(
        self,
        order: Dict[Any, Any],
        price : float = None,
    ):
        order_mods = self.order_mods_from_order(order)
        if price:
            order_mods['OrderPrice'] = price
        # else:
        #     raise OrderError(f"The order you are trying to modify needs to have an order Duration: {order}")


        res = self.rest_conn._PATCH_json(api_set="trade", endpoint="orders", api_ver=2, json=order_mods)  # type: ignore
        return res


