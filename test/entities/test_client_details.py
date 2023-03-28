# -*- coding: utf-8 -*-
import json
import os
from pathlib import Path

from sxo.interface.entities.auto_entities import ClientDetails

samples_path = Path(os.getenv("PWD")) / "samples"  # type: ignore

if __name__ == "__main__":
    file_path = samples_path / "client_details.json"
    json_str = open(file_path).read()
    jsn = json.loads(json_str)

    client_info = ClientDetails(jsn)  # type: ignore

    print(client_info.Name())  # type: ignore
    print(client_info.ClientKey())  # type: ignore
    print(client_info.ClientId())  # type: ignore
    print(client_info.DefaultAccountId())  # type: ignore
    print(client_info.DefaultAccountKey())  # type: ignore
    print(client_info.LegalAssetTypes())  # type: ignore

    # pass
