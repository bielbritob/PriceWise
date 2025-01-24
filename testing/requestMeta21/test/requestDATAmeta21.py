import requests
from rich import print


headers = {
    'sec-ch-ua-platform': '"Android"',
    'Referer': 'https://supermercadometa21.instabuy.com.br/',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Brave";v="132"',
    'IB-Session-Id': '6776ec9642ed67fbaab78de0',
    'Content-Type': 'application/json',
    'sec-ch-ua-mobile': '?1',
}

params = {
    'subdomain': 'supermercadometa21',
    'category_slug': 'Bebe-Crianca',
}

response = requests.get('https://api.instabuy.com.br/apiv3/layout', params=params, headers=headers)
print(response.json())