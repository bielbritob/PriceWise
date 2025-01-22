import requests
from rich import print
cookies = {
    'app': '%7B%22cidade%22%3A37%2C%22empresa%22%3A20%2C%22tipoEnvio%22%3A2%2C%22aceiteCookies%22%3Afalse%2C%22userName%22%3A%22%22%2C%22totalCart%22%3A%220%2C00%22%2C%22quantityCart%22%3A0%2C%22modalMergeCart%22%3Afalse%2C%22quantityCartBrowser%22%3A0%7D',
    'viewport': 'sm',
}

headers = {
    'accept': '*/*',
    'accept-language': 'pt-BR,pt;q=0.5',
    'authorization': 'undefined',
    'content-type': 'application/json',
    # 'cookie': 'app=%7B%22cidade%22%3A37%2C%22empresa%22%3A20%2C%22tipoEnvio%22%3A2%2C%22aceiteCookies%22%3Afalse%2C%22userName%22%3A%22%22%2C%22totalCart%22%3A%220%2C00%22%2C%22quantityCart%22%3A0%2C%22modalMergeCart%22%3Afalse%2C%22quantityCartBrowser%22%3A0%7D; viewport=sm',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Brave";v="132"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36',
    'x-cart': 'undefined',
    'x-empresa': '20', # 20 = pvh; 122 = guajaráMirim
    'x-tipo-envio': '2',
}

params = {
    'pesquisa': 'café 500g',
    'pagina': '20',
}

response = requests.get(
    'https://www.irmaosgoncalves.com.br/api/produto/pesquisar',
    params=params,
    cookies=cookies,
    headers=headers,
)
print(response.json())