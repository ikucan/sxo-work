# -*- coding: utf-8 -*-
import json
import os
from pathlib import Path

from sxo.interface.entities.auto_entities import AccountDetails

samples_path = Path(os.getenv("PWD")) / "samples"  # type: ignore

if __name__ == "__main__":
    file_path = samples_path / "account_details.json"
    json_str = open(file_path).read()
    jsn = json.loads(json_str)

    acct = AccountDetails(jsn)  # type: ignore
    print(acct.Name())  # type: ignore
    print(acct.ClientKey())  # type: ignore
    print(acct.UserId())  # type: ignore
    print(acct.UserKey())  # type: ignore
    pass
