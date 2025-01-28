import requests
from rich import print
import time
import sqlite3
import json
import subprocess
from datetime import datetime
import math

# Coleta de dados *Markets
def coletar_dados_ig():
    # Conectar ao banco de dados SQLite3 (ou criar se não existir)
    conn = sqlite3.connect('produtos.db')
    cursor = conn.cursor()

    # Criar a tabela se ela não existir
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ean TEXT UNIQUE,  -- Campo único para evitar duplicação
        mercado TEXT,
        nome TEXT,
        marca TEXT,
        url TEXT,
        valor REAL,
        valorkg REAL,
        valorAntigo REAL, 
        imagem TEXT
    )
    ''')
    conn.commit()

    # Configurações da requisição
    cookies = {
        'app': '%7B%22cidade%22%3A37%2C%22empresa%22%3A20%2C%22tipoEnvio%22%3A2%2C%22aceiteCookies%22%3Afalse%2C%22userName%22%3A%22%22%2C%22totalCart%22%3A%220%2C00%22%2C%22quantityCart%22%3A0%2C%22modalMergeCart%22%3Afalse%2C%22quantityCartBrowser%22%3A0%7D',
        'viewport': 'sm',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'pt-BR,pt;q=0.5',
        'authorization': 'undefined',
        'content-type': 'application/json',
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
        'x-empresa': '20',  # 20 = pvh; 122 = guajaráMirim
        'x-tipo-envio': '2',
    }

    # Lista de categorias
    categorias = [
        "/categoria/utilidades-e-casa",
        "/categoria/pet",
        "/categoria/peixes",
        "/categoria/papelaria",
        "/categoria/padaria",
        "/categoria/mercearia",
        "/categoria/magazine",
        "/categoria/limpeza",
        "/categoria/hortifruti",
        "/categoria/higiene-e-perfumaria",
        "/categoria/frios-e-laticínios",
        "/categoria/congelados--resfriados-e-sobremesas",
        "/categoria/calçados",
        "/categoria/bebidas-alcoólicas",
        "/categoria/bebidas",
        "/categoria/bebê-e-infantil",
        "/categoria/açougue"
    ]

    # Iterar sobre cada categoria e fazer a requisição
    for categoria in categorias:
        url = f"https://www.irmaosgoncalves.com.br/api/produto/pesquisar?&categoria={categoria}&pagina=2000"
        print(f"Buscando produtos da categoria: {categoria}")

        # Fazer a requisição à API
        response = requests.get(
            url,
            cookies=cookies,
            headers=headers,
        )

        # Verificar se a requisição foi bem-sucedida
        if response.status_code == 200:
            data = response.json()
            produtos = data.get('produtos', [])  # Acessar a lista de produtos

            # Inserir os produtos no banco de dados
            for produto in produtos:
                # Formatar a URL e a imagem
                url_completa = f"https://www.irmaosgoncalves.com.br{produto.get('url')}"
                imagem_completa = f"https://conteudo.irmaosgoncalves.com.br/produto{produto.get('imagem')}"
                ean = f"IgEan: {produto.get('ean')}"
                # Verificar se o produto já existe no banco de dados (usando o campo 'ean' como chave única)
                cursor.execute('SELECT * FROM produtos WHERE ean = ?', (produto.get('ean'),))
                if cursor.fetchone() is None:
                    # Inserir no banco de dados
                    cursor.execute('''
                    INSERT OR REPLACE INTO produtos (ean, mercado, nome, marca, url, valor, valorkg, valorAntigo, imagem)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        ean,
                        'Irmãos Gonçalves',
                        produto.get('nome'),
                        produto.get('marca'),
                        url_completa,
                        produto.get('valor'),
                        produto.get('valorKg'),
                        produto.get('valorAntigo'),
                        imagem_completa
                    ))
            conn.commit()
            print(f"Produtos da categoria {categoria} salvos com sucesso!")
        else:
            print(f"Erro na requisição para a categoria {categoria}: {response.status_code}")

    # Fechar a conexão com o banco de dados
    conn.close()

    print("Produtos IG salvos no banco de dados 'produtos.db'.")

def coletar_dados_meta21():
    # Conectar ao banco de dados SQLite3 (ou criar se não existir)
    conn = sqlite3.connect('produtos.db')
    cursor = conn.cursor()

    # Criar a tabela se ela não existir
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ean TEXT UNIQUE,  -- Campo único para evitar duplicação
        mercado TEXT,
        nome TEXT,
        marca TEXT,
        url TEXT,
        valor REAL,
        valorkg REAL,
        valorAntigo REAL, 
        imagem TEXT
    )
    ''')
    conn.commit()

    # Configurações da requisição
    headers = {
        'accept': '*/*',
        'accept-language': 'pt-BR,pt;q=0.5',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36',
    }

    # Lista de IDs das subcategorias
    subcategorias = [
        "65216bca0c9d838df85e8f95",  # Frutas
        "65216bca0c9d838df85e8f96",  # Frutas secas e oleaginosas
        "65216bca0c9d838df85e8f97",  # Legumes
        "65216bca0c9d838df85e8f98",  # Ovos
        "65216bca0c9d838df85e8f9a",  # Verduras
        "65216bca0c9d838df85e8fa2",  # Aves e frangos
        "65216bca0c9d838df85e8fa3",  # Bovinos
        "65216bca0c9d838df85e8fa5",  # Linguiças
        "65216bca0c9d838df85e8fa7",  # Peixaria
        "65216bca0c9d838df85e8fa9",  # Suínos
        "65216bcb0c9d838df85e8fab",  # Bebidas Lácteas
        "65216bcb0c9d838df85e8fac",  # Iogurtes
        "65216bcb0c9d838df85e8fad",  # Leites
        "65216bcb0c9d838df85e8fae",  # Manteigas e Margarinas
        "65216bcb0c9d838df85e8fb0",  # Massas Resfriadas
        "65216bcb0c9d838df85e8fb2",  # Queijos
        "65216bcb0c9d838df85e8fb3",  # Requeijão
        "65216bcb0c9d838df85e8fb4",  # Sobremesas
        "65216bcb0c9d838df85e8fb8",  # Arroz
        "65216bcb0c9d838df85e8fb7",  # Açucar
        "65216bcb0c9d838df85e8fba",  # Farinhas e Farofas
        "65216bcb0c9d838df85e8fbb",  # Feijão
        "65216bcb0c9d838df85e8fbc",  # Grãos
        "65216bcb0c9d838df85e8fbe",  # Sal
        "65216bcb0c9d838df85e8fbd",  # Óleo
        "65216bcb0c9d838df85e8fc2",  # Cachaças
        "65216bcb0c9d838df85e8fc3",  # Cervejas
        "65216bcb0c9d838df85e8fc4",  # Conhaque
        "65216bcb0c9d838df85e8fc5",  # Drinques Prontos
        "65216bcb0c9d838df85e8fc6",  # Gin
        "65216bcb0c9d838df85e8fc8",  # Licores e Aperitivos
        "65216bcc0c9d838df85e8fca",  # Vodka
        "65216bcc0c9d838df85e8fcc",  # Whisky
        "65216bcc0c9d838df85e8fcf",  # A base de Vegetais
        "65216bcc0c9d838df85e8fd0",  # Energeticos e Isotonicos
        "65216bcc0c9d838df85e8fd1",  # Refrescos
        "65216bcc0c9d838df85e8fd2",  # Refrigerantes
        "65216bcc0c9d838df85e8fd3",  # Sucos
        "65216bcc0c9d838df85e8fd5",  # Agua de coco
        "65216bcc0c9d838df85e8fd7",  # Aguas Minerais
        "65216bcc0c9d838df85e8fdc",  # Achocolatados
        "65216bcc0c9d838df85e8fdd",  # Adoçantes
        "65216bcc0c9d838df85e8fde",  # Biscoitos
        "65216bcc0c9d838df85e8fdf",  # Cafés e Capsulas
        "65216bcc0c9d838df85e8fe0",  # Careais
        "65216bcc0c9d838df85e8fe1",  # Chas
        "65216bcc0c9d838df85e8fe3",  # Geleias
        "65216bcc0c9d838df85e8fe4",  # Leites em pó
        "65216bcc0c9d838df85e8fe6",  # Torradas
        "65216bcc0c9d838df85e8fe9",  # Azeites
        "65216bcc0c9d838df85e8fea",  # Batata Palha
        "65216bcd0c9d838df85e8feb",  # bonboniere
        "65216bcd0c9d838df85e8fec",  # Chocolate em pó
        "65216bcd0c9d838df85e8fed",  # Conservas e enlatados
        "65216bcd0c9d838df85e8fee",  # Derivados de tomate
        "65216bcd0c9d838df85e8fef",  # doces e compostas
        "65216bcd0c9d838df85e8ff0",  # especiarias e temperos
        "65216bcd0c9d838df85e8ff2",  # gelatinas
        "65216bcd0c9d838df85e8ff3",  # leites condensados e cremes de leite
        "65216bcd0c9d838df85e8ff4",  # leites de coco e coco ralado
        "65216bcd0c9d838df85e8ff5",  # maioneses, ketchups e mostardas
        "65216bcd0c9d838df85e8ff7",  # Massas tradicionais e instantaneas
        "65216bcd0c9d838df85e8ff8",  # Molhos diversos
        "65216bcd0c9d838df85e8ff9",  # Pipocas
        "65216bcd0c9d838df85e8ffb",  # Snacks e aperitivos
        "65216bcd0c9d838df85e8ffc",  # sopas instaneas
        "65216bcd0c9d838df85e8ffe",  # vinagres
        "65216bcd0c9d838df85e9001",  # Embutidos
        "65216bce0c9d838df85e9002",
        "65216bce0c9d838df85e9004",
        "65216bce0c9d838df85e9005",
        "65216bce0c9d838df85e9006",
        "65216bcf0c9d838df85e9010",
        "65216bcf0c9d838df85e9016",
        "65216bcf0c9d838df85e9013",
        "65216bcf0c9d838df85e9014",
        "65216bcf0c9d838df85e9015",
        "65216bd00c9d838df85e9019",
        "65216bd00c9d838df85e901a",
        "65216bd00c9d838df85e901c",
        "65216bd00c9d838df85e9021",
        "65216bd00c9d838df85e9023",
        "65216bd00c9d838df85e9024",
        "65216bd00c9d838df85e9025",
        "65216bd10c9d838df85e902a",
        "65216bd10c9d838df85e902b",
        "65216bd10c9d838df85e902c",
        "65216bd10c9d838df85e902d",
        "65216bd10c9d838df85e902e",
        "65216bd10c9d838df85e902f",
        "65216bd10c9d838df85e9030",
        "65216bd10c9d838df85e9031",
        "65216bd10c9d838df85e9033",
        "65216bd20c9d838df85e9034",
        "65216bd20c9d838df85e9035",
        "65216bd20c9d838df85e903b",
        "65216bd20c9d838df85e903d",
        "65216bd20c9d838df85e903e",
        "65216bd20c9d838df85e903f",
        "65216bd20c9d838df85e9040",
        "65216bd20c9d838df85e9042",
        "65216bd20c9d838df85e9043",
        "65216bd20c9d838df85e9044",
        "65216bd30c9d838df85e9046",
        "65216bd30c9d838df85e904d",
        "65216bd30c9d838df85e9049",
        "65216bd30c9d838df85e904b",
        "65216bd30c9d838df85e904f",
        "65216bd30c9d838df85e9047",
        "65216bd30c9d838df85e9055",
        "65216bd30c9d838df85e9058",
        "65216bd30c9d838df85e9059",
        "65216bd30c9d838df85e905a",
        "65216bd30c9d838df85e905b",
        "65216bd30c9d838df85e905d",
        "65216bd30c9d838df85e905e",
        "65216bd30c9d838df85e9061",
        "65216bd30c9d838df85e9062",
        "65216bd30c9d838df85e9063",
        "65216bd30c9d838df85e9064",
        "65216bd30c9d838df85e9065",
        "665772e2d4ab036ecd154a89"
    ]

    # Função para processar produtos de uma subcategoria
    def processar_subcategoria(subcategoria_id):
        url = f"https://api.instabuy.com.br/apiv3/item?subdomain=supermercadometa21&N=2000&page=1&subcategory_id={subcategoria_id}&sort=top_sellers"
        print(f"Buscando produtos da subcategoria ID: {subcategoria_id}")

        try:
            # Fazer a requisição à API
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Levanta uma exceção para códigos de status HTTP ruins

            data = response.json()

            # Verificar se a subcategoria tem dados
            if 'data' in data and data['data']:
                # Iterar sobre cada produto dentro de 'data'
                for produto in data['data']:
                    # Verificar se o produto está em estoque
                    if produto.get('stock_infos', {}).get('stock_balance', 0) > 0:
                        # Formatar a URL e a imagem
                        url_completa = f"https://supermercadometa21.instabuy.com.br/p/{produto.get('slug')}"
                        imagem_completa = f"https://ibassets.com.br/ib.item.image.big/b-{produto.get('images')[0]}" if produto.get(
                            'images') else None

                        # Verificar se o produto tem preços e códigos de barras
                        prices = produto.get('prices', [])
                        if prices:  # Se houver preços
                            bar_codes = prices[0].get('bar_codes', [])
                            ean = bar_codes[0] if bar_codes else None  # Pega o primeiro código de barras, se existir
                        else:
                            ean = None

                        # Se não houver EAN, usar o ID do produto como EAN
                        if not ean:
                            ean = produto.get('id')  # Usar o ID do produto como EAN

                        # Verificar se o produto já existe no banco de dados (usando o campo 'ean' como chave única)
                        cursor.execute('SELECT * FROM produtos WHERE ean = ?', (ean,))
                        if cursor.fetchone() is None:
                            # Inserir no banco de dados
                            cursor.execute('''
                            INSERT OR REPLACE INTO produtos (ean, mercado, nome, marca, url, valor, valorkg, valorAntigo, imagem)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                            ''', (
                                f"Meta21Ean: {ean}",
                                'Meta21',
                                produto.get('name'),
                                produto.get('brand', ''),  # Usar string vazia se 'brand' não existir
                                url_completa,
                                produto.get('min_price_valid'),
                                None,  # valorkg não disponível
                                None,  # valorAntigo não disponível
                                imagem_completa
                            ))
                conn.commit()
                print(f"Produtos da subcategoria ID {subcategoria_id} salvos com sucesso!")
            else:
                print(f"Nenhum dado encontrado para a subcategoria ID {subcategoria_id}")

        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição para a subcategoria ID {subcategoria_id}: {e}")
        except Exception as e:
            print(f"Erro ao processar a subcategoria ID {subcategoria_id}: {e}")

    # Iterar sobre cada subcategoria e processar
    for subcategoria_id in subcategorias:
        processar_subcategoria(subcategoria_id)

    # Fechar a conexão com o banco de dados
    conn.close()

    print("Produtos Meta21 salvos no banco de dados 'produtos.db'.")

def coletar_dados_novaera():
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

    print("Produtos NovaEra salvos no banco de dados 'produtos.db'.")


def coletar_dados_atacadao():
    def fetch_products_by_category(base_url, category, first=20):
        all_products = []  # Lista para armazenar todos os produtos de uma categoria
        offset = 0  # Deslocamento inicial
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
                {"key": "channel",
                 "value": '{"salesChannel":"2","seller":"atacadaobr213","regionId":"U1cjYXRhY2FkYW9icjIxMw=="}'},
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
        total_count = data.get("data", {}).get("search", {}).get("products", {}).get("pageInfo", {}).get("totalCount",
                                                                                                         0)
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
            stock = produto["node"]["sellers"][0]["commertialOffer"].get("AvailableQuantity")
            print(stock)
            if stock > 0:
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
                        INSERT OR REPLACE INTO produtos (ean, mercado, nome, marca, url, valor, valorkg, valorAntigo, imagem)
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
            else:
                print('produto sem Estoque < 0')

        conn.close()
    print("dados do atacadão salvo com sucesso!!!")

# Função para salvar a data de envio em um arquivo
def salvar_data_envio():
    data_atual = datetime.now().strftime("%d/%m/%Y")
    with open("last_sent_date.txt", "w") as f:
        f.write(data_atual)


# Função para enviar DB e lsd para o GitHub
def enviar_para_github():
    data_atual = datetime.now().strftime("%d/%m/%Y")
    subprocess.run(["git", "add", "produtos.db"])
    subprocess.run(["git", "add", "last_sent_date.txt"])
    subprocess.run(["git", "commit", "-m", f"Atualização diária do banco de dados - dia: {data_atual}"])
    subprocess.run(["git", "push"])



coletar_dados_ig()
coletar_dados_meta21()
coletar_dados_novaera()
coletar_dados_atacadao()
print("Todos os dados coletado com Success!!!")
salvar_data_envio()
enviar_para_github()


