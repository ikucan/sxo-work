# -*- coding: utf-8 -*-
from pathlib import Path

import sxo.interface.entities.instruments as ref_db
from sxo.interface.entities.instruments.reference import InstrumentDb
from sxo.interface.entities.instruments.reference import FxSpotSyms
from sxo.interface.entities.instruments.reference import EquitySyms

# check the path - these need to be colocated (or modify path)
AssetClassDb  = InstrumentDb
FxSpotInstruments = FxSpotSyms(Path(ref_db.__file__).parent / "FxSpot.json")
EquityInstruments = EquitySyms(Path(ref_db.__file__).parent / "Stock.json")

