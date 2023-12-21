import os
import numpy as np
import pandas as pd
import clickhouse_connect as cc 


class ClickhouseConfig:
    HOST = "CLICKHOUSE_HOST"
    PORT = "CLICKHOUSE_PORT"

    def __init__(self,):
        if  ClickhouseConfig.HOST in os.environ:
            self._host = os.environ[ClickhouseConfig.HOST]
        else:
            self._host = "0.0.0.0"
        
        if  ClickhouseConfig.PORT in os.environ:
            self._port = os.environ[ClickhouseConfig.PORT]
        else:
            self._port = 8123

    def host(self,) -> str:
        return self._host

    def port(self,) -> int:
        return self._port

# qry = "select d, t, pair, bid, bsz, ask, asz from Saxo.FxSpot where pair='GBPUSD' order by t asc"
# res = client.query(qry)
# df = pd.DataFrame(res.result_rows, columns=['d', 't', 'pair', 'bid', 'bsz','ask','asz'])
# bins = bin_values(df, 60, 'bid', check_ordering=True)
# i = 123

class SaxoFxSpot(ClickhouseConfig):

    def init(self,):
        self.ch_client = cc.get_client(self.host(), self.port())

    def get_ticks(pair:str = None,
                  start:np.datetime64 = None,
                  end:np.datetime64 = None,
                  sort:bool = False,
        ) -> pd.DataFrame:
        
        qry = "select d, t, pair, bid, bsz, ask, asz from Saxo.FxSpot"
        if pair:
            ...
        "where pair='GBPUSD' order by t asc"

        pass


if __name__ == "__main__":
    ch = ClickhouseConfig()
    i = 123
