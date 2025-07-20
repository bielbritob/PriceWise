import requests
import base64
import json


def encode_variables(payload):
    return base64.b64encode(json.dumps(payload).encode()).decode()


def fetch_products(category, total_pages=50, step=12):
    results = []

    headers = {
        'sec-ch-ua-platform': '"Android"',
        'Referer': 'https://www.supernovaera.com.br/bebidas/?page=48',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36',
        'accept': '*/*',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Brave";v="138"',
        'content-type': 'application/json',
        'sec-ch-ua-mobile': '?1',
    }

    params = {
        'workspace': 'master',
        'maxAge': 'short',
        'appsEtag': 'remove',
        'domain': 'store',
        'locale': 'pt-BR',
        '__bindingId': '8b389c2d-2c18-4726-b45e-b6b134af62da',
        'operationName': 'productSearchV3',
        'variables': '{}',
        'extensions': '{"persistedQuery":{"version":1,"sha256Hash":"c351315ecde7f473587b710ac8b97f147ac0ac0cd3060c27c695843a72fd3903","sender":"vtex.store-resources@0.x","provider":"vtex.search-graphql@0.x"},"variables":"eyJoaWRlVW5hdmFpbGFibGVJdGVtcyI6dHJ1ZSwic2t1c0ZpbHRlciI6IkFMTCIsInNpbXVsYXRpb25CZWhhdmlvciI6ImRlZmF1bHQiLCJpbnN0YWxsbWVudENyaXRlcmlhIjoiTUFYX1dJVEhPVVRfSU5URVJFU1QiLCJwcm9kdWN0T3JpZ2luVnRleCI6ZmFsc2UsIm1hcCI6ImMiLCJxdWVyeSI6ImJlYmlkYXMiLCJvcmRlckJ5IjoiT3JkZXJCeVNjb3JlREVTQyIsImZyb20iOjU1MiwidG8iOjU2Mywic2VsZWN0ZWRGYWNldHMiOlt7ImtleSI6ImMiLCJ2YWx1ZSI6ImJlYmlkYXMifV0sIm9wZXJhdG9yIjoiYW5kIiwiZnV6enkiOiIwIiwic2VhcmNoU3RhdGUiOm51bGwsImZhY2V0c0JlaGF2aW9yIjoiU3RhdGljIiwiY2F0ZWdvcnlUcmVlQmVoYXZpb3IiOiJkZWZhdWx0Iiwid2l0aEZhY2V0cyI6ZmFsc2UsImFkdmVydGlzZW1lbnRPcHRpb25zIjp7InNob3dTcG9uc29yZWQiOnRydWUsInNwb25zb3JlZENvdW50IjozLCJhZHZlcnRpc2VtZW50UGxhY2VtZW50IjoidG9wX3NlYXJjaCIsInJlcGVhdFNwb25zb3JlZFByb2R1Y3RzIjp0cnVlfX0="}',
    }

    for page in range(total_pages):
        start = page * step
        end = start + step - 1

        variables = {
            "hideUnavailableItems": True,
            "skusFilter": "ALL",
            "simulationBehavior": "default",
            "installmentCriteria": "MAX_WITHOUT_INTEREST",
            "productOriginVtex": False,
            "map": "c",
            "query": category,
            "orderBy": "OrderByScoreDESC",
            "from": start,
            "to": end,
            "selectedFacets": [{"key": "c", "value": category}],
            "operator": "and",
            "fuzzy": "0",
            "searchState": None,
            "facetsBehavior": "Static",
            "categoryTreeBehavior": "default",
            "withFacets": False,
            "advertisementOptions": {
                "showSponsored": True,
                "sponsoredCount": 3,
                "advertisementPlacement": "top_search",
                "repeatSponsoredProducts": True
            }
        }

        encoded_vars = encode_variables(variables)

        url = (
            "https://www.supernovaera.com.br/_v/segment/graphql/v1?"
            "workspace=master&maxAge=short&appsEtag=remove&domain=store&locale=pt-BR"
            "&__bindingId=8b389c2d-2c18-4726-b45e-b6b134af62da"
            "&operationName=productSearchV3"
            "&variables={}"
            f"&extensions={{\"persistedQuery\":{{\"version\":1,"
            "\"sha256Hash\":\"c351315ecde7f473587b710ac8b97f147ac0ac0cd3060c27c695843a72fd3903\","
            "\"sender\":\"vtex.store-resources@0.x\","
            "\"provider\":\"vtex.search-graphql@0.x\"}},"
            f"\"variables\":\"{encoded_vars}\"}}"
        )

        resp = requests.get(url, params=params, headers=headers)
        data = resp.json()
        print(f'[bold red]{data}')
        print("-"*100)
        products = data.get("data", {}).get("productSearch", {}).get("products", [])
        results.extend(products)
        print(results)
        #print(f"Página {page + 1}: {len(products)} produtos")

        if not products:
            break  # Parar se não vier mais nada

    return results


# Exemplo de uso
todos_produtos = fetch_products("bebidas")
