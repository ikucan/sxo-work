# -*- coding: utf-8 -*-
import os
from typing import Tuple


class RedisConfig:
    @staticmethod
    def get() -> Tuple[str, int, str | None]:
        host = os.getenv("REDIS_HOST")
        port_str = os.getenv("REDIS_PORT")
        pwrd = os.getenv("REDIS_PASS")

        if host is None:
            host = "127.0.0.1"
        if port_str is None:
            port = 6379
        else:
            port = int(port_str)

        return (host, port, pwrd)
