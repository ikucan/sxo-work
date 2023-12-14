
from typing import List
from typing import Dict

from sxo.interface.client import SaxoClient
from sxo.om.orders import Order
from sxo.om.positions import NetPosition

class OrderManagerError(Exception):
    ...

class Manager:
    def __init__(self, client: SaxoClient = None, token_file: str = None):
        if client:
            self._client = client
        elif token_file:
            self._client = SaxoClient(token_file = token_file)
        else:
            print(f"warning, creating default client")
            self._client = SaxoClient(token_file = "/data/saxo_token")
    
    def list_orders(self, cached:bool = False) -> List[Order]:
        '''
        list all orders
        '''
        if cached:
            return self._orders
        else:
            orders_json = self._client.list_orders()
            return Order.parse(orders_json)

    def orders_by_id(self, cached:bool = False) -> Dict[int, Order]:
        '''
        orders mapped by id
        '''
        if cached:
            return self._orders_by_id
        else:
            return {o.id():o for o in self.list_orders()}

    def refresh_orders(self,) -> Dict[int, Order]:
        '''
        refresh orders in the local cache
        '''
        self._orders = self.list_orders()
        self._orders_by_id = {o.id():o for o in self._orders}
        return self._orders_by_id

    def net_positions(self,):
        '''
        list net positions
        '''
        positions_json = self._client.all_positions()
        return NetPosition.parse(positions_json)

    def modify_order_by_id(self,
                           order_id:int,
                           target_price:float = None,
                           refresh_first:bool = False):
        '''
        modify an order by id. if refresh, pull the latest view of orders
        '''
        if refresh_first:
            self.refresh_orders()

        if order_id in self._orders_by_id:
            self._client.modify_order(
                order = self._orders_by_id[order_id]._json,
                price = target_price,
            )
        else:
            raise OrderManagerError(f"ERROR. Order with id {order_id} does not exist. Refresh if it should?")

    # def get_instrument_ref(self,

if __name__ == "__main__":
    om = Manager()
    a = om.list_orders()
    b = om.orders_by_id()
    c = om.net_positions()

    z = 123    