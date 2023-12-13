# -*- coding: utf-8 -*-
import json
from sxo.util import file
from sxo.interface.client import SaxoClient
from sxo.interface.entities.instruments import InstrumentUtil
if __name__ == "__main__":
    client = SaxoClient()

    instruments = ['FxSpot::GBPUSD']
    for instr in instruments:
        resolved = InstrumentUtil.parse(instr)
        details_json = client.instrument_details(
                                    resolved.uic(),
                                    resolved.asset_type().name)
    

    print("--------------------------------------------------------")
    print("--------------------------------------------------------")
