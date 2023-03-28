# -*- coding: utf-8 -*-
# import datetime as dt
# import json
# import re
# from pprint import pprint
# from typing import Any
# from typing import Dict
# import numpy as np
# import pandas as pd
# # if __name__ == "__main__" :
# #     instrument, date = "GBPEUR", "20220527"
# #     raw_data_file = f"/data/{instrument}_raw_{date}.json"
# class StrategyA:
#     def __init__(self, *, execute_frequency_s: int, data_window_s: int, clock_drift_tillerance_ms: int, min_updates: int):
#         """
#         init the strategy:
#           - execute_frequency_s - period in seconds of how often the strategy should be run
#           - data_window_s - window over which to keep the data
#           - clock_drift_tillerance_ms - max allowed abs diff between data timestamp and wall timestamp
#           - min_updates - smallest number of data updates over the window for
#         keep track of current last batch of updates (betweenn executions)
#         keep track of a trailing window of data
#         """
#         self.execute_frequency = execute_frequency_s
#         self.data_window_s = data_window_s
#         self.drift_tolerance = clock_drift_tillerance_ms
#         self.min_updates = min_updates
#         self.t_last = np.datetime64("2022-01-01T00:00:00.000")
#         self.updates = []
#         self.data_set = pd.DataFrame()
#         self.n_executions = 0
#     def __call__(self, update: Dict[str, Any]):
#         """
#         process quote update. execute the strategy if the time has passed
#         """
#         if "ContextId" in update:
#             update = update["Snapshot"]
#         wall_time = np.datetime64(dt.datetime.now())
#         update_time = np.datetime64(update["LastUpdated"][0:-4])
#         # if an update is a full quote
#         if "Quote" in update:
#             upd = update["Quote"]
#             upd["t"] = update_time
#             self.updates.append(upd)
#         time_since_last_run = (update_time - self.t_last).astype("timedelta64[s]").astype(int)
#         if time_since_last_run > self.execute_frequency:
#             if len(self.updates) > 0:
#                 self.execute()
#                 self.n_executions += 1
#                 print(f"[# {self.n_executions}] time_since_last_run: {time_since_last_run}, #samples: {len(self.updates)}")
#                 self.updates = []
#             self.t_last = update_time
#             # pprint(upd)
#     def execute(
#         self,
#     ):
#         print("======")
#         tick_updates = [
#             {
#                 "t": u["t"],
#                 "b": u["Bid"],
#                 "a": u["Ask"],
#                 "m": u["Mid"],
#             }
#             for u in self.updates
#             if "t" in u
#         ]
#         df = pd.DataFrame(tick_updates)
#         t = df.t.values.astype("datetime64[ms]").astype("int")
#         bid, ask, mid = df.b.values, df.a.values, df.m.values
#         spread = bid - ask
#         # compute the metrics
#         dt = np.append(np.diff(t), 0)
#         twap = dt = np.append(np.diff(t), 0)
#         min, max = np.min(mid), np.max(mid)
#         range = max - min
#         if range < 0:
#             raise Exception(f"ERROR, range is negativeL {range}")
#         else:
#             print(f"metrics: {twap}")
#         pass
# if __name__ == "__main__":
#     instrument, date = "GBPEUR", "20220606"
#     strat = StrategyA(execute_frequency_s=300, data_window_s=1800, clock_drift_tillerance_ms=1800, min_updates=10)
#     raw_data_file = f"/data/{instrument}_raw_{date}.json"
#     t_last = np.datetime64("2022-01-01T00:00:00.000")
#     with open(raw_data_file) as file:
#         line = file.readline()
#         while line != None and len(line) > 0:
#             update = json.loads(line)
#             strat(update)
#             line = file.readline()
#         pass
