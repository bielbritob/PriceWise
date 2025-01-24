import requests
import json
import time
import  sqlite3

# URL da API
url = "https://www.supernovaera.com.br/_v/segment/graphql/v1"

# Cabeçalhos
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "application/json",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
}

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
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return None

# Coletar todos os produtos
todos_produtos = []
page_size = 100  # Número de produtos por página
from_index = 0
max_tentativas = 3  # Número máximo de tentativas em caso de falha
limite_produtos = 3100  # Limite máximo de produtos

while from_index < limite_produtos:
    tentativas = 0
    data = None

    # Tentar buscar os produtos até o número máximo de tentativas
    while tentativas < max_tentativas:
        to_index = min(from_index + page_size - 1, limite_produtos - 1)  # Ajusta o valor de `to`
        data = buscar_produtos(from_index, to_index)
        if data is not None:
            break  # Sai do loop se os dados forem obtidos com sucesso
        tentativas += 1
        print(f"Tentativa {tentativas} de {max_tentativas}...")
        time.sleep(2)  # Espera 2 segundos antes de tentar novamente

    # Se não conseguir obter os dados após as tentativas, interrompe o loop
    if data is None:
        print("Não foi possível obter os dados após várias tentativas. Interrompendo...")
        break

    # Verificar se a resposta contém produtos
    if not isinstance(data, dict) or "data" not in data or "productSearch" not in data["data"] or "products" not in data["data"]["productSearch"]:
        print("Resposta da API não contém produtos. Interrompendo...")
        break

    produtos = data["data"]["productSearch"]["products"]

    # Adicionar produtos à lista
    todos_produtos.extend(produtos)

    # Verificar se atingiu o limite de produtos
    if len(todos_produtos) >= limite_produtos:
        print(f"Limite de {limite_produtos} produtos atingido. Interrompendo...")
        break

    # Verificar se há mais produtos
    if len(produtos) < page_size:
        break  # Fim dos resultados

    # Atualizar índice para a próxima página
    from_index += page_size
    print(f"Coletados {len(todos_produtos)} produtos até agora...")

    # Pausa entre requisições para evitar rate limiting
    time.sleep(1)

# Coletar os produtos restantes (de 3200 a 3211)
if len(todos_produtos) < limite_produtos:
    print("Coletando produtos restantes...")
    from_index = 3200
    to_index = 3211
    data = buscar_produtos(from_index, to_index)
    if data and "data" in data and "productSearch" in data["data"] and "products" in data["data"]["productSearch"]:
        produtos = data["data"]["productSearch"]["products"]
        todos_produtos.extend(produtos)
        print(f"Coletados {len(todos_produtos)} produtos no total.")

# Exibir total de produtos coletados
print(f"Total de produtos coletados: {len(todos_produtos)}")


# Conectar ao banco de dados (ou criar se não existir)
conn = sqlite3.connect('../test/produtos.db')
cursor = conn.cursor()

# Criar a tabela de produtos (se não existir)
cursor.execute("""
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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

# Função para salvar os produtos no banco de dados
def salvar_no_banco(produtos):
    for produto in produtos:
        url_completa = f"https://www.supernovaera.com.br{produto.get('link')}"
        image_url = produto["items"][0]["images"][0].get("imageUrl")  # Ajuste para acessar a URL da imagem corretamente
        prices = produto["items"][0]["sellers"][0]["commertialOffer"].get("Price")
        if prices:
            itemId = produto["items"][0].get("itemId")
            trueEan = produto["items"][0].get("ean")
            ean = trueEan if trueEan is int else itemId

            # Verificar se o produto já existe no banco de dados (usando o campo 'ean' como chave única)
            cursor.execute('SELECT * FROM produtos WHERE ean = ?', (ean,))
            if cursor.fetchone() is None:
                # Inserir no banco de dados
                cursor.execute("""
                INSERT INTO produtos (ean, mercado, nome, marca, url, valor, valorkg, valorAntigo, imagem)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    ean,
                    'Nova Era',
                    produto.get("productName"),
                    produto.get("brand", ''),
                    url_completa,
                    prices,
                    None,  # valorkg (ajuste conforme necessário)
                    None,  # valorAntigo (ajuste conforme necessário)
                    image_url
                ))
                conn.commit()

# Salvar os produtos no banco de dados
salvar_no_banco(todos_produtos)

# Fechar a conexão com o banco de dados
conn.close()

print("Produtos salvos no banco de dados 'produtos.db'.")