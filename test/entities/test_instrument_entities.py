# -*- coding: utf-8 -*-
from sxo.interface.entities.instruments import FxSpotInstruments

if __name__ == "__main__":
    # pairs = FxSpotInstruments.all_pairs()
    # for sym in pairs:
    #     pair = FxSpotInstruments.get_pair(sym)
    #     iid = FxSpotInstruments.get_instrument_id(sym)
    #     print(f"{sym} -> {iid}")
    print(FxSpotInstruments.get_instrument_id("EURGBP"))
