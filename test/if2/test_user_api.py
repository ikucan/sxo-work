# -*- coding: utf-8 -*-
from sxo.interface2.client import SaxoClient

if __name__ == "__main__":
    client = SaxoClient()
    import json
    from sxo.util import file

    print("--------------------------------------------------------")
    file.save("samples/user_details.json", json.dumps(client.user_details(), indent=4, sort_keys=True))
    print("--------------------------------------------------------")
    file.save("samples/client_details.json", json.dumps(client.client_details(), indent=4, sort_keys=True))
    print("--------------------------------------------------------")
    file.save("samples/account_details.json", json.dumps(client.account_details(), indent=4, sort_keys=True))
    print("--------------------------------------------{1024*1024}------------")
    file.save("samples/ref_countries.json", json.dumps(client.countries(), indent=4, sort_keys=True))
    print("--------------------------------------------------------")
    file.save("samples/ref_cultures.json", json.dumps(client.cultures(), indent=4, sort_keys=True))
    print("--------------------------------------------------------")
    file.save("samples/ref_currencies.json", json.dumps(client.currencies(), indent=4, sort_keys=True))
    print("--------------------------------------------------------")
    # file.save("samples/ref_currency_pairs.json", json.dumps(client.currency_pairs(), indent=4, sort_keys=True))
    print("--------------------------------------------------------")
    file.save("samples/exchanges.json", json.dumps(client.exchanges(0), indent=4, sort_keys=True))
    print("--------------------------------------------------------")
    file.save("samples/ref_currency_pairs.json", json.dumps(client.currency_pairs(), indent=4, sort_keys=True))
    print("--------------------------------------------------------")
    for asset_type in [
        "FxSpot",
        "FxForwards",
        "FxVanillaOption",
        "CfdOnStock",
        "CfdOnIndex",
        "CfdOnFutures",
        "Stock",
        "StockIndex",
        "StockOption",
        "StockIndexOption",
        "FuturesOption",
        "Bond",
    ]:
        # for asset_type in ["Stock"]:
        print(f"getting::> {asset_type} instruments")
        file.save(f"samples/instruments/{asset_type}.json", json.dumps(client.instruments(asset_type), indent=4, sort_keys=True))
    print("--------------------------------------------------------")
