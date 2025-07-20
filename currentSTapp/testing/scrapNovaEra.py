import requests
from rich import print
import json
import base64

cookies = {
    'checkout.vtex.com': '__ofid=96e47bc532ab48f9b278980f5ec7bbd5',
    'CheckoutOrderFormOwnership': 'uLAqgu376y8Cz8OP5nwszIOnXCYfp9DuiNi0BlDwVKV1t7c1X8wsxQJfsu05Y6+57XPOj2UwvZN4grsjwzJfppLnIn5m46Ajwky1+GaiI2jbbTWsuLjJ8YxJK5ipTT0z7tPekUVKfD5+TYlD4FPKDs/OYTK7uZ8Na+s58aXhjsaHmfL5hyQKevpYJd5zowui0Efl/JlqOMCcsZz/1ohLN6qdi80yS/zDtMXsOB0BtsYtv1o1TydcuUjYtlkrXMLv/45SxAwJHgD3OhP5ROW+0Miwb37Uiv0/w0gnQwctCroCrvLy8OXBDzzVBV+//fi4c+sHTp4INSEVSNyQRw0atw==',
    'VtexWorkspace': 'master%3A-',
    'vtex-search-session': 'be5ecd09f2e04dd0b27df64beb671c80',
    'vtex-search-anonymous': '5598284627fc4287bbededa60b5c6299',
    'vtex_segment': 'eyJjYW1wYWlnbnMiOm51bGwsImNoYW5uZWwiOiIxIiwicHJpY2VUYWJsZXMiOm51bGwsInJlZ2lvbklkIjoiVTFjamJXVnlZMkZ1ZEdsc2JtOTJZV1Z5WVdGa1pXZGhjR0YwYVc4N2JXVnlZMkZ1ZEdsc2JtOTJZV1Z5WVd4dmFtRXlPQT09IiwidXRtX2NhbXBhaWduIjpudWxsLCJ1dG1fc291cmNlIjpudWxsLCJ1dG1pX2NhbXBhaWduIjpudWxsLCJjdXJyZW5jeUNvZGUiOiJCUkwiLCJjdXJyZW5jeVN5bWJvbCI6IlIkIiwiY291bnRyeUNvZGUiOiJCUkEiLCJjdWx0dXJlSW5mbyI6InB0LUJSIiwiY2hhbm5lbFByaXZhY3kiOiJwdWJsaWMifQ',
    'vtex_session': 'eyJhbGciOiJFUzI1NiIsImtpZCI6ImZlNTZlYjJkLWY4ZWEtNDE1Ny1iZmE5LTJjYTg0YjRkNDY4YiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50LmlkIjpbXSwiaWQiOiIyZWFkMjZlNC1jOTk4LTRiYjctOTVjYy04NTE5YzRlZjAzMDQiLCJ2ZXJzaW9uIjozLCJzdWIiOiJzZXNzaW9uIiwiYWNjb3VudCI6InNlc3Npb24iLCJleHAiOjE3NTMyMTA1NDIsImlhdCI6MTc1MjUxOTM0MiwianRpIjoiZDc3Yjc4ODAtYjViYy00MzA0LTlmMmQtYjQyOWEyZmFkNGQwIiwiaXNzIjoic2Vzc2lvbi9kYXRhLXNpZ25lciJ9.e-yJdE69rc-8K_cSEgu3HaOHgj3SLsRafJecd7G3XZV70HwupH8tWQChIn5w4Q6bCOqa2WILEMiEtXvK1QwEsg',
    'vtex_binding_address': 'mercantilnovaera.myvtex.com/',
}

headers = {
    'accept': '*/*',
    'accept-language': 'pt-BR,pt;q=0.8',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.supernovaera.com.br/bebidas/?page=43',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Brave";v="138"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36',
    'cookie': 'checkout.vtex.com=__ofid=96e47bc532ab48f9b278980f5ec7bbd5; CheckoutOrderFormOwnership=uLAqgu376y8Cz8OP5nwszIOnXCYfp9DuiNi0BlDwVKV1t7c1X8wsxQJfsu05Y6+57XPOj2UwvZN4grsjwzJfppLnIn5m46Ajwky1+GaiI2jbbTWsuLjJ8YxJK5ipTT0z7tPekUVKfD5+TYlD4FPKDs/OYTK7uZ8Na+s58aXhjsaHmfL5hyQKevpYJd5zowui0Efl/JlqOMCcsZz/1ohLN6qdi80yS/zDtMXsOB0BtsYtv1o1TydcuUjYtlkrXMLv/45SxAwJHgD3OhP5ROW+0Miwb37Uiv0/w0gnQwctCroCrvLy8OXBDzzVBV+//fi4c+sHTp4INSEVSNyQRw0atw==; VtexWorkspace=master%3A-; vtex-search-session=be5ecd09f2e04dd0b27df64beb671c80; vtex-search-anonymous=5598284627fc4287bbededa60b5c6299; vtex_segment=eyJjYW1wYWlnbnMiOm51bGwsImNoYW5uZWwiOiIxIiwicHJpY2VUYWJsZXMiOm51bGwsInJlZ2lvbklkIjoiVTFjamJXVnlZMkZ1ZEdsc2JtOTJZV1Z5WVdGa1pXZGhjR0YwYVc4N2JXVnlZMkZ1ZEdsc2JtOTJZV1Z5WVd4dmFtRXlPQT09IiwidXRtX2NhbXBhaWduIjpudWxsLCJ1dG1fc291cmNlIjpudWxsLCJ1dG1pX2NhbXBhaWduIjpudWxsLCJjdXJyZW5jeUNvZGUiOiJCUkwiLCJjdXJyZW5jeVN5bWJvbCI6IlIkIiwiY291bnRyeUNvZGUiOiJCUkEiLCJjdWx0dXJlSW5mbyI6InB0LUJSIiwiY2hhbm5lbFByaXZhY3kiOiJwdWJsaWMifQ; vtex_session=eyJhbGciOiJFUzI1NiIsImtpZCI6ImZlNTZlYjJkLWY4ZWEtNDE1Ny1iZmE5LTJjYTg0YjRkNDY4YiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50LmlkIjpbXSwiaWQiOiIyZWFkMjZlNC1jOTk4LTRiYjctOTVjYy04NTE5YzRlZjAzMDQiLCJ2ZXJzaW9uIjozLCJzdWIiOiJzZXNzaW9uIiwiYWNjb3VudCI6InNlc3Npb24iLCJleHAiOjE3NTMyMTA1NDIsImlhdCI6MTc1MjUxOTM0MiwianRpIjoiZDc3Yjc4ODAtYjViYy00MzA0LTlmMmQtYjQyOWEyZmFkNGQwIiwiaXNzIjoic2Vzc2lvbi9kYXRhLXNpZ25lciJ9.e-yJdE69rc-8K_cSEgu3HaOHgj3SLsRafJecd7G3XZV70HwupH8tWQChIn5w4Q6bCOqa2WILEMiEtXvK1QwEsg; vtex_binding_address=mercantilnovaera.myvtex.com/',
}

def encode_variables(payload: dict) -> str:
    json_str = json.dumps(payload, separators=(",", ":"))
    return base64.b64encode(json_str.encode()).decode()

# --- Geração dinâmica dos parâmetros para paginação ---
from_index = 516
to_index = 527
categoria = "bebidas"

# --- Variáveis do corpo que serão codificadas em Base64 ---
variables_payload = {
    "hideUnavailableItems": True,
    "skusFilter": "ALL",
    "simulationBehavior": "default",
    "installmentCriteria": "MAX_WITHOUT_INTEREST",
    "productOriginVtex": False,
    "map": "c",
    "query": categoria,
    "orderBy": "OrderByScoreDESC",
    "from": from_index,
    "to": to_index,
    "selectedFacets": [{"key": "c", "value": categoria}],
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

# --- Codifica a variável em base64 ---
encoded_variables = encode_variables(variables_payload)

# --- Parâmetros da requisição, com o campo variables substituído ---
params = {
    'workspace': 'master',
    'maxAge': 'short',
    'appsEtag': 'remove',
    'domain': 'store',
    'locale': 'pt-BR',
    '__bindingId': '8b389c2d-2c18-4726-b45e-b6b134af62da',
    'operationName': 'productSearchV3',
    'variables': '{}',
    'extensions': json.dumps({
        "persistedQuery": {
            "version": 1,
            "sha256Hash": "c351315ecde7f473587b710ac8b97f147ac0ac0cd3060c27c695843a72fd3903",
            "sender": "vtex.store-resources@0.x",
            "provider": "vtex.search-graphql@0.x"
        },
        "variables": encoded_variables
    })
}

# --- Faz a requisição GET ao endpoint GraphQL ---
response = requests.get(
    'https://www.supernovaera.com.br/_v/segment/graphql/v1',
    params=params,
    cookies=cookies,
    headers=headers
)

# --- Exibe os dados retornados ---
data = response.json()
print(data)
#produtos = data["data"]["productSearch"]["products"]
#total_products_found =
#for produto in produtos:
#    url_completa = f"https://www.supernovaera.com.br{produto.get('link')}"
#    image_url = produto["items"][0]["images"][0].get("imageUrl")  # Ajuste para acessar a URL da imagem corretamente
#   prices = produto["items"][0]["sellers"][0]["commertialOffer"].get("Price")


