# -*- coding: utf-8 -*-
import json
from pprint import pprint

import numpy as np
import pandas as pd
import pyarrow as pa

# if __name__ == "__main__" :
#     instrument, date = "GBPEUR", "20220527"
#     raw_data_file = f"/data/{instrument}_raw_{date}.json"


#     with open(raw_data_file) as file:
#         line = file.readline()
#         while line != None and len(line) > 0:
#             update = json.loads(line)
#             pprint(update)
#             line = file.readline()

if __name__ == "__main__":
    instrument, date = "GBPEUR", "20220527"
    raw_data_file = f"/data/{instrument}_raw_{date}.json"
    t = np.datetime64("2022-05-27T17:48:52.622000").astype("datetime64[ms]").astype(np.int64)
    df = pd.DataFrame({"Ask": [1.0], "Bid": [1.0], "Mid": [1.0], "t": t})
    big_tab = pa.Table.from_pandas(df)
    with open(raw_data_file) as file:
        line = file.readline()
        while line is not None and len(line) > 0:
            update = json.loads(line)
            if "Quote" in update:
                update["Quote"]["t"] = t
                upd = [update["Quote"]]
                tab = pa.Table.from_pylist(upd)
                big_tab = pa.concat_tables([big_tab, tab])
                print(tab)
            pprint(update)
            line = file.readline()

    print(big_tab)
