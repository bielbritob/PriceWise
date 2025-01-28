import requests
import json
import sqlite3
import time
from rich import print

# URL base da API
BASE_URL = "https://www.supernovaera.com.br/_v/segment/graphql/v1"

# Cabeçalhos para as requisições
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "application/json",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
}

# Cookies necessários (ajustar conforme necessário)
COOKIES = {
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

# Lista de categorias
CATEGORIAS = [
    "alimentos",
    "bebidas",
    "casa-e-bazar",
    "vestuario",
    "cuidados-com-a-roupa",
    "utilitarios-e-descartaveis",
    "eletro",
    "automotivo",
    "higiene-e-beleza",
    "infantil",
    "limpeza",
    "pet-shop"
]


def buscar_produtos(categoria, from_index, to_index):
    """Faz uma requisição à API para buscar produtos de uma categoria em um intervalo de índices."""
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
            "query": categoria,  # Categoria específica
            "orderBy": "OrderByNameASC",  # Ordenar alfabeticamente
            "from": from_index,
            "to": to_index,
            "selectedFacets": [],
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

    try:
        response = requests.get(BASE_URL, headers=HEADERS, cookies=COOKIES, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[bold red]Erro na requisição para a categoria '{categoria}': {e}[/bold red]")
        return None


def salvar_no_banco(produtos, categoria):
    """Salva os produtos no banco de dados."""
    conn = sqlite3.connect('produtos.db')
    cursor = conn.cursor()

    # Criação da tabela se não existir
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ean TEXT UNIQUE,  -- Chave única
            mercado TEXT,
            nome TEXT,
            marca TEXT,
            categoria TEXT,
            url TEXT,
            valor REAL,
            valorkg REAL,
            valorAntigo REAL,
            imagem TEXT
        )
    """)
    conn.commit()

    for produto in produtos:
        try:
            stock = produto["items"][0]["sellers"][0]["commertialOffer"].get("AvailableQuantity")
            if stock > 0:
                url_completa = f"https://www.supernovaera.com.br{produto.get('link')}"
                image_url = produto["items"][0]["images"][0].get("imageUrl", "")
                prices = produto["items"][0]["sellers"][0]["commertialOffer"].get("Price", 0)
                itemId = produto["items"][0].get("itemId", "")
                trueEan = produto["items"][0].get("ean", itemId)
                if trueEan != int:
                   trueEan = produto["items"][0].get("itemId")


                # Verificar se o produto já existe no banco
                cursor.execute("SELECT * FROM produtos WHERE ean = ?", (trueEan,))
                existing_product = cursor.fetchone()

                if existing_product:
                    # Atualizar produto se o preço for diferente
                    old_price = existing_product[6]  # Índice do campo `valor`
                    if old_price != prices:
                        cursor.execute("""
                            UPDATE produtos
                            SET valor = ?, imagem = ?, nome = ?, marca = ?, url = ?
                            WHERE ean = ?
                        """, (
                            prices,
                            image_url,
                            produto.get("productName", ""),
                            produto.get("brand", ""),
                            url_completa,
                            f'NovaEraEan: {trueEan}'
                        ))
                else:
                    # Inserir novo produto
                    cursor.execute("""
                        INSERT OR REPLACE INTO produtos (ean, mercado, nome, marca, url, valor, valorkg, valorAntigo, imagem)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        f'NovaEraEan: {trueEan}',
                        "Nova Era",
                        produto.get("productName", ""),
                        produto.get("brand", ""),
                        url_completa,
                        prices,
                        None,
                        None,
                        image_url
                    ))
                conn.commit()
            else:
                print('produto não DISPONIVEL STOCK = 0')
        except Exception as e:
            print(f"[bold red]Erro ao salvar produto no banco: {e}[/bold red]")

    conn.close()


def coletar_todos_produtos():
    """Coleta todos os produtos de todas as categorias."""
    for categoria in CATEGORIAS:
        print(f"[blue]Iniciando coleta para a categoria: {categoria}[/blue]")
        todos_produtos = []
        page_size = 100  # Produtos por página
        from_index = 0

        while True:
            to_index = from_index + page_size - 1
            print(f"[cyan]Coletando produtos de {from_index} a {to_index} para a categoria '{categoria}'...[/cyan]")
            data = buscar_produtos(categoria, from_index, to_index)

            if not data or "data" not in data or "productSearch" not in data["data"]:
                print(f"[yellow]Nenhum dado retornado para a categoria '{categoria}'. Fim da coleta.[/yellow]")
                break

            produtos = data["data"]["productSearch"].get("products", [])
            if not produtos:
                print(f"[yellow]Sem mais produtos para coletar na categoria '{categoria}'.[/yellow]")
                break

            todos_produtos.extend(produtos)
            salvar_no_banco(produtos, categoria)

            from_index += page_size
            time.sleep(0.1)  # Pausa para evitar rate-limiting

        print(f"[green]Total de produtos coletados para a categoria '{categoria}': {len(todos_produtos)}[/green]")

# Iniciar coleta
coletar_todos_produtos()
