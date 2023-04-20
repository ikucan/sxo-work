# -*- coding: utf-8 -*-
from pathlib import Path

import sxo.interface.entities.instruments as ref_db
from sxo.interface.entities.instruments.entities import FxSpot
from sxo.interface.entities.instruments.entities import Equity

# check the path - these need to be colocated (or modify path)
FxSpotInstruments = FxSpot(Path(ref_db.__file__).parent / "FxSpot.json")
EquityInstruments = Equity(Path(ref_db.__file__).parent / "Stock.json")
