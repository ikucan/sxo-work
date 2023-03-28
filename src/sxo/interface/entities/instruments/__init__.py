# -*- coding: utf-8 -*-
from pathlib import Path

import sxo.interface.entities.instruments as ref_db
from sxo.interface.entities.instruments.entities import FxSpot

FxSpotInstruments = FxSpot(Path(ref_db.__file__).parent / "FxSpot.json")
