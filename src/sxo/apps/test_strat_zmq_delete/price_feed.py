# -*- coding: utf-8 -*-
import json
from typing import Any
from typing import Dict

import zmq
from sxo.interface.client import SaxoClient

# from concurrent.futures import ThreadPoolExecutor as Executor


if __name__ == "__main__":
    instrument = "GBPEUR"
    pub_port = 5556

    zmq_context = zmq.Context()
    socket = zmq_context.socket(zmq.PUB)
    socket.bind(f"tcp://*:{pub_port}")

    def subscribe_and_publish(broker_host: str, broker_port: int) -> bool:
        try:

            def send_messge(msg: Dict[str, Any]):
                msg_str = f"{instrument}:: {json.dumps(msg)}"
                print(msg_str)
                socket.send_string(msg_str)

            sxc = SaxoClient()
            sxc.subscribe_fx_spot(instrument, send_messge)
            return True
        except Exception as e:
            print(f"ERROR :: {e}")
            return False

    subscribe_and_publish("localhost", pub_port)
