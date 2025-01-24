import sqlite3

import requests
import json
import sqlite3

conn = sqlite3.connect('produtos.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINREMENT,
    ean TEXT UNIQUE, -- unique 
    mercado TEXT,
    nome TEXT,
    marca TEXT, 
    url TEXT,
    valor REAL,
    valorkg REAL,
    valorAntigo REAL,
    imagem TEXT
)
""")
conn.commit()


# URL da API
url = "https://www.supernovaera.com.br/_v/segment/graphql/v1"

# Cabeçalhos
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "application/json",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
}

# Cookies
cookies = {
    'vtex-search-anonymous': '3a3ee8bbef864fa182366d6c16b2de60',
    'checkout.vtex.com': '__ofid=96e47bc532ab48f9b278980f5ec7bbd5',
    'VtexWorkspace': 'master%3A-',
    'vtex-search-session': 'b16e127bb4f84c2491653ff537277e0c',
    'vtex_binding_address': 'mercantilnovaera.myvtex.com/',
    'vtex_session': 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjhkMDg0ZmViLTg2MDQtNDUwOS1iYjE4LTZlYzNlY2M0ZDM5ZSIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50LmlkIjpbXSwiaWQiOiJlNzRhNDNlOC1jNjcwLTQ2MTctYWM3Ni0wMmIwOGMyZmZkNjMiLCJ2ZXJzaW9uIjo1LCJzdWIiOiJzZXNzaW9uIiwiYWNjb3VudCI6InNlc3Npb24iLCJleHAiOjE3MzgzNzI1MjIsImlhdCI6MTczNzY4MTMyMiwianRpIjoiZjE0OWJmZjctODQwOC00ZTEzLTkzOTItYjAwZjhjYmRmNDE3IiwiaXNzIjoic2Vzc2lvbi9kYXRhLXNpZ25lciJ9.KTFBQweytaRo_wwfRwzDn1TcEbHnZy1bNvi_da8rhD-SF3Zzp1xkJgGr56o2XGjPuQjhsZNLvE4OXb45Zd69ZQ',
    'vtex_segment': 'eyJjYW1wYWlnbnMiOm51bGwsImNoYW5uZWwiOiIxIiwicHJpY2VUYWJsZXMiOm51bGwsInJlZ2lvbklkIjoiVTFjamJXVnlZMkZ1ZEdsc2JtOTJZV1Z5WVd4dmFtRXlPQT09IiwidXRtX2NhbXBhaWduIjpudWxsLCJ1dG1fc291cmNlIjpudWxsLCJ1dG1pX2NhbXBhaWduIjpudWxsLCJjdXJyZW5jeUNvZGUiOiJCUkwiLCJjdXJyZW5jeVN5bWJvbCI6IlIkIiwiY291bnRyeUNvZGUiOiJCUkEiLCJjdWx0dXJlSW5mbyI6InB0LUJSIiwiY2hhbm5lbFByaXZhY3kiOiJwdWJsaWMifQ',
    'CheckoutOrderFormOwnership': 'fRyVUn2+V+yAHuoVCI9oneYQ0ZInsiOZ3hMlPwr82wWXp8tc9tg9LmAtfcGjm+Ry1Me7iPdnezPhMnFKUxBZ7TcWEna28vaEVj0Dc8pVLmJvN+buRsbErjbtp7nXte8XjnjT+mhhACYYNxXu0RyR3ssioU5+KraRJd88fJOG4gt8eRK3uHonp/O7O5PW6PL7lKcRg8ZFRQUq3GyF7CgZa2Ad2SBpqcuwhcLfNpgqlR6LpyadLJBERTqAbNIRrPaCLq0ingSm/ew6w+MSg4qXeUOMdP7jLcAqv1ifko9aObE=',
    'biggy-search-history': 'leite%20uht%2CAbacaxi%20P%C3%A9rola%2Ccaf%C3%A9%20500g',
    'janus_sid': '01294fb0-89ec-4559-a7d3-bc2bc10fd8cc',
}


# Função para buscar produtos
def buscar_produtos(from_index, to_index):
    # Parâmetros da requisição
    params = {
        "workspace": "master",
        "maxAge": "short",
        "appsEtag": "remove",
        "domain": "store",
        "locale": "pt-BR",
        "__bindingId": "8b389c2d-2c18-4726-b45e-b6b134af62da",
        "operationName": "productSearchV3",
        "variables": json.dumps({
            "hideUnavailableItems": True,
            "skusFilter": "ALL",
            "simulationBehavior": "default",
            "installationCriteria": "MAX_WITHOUT_INTEREST",
            "productOriginVtex": False,
            "map": "c,c",
            "query": "",  # Query vazia para buscar todos os produtos
            "orderBy": "OrderByNameASC",  # Ordenar por nome em ordem alfabética
            "from": from_index,
            "to": to_index,
            "selectedFacets": [],  # Lista vazia para remover filtros
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
        }),
        "extensions": json.dumps({
            "persistedQuery": {
                "version": 1,
                "sha256Hash": "9177ba6f883473505dc99fcf2b679a6e270af6320a157f0798b92efeab98d5d3",
                "sender": "vtex.store-resources@0.x",
                "provider": "vtex.search-graphql@0.x"
            }
        })
    }

    # Fazer a requisição
    try:
        response = requests.get(url, params=params, headers=headers, cookies=cookies)
        response.raise_for_status()  # Levanta uma exceção para códigos de status HTTP ruins
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
            print("Erro 400: Fim dos produtos.")
            return {"data": {"productSearch": None}}  # Retorna uma estrutura compatível
        else:
            print(f"Erro HTTP na requisição: {e}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return None


# Função para coletar todos os produtos
def coletar_todos_produtos():
    todos_produtos = []
    from_index = 0
    to_index = 50  # Ajuste o tamanho do lote conforme necessário
    while True:
        print(f"Coletando produtos de {from_index} a {to_index}...")
        data = buscar_produtos(from_index, to_index)

        # Verifica se a resposta é inválida (erro 400 ou outro erro)
        if data is None:
            print("Erro: Resposta inválida da API.")
            break

        # Verifica se a estrutura da resposta está correta
        if "data" not in data or "productSearch" not in data["data"]:
            print("Erro: Estrutura da resposta inesperada.")
            break

        # Verifica se productSearch é None (fim dos produtos)
        if data["data"]["productSearch"] is None:
            print("Fim dos produtos.")
            break

        produtos = data["data"]["productSearch"].get("products", [])

        if not produtos:
            print("Fim dos produtos.")
            break  # Sai do loop se não houver mais produtos



        # salvar @all to json
        todos_produtos.extend(produtos)
        from_index = to_index + 1
        to_index += 50  # Ajuste o incremento conforme necessário

    return todos_produtos


# Coletar todos os produtos
todos_produtos = coletar_todos_produtos()

# Salvar os dados em um arquivo JSON
with open("todos_produtos.json", "w", encoding="utf-8") as f:
    json.dump(todos_produtos, f, ensure_ascii=False, indent=4)

if cursor.fetchone() is None:
    # Inserir no db
    cursor.execute("""
    INSERT INTO produtos (ean, mercado, nome, marca, url, valor, valokg, valorAntigo, imagem)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        ean,
        'Nova Era',
        todos_produtos.get
    ))

print(f"Total de produtos coletados: {len(todos_produtos)}")
print("Dados salvos em 'todos_produtos.json'.")