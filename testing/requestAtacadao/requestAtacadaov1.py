import requests
import json
import math
import sqlite3
from rich import print

def fetch_products_by_category(base_url, category, first=20):
    all_products = []  # Lista para armazenar todos os produtos de uma categoria
    offset = 0         # Deslocamento inicial
    headers = {
        "accept": "*/*",
        "accept-language": "pt-BR,pt;q=0.7",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36"
    }

    # Primeiro, obtenha o total de produtos na categoria
    variables = {
        "first": first,
        "after": str(offset),
        "sort": "score_desc",
        "term": "",
        "selectedFacets": [
            {"key": "category-1", "value": category},
            {"key": "channel", "value": '{"salesChannel":"2","seller":"atacadaobr213","regionId":"U1cjYXRhY2FkYW9icjIxMw=="}'},
            {"key": "locale", "value": "pt-BR"}
        ]
    }

    payload = {
        "operationName": "ProductsQuery",
        "variables": json.dumps(variables)
    }

    # Requisição inicial para descobrir o total de produtos
    response = requests.get(base_url, params=payload, headers=headers)
    if response.status_code != 200:
        print(f"[{category}] Erro na requisição inicial: {response.status_code}")
        return []

    data = response.json()
    total_count = data.get("data", {}).get("search", {}).get("products", {}).get("pageInfo", {}).get("totalCount", 0)
    print(f"[{category}] Total de produtos: {total_count}")

    # Calcula o número total de páginas
    total_pages = math.ceil(total_count / first)
    print(f"[{category}] Total de páginas: {total_pages}")

    # Itera sobre as páginas para obter todos os produtos
    for page in range(total_pages):
        offset = page * first
        variables["after"] = str(offset)
        payload["variables"] = json.dumps(variables)

        response = requests.get(base_url, params=payload, headers=headers)
        if response.status_code != 200:
            print(f"[{category}] Erro na página {page + 1}: {response.status_code}")
            continue

        data = response.json()
        products = data.get("data", {}).get("search", {}).get("products", {}).get("edges", [])
        all_products.extend(products)

    return all_products


def fetch_all_categories(base_url, categories):
    all_data = {}

    for category in categories:
        print(f"\n--- Processando categoria: {category} ---")
        products = fetch_products_by_category(base_url, category)
        all_data[category] = products
        print(f"[{category}] Total de produtos coletados: {len(products)}")

    return all_data


# URL base da API
base_url = "https://www.atacadao.com.br/api/graphql"

# Lista de categorias
todas_categorias = [
    'mercearia',
    'bebidas',
    'limpeza',
    'higiene-e-perfumaria',
    'padaria-e-matinais',
    'papelaria',
    'pet-shop',
    'automotivo',
    'eletronicos-e-eletroportateis',
    'vestuario',
    'utilidades-domesticas',
    'descartaveis-e-embalagens',
    'esporte-e-lazer'
]

# Coletar produtos de todas as categorias
dados_todas_categorias = fetch_all_categories(base_url, todas_categorias)

# Exibir resumo dos resultados
print("\n--- Resumo Final ---")
for categoria, produtos in dados_todas_categorias.items():
    print(f"Categoria: {categoria} - Produtos coletados: {len(produtos)}")

    # Conexão com o banco de dados
    conn = sqlite3.connect('produtos.db')
    cursor = conn.cursor()
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

    # Iterar sobre todos os produtos de uma categoria
    for produto in produtos:
        node = produto["node"]
        name = node.get("name")
        ean = node.get("id")
        mercado = "Atacadão"
        marca = node["brand"].get("name")
        url = node["breadcrumbList"]["itemListElement"][-1].get("item")
        url_full = f"https://www.atacadao.com.br{url}"
        valor = node["offers"].get("highPrice")
        imagem = node["image"][0].get("url")

        # Verificar se o produto já está no banco de dados
        cursor.execute('SELECT * FROM produtos WHERE ean = ?', (ean,))
        if cursor.fetchone() is None:
            # Inserir no banco de dados
            cursor.execute("""
                INSERT OR IGNORE INTO produtos (ean, mercado, nome, marca, url, valor, valorkg, valorAntigo, imagem)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                f'AtacadãoEan: {ean}',
                mercado,
                name,
                marca,
                url_full,
                valor,
                None,  # valorkg (ajuste conforme necessário)
                None,  # valorAntigo (ajuste conforme necessário)
                imagem
            ))
            conn.commit()

    conn.close()
