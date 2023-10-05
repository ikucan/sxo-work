# -*- coding: utf-8 -*-
import os


# ###
# split the instruments out of the CSV env string
# ###
def parse_instruments(raw_instr_string: str):
    instrs = []
    for entry in raw_instr_string.split(","):
        clean_str = entry.strip()
        if len(clean_str) > 0:
            instrs.append(entry.strip())
    return instrs


def read_env(var: str, raise_if_missing: bool = True, default_value=None) -> str:
    if var in os.environ:
        return os.environ[var]
    elif raise_if_missing and not default_value:
        raise ValueError(f"missing environment varialble '{var}'")
    else:
        return default_value

# ###
# # read and check config to make sure everything is sensible
# ###
def config():
    """
    read the config from environemnt variables
    """

    token_file = read_env("TOKEN_FILE")
    raw_instruments = read_env("INSTRUMENTS")
    loop_sleep = read_env("SLEEP_PERIOD", raise_if_missing=False)
    hb_tolerrance = read_env("HB_TOLERANCE", raise_if_missing=False)
    if loop_sleep is None:
        loop_sleep = 5
    if hb_tolerrance is None:
        hb_tolerrance = 20
    else:
        hb_tolerrance = int(hb_tolerrance)
    instruments = parse_instruments(raw_instruments)
    return token_file, instruments, loop_sleep, hb_tolerrance


# ###
# # read config for the actual strategy
# ###
def strategy_config() -> (float, float, int, int):
    """
    read the config from environemnt variables
    """

    data_window_minutes = int(read_env("STRATEGY_DATA_WINDOW_M", default_value=24*60))
    stragey_frequency = int(read_env("STRATEGY_FREQUENCY_S", default_value=24*60))
    alpha = float(read_env("STRATEGY_ALPHA", default_value=3))
    beta = float(read_env("STRATEGY_BETA", default_value=1))

    return alpha, beta, stragey_frequency, data_window_minutes