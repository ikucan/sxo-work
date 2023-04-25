# -*- coding: utf-8 -*-
from pathlib import Path

import sxo.interface.entities.instruments as ref_db
from sxo.interface.entities.instruments.reference import FxSpotDb
from sxo.interface.entities.instruments.reference import EquityDb

# check the path - these need to be colocated (or modify path)
FxSpotInstruments = FxSpotDb(Path(ref_db.__file__).parent / "FxSpot.json")
EquityInstruments = EquityDb(Path(ref_db.__file__).parent / "Stock.json")
