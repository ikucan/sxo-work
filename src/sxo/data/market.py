import os
import numpy as np
import pandas as pd
from typing import List

import clickhouse_connect as cc 

from sxo.util.binning import bin_values


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

    def __init__(self,
             saxo_db:str = "Saxo",
             fx_table:str =  "FxSpot",
             cols:List[str] = ["d", "t", "pair", "bid", "bsz", "ask", "asz"],
             time_col:str = "t",
             instr_col:str = "pair"
             ):
        super().__init__()

        self._ch_client = cc.get_client(host=self.host(), port=self.port())
        self._saxo_db = saxo_db
        self._fx_table = fx_table
        self._fq_tname = f"{saxo_db}.{fx_table}"
        self._cols = cols
        self._instr_col = instr_col
        self._time_col = time_col

    def ls(self,) -> pd.DataFrame:
        sql = (f"SELECT {self._instr_col}, "
               "count(1) as n, "
               f"min({self._time_col}) as `first`, "
               f"max({self._time_col}) as `last` "
               f"FROM {self._fq_tname} "
               f"GROUP BY {self._instr_col}")
        return self.__query_to_df(sql, ['pair', 'n_ticks', 'from', 'to'])

    def get_quotes(self,
                  pair:str = None,
                  start:np.datetime64 = None,
                  end:np.datetime64 = None,
                  filter_no_volume:bool = True,
        ) -> pd.DataFrame:
        
        qry = f"SELECT {','.join(self._cols)} FROM {self._fq_tname} "
        where_cls = ""
        if pair:
            where_cls += f"WHERE {self._instr_col}='{pair}' "
        if start:
            where_cls += "WHERE " if len(where_cls) == 0 else "AND "
            where_cls += f"{self._time_col} >= '{str(start)}' "
        if end:
            where_cls += "WHERE " if len(where_cls) == 0 else "AND "
            where_cls += f"{self._time_col} <= '{str(end)}' "
        qry += where_cls

        quotes = self.__query_to_df(qry, self._cols)
        if filter_no_volume:
            non_zero_volume = (quotes['bsz'].values > 0) & (quotes['asz'].values > 0)
            quotes = quotes[non_zero_volume].copy()
        sorted = quotes.sort_values(by = self._time_col)
        return sorted
    
    def get_bins(self,
                 pair:str,
                 bin_size_s:int = 60,
                 start:np.datetime64 = None,
                 end:np.datetime64 = None,
        ) -> pd.DataFrame:
        quotes = self.get_quotes(pair, start, end)
        quotes['mid'] = (quotes['bid'].values + quotes['ask'].values) / 2
        bins = bin_values(quotes, bin_size_s, 'mid', check_ordering=True)
        return bins



    def __query_to_df(self, sql_query:str, cols:List[str]) -> pd.DataFrame :
        res = self._ch_client.query(sql_query)
        return pd.DataFrame(res.result_rows, columns=cols)


if __name__ == "__main__":
    fx_db = SaxoFxSpot()
    df1 = fx_db.ls()
    # df2 = fx_db.get_quotes(pair='GBPUSD')
    # df3 = fx_db.get_quotes(pair='GBPUSD', start = np.datetime64('2023-12-15'))
    # df4 = fx_db.get_quotes(pair='GBPUSD', end = np.datetime64('2023-12-15'))
    # df5 = fx_db.get_quotes(pair='GBPUSD', start = np.datetime64('2023-12-14'), end = np.datetime64('2023-12-16'))
    # df12 = fx_db.get_bins(pair='GBPUSD')
    # df13 = fx_db.get_bins(pair='GBPUSD', start = np.datetime64('2023-12-15'))
    # df14 = fx_db.get_bins(pair='GBPUSD', end = np.datetime64('2023-12-15'))
    df15 = fx_db.get_bins(pair='GBPUSD', start = np.datetime64('2023-12-14'), end = np.datetime64('2023-12-16'))
    i = 123
