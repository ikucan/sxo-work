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


# ###
# # read and check config to make sure everything is sensible
# ###
def config():
    """
    read the config from environemnt variables
    """

    def read_env(var: str, raise_if_missing: bool = True, default_value=None) -> str:
        if var in os.environ:
            return os.environ[var]
        elif raise_if_missing:
            raise ValueError(f"missing environment varialble '{var}'")
        else:
            return default_value

    token_file = read_env("TOKEN_FILE")
    raw_instruments = read_env("INSTRUMENTS")
    loop_sleep = read_env("SLEEP_PERIOD", raise_if_missing=False)
    hb_tolerrance = read_env("HB_TOLERANCE", raise_if_missing=False)
    if loop_sleep is None:
        loop_sleep = 5
    if hb_tolerrance is None:
        hb_tolerrance = 20
    instruments = parse_instruments(raw_instruments)
    return token_file, instruments, loop_sleep, hb_tolerrance
