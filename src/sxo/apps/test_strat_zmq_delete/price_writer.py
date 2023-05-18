# -*- coding: utf-8 -*-
import zmq


class PriceWriter:
    def __init__(self, fnm: str):
        pass


if __name__ == "__main__":
    instrument = "GBPEUR"
    sub_port = 5556

    #  Socket to talk to server
    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    print("Collecting updates from weather server...")
    socket.connect(f"tcp://localhost:{sub_port}")

    # Subscribe to zipcode, default is NYC, 10001
    socket.setsockopt_string(zmq.SUBSCRIBE, "GBPEUR")

    # Process 5 updates
    total_temp = 0
    for _update_nbr in range(5):
        string = socket.recv_string()
        print(string)
