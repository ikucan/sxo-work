import pandas as pd
import clickhouse_connect as cc 

from sxo.util.binning import bin_values

HOST="0.0.0.0"
PORT=8123


client = cc.get_client(host=HOST, port=PORT)

qry = "select d, t, pair, bid, bsz, ask, asz from Saxo.FxSpot where pair='GBPUSD'"
res = client.query(qry)
df = pd.DataFrame(res.result_rows, columns=['d', 't', 'pair', 'bid', 'bsz','ask','asz'])
bins = bin_values(df, 60, 'bid')
i = 123


