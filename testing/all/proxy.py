import subprocess
import threading
import requests
import time
from flask import Flask, request, jsonify, send_file
from flask_httpauth import HTTPBasicAuth
import sqlite3
from rich import print
import json

app = Flask(__name__)
auth = HTTPBasicAuth()

# Configuração de usuário e senha
USUARIO = "biel"
SENHA = "k2g9ekk6"

# Variável para armazenar a URL do Ngrok
ngrok_url = None

# Verifica o usuário e senha
@auth.verify_password
def verificar_senha(usuario, senha):
    if usuario == USUARIO and senha == SENHA:
        return True
    return False

# Rota para retornar a URL do Ngrok
@app.route('/ngrok_url', methods=['GET'])
@auth.login_required
def get_ngrok_url():
    global ngrok_url
    if ngrok_url:
        return jsonify({"ngrok_url": ngrok_url})
    else:
        return jsonify({"error": "Ngrok URL não disponível"}), 404

@app.route('/api/produto/pesquisar', methods=['GET'])
@auth.login_required
def pesquisar_produto():
    try:
        params = request.args.to_dict()
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
            'x-empresa': '20',
            'x-tipo-envio': '2',
        }
        response = requests.get(
            'https://www.irmaosgoncalves.com.br/api/produto/pesquisar',
            params=params,
            headers=headers
        )
        response.raise_for_status()
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
    except ValueError as e:
        return jsonify({"error": "Resposta inválida da API"}), 500

# Rota para baixar o banco de dados
@app.route('/download_db', methods=['GET'])
@auth.login_required
def download_db():
    try:
        return send_file('../produtos.db', as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota para atualizar o banco de dados
@app.route('/atualizar_db', methods=['POST'])
@auth.login_required
def atualizar_db():
    try:
        # Executa o código de coleta de dados do IG
        coletar_dados_ig()
        coletar_dados_meta21()
        coletar_dados_novaera()
        print("Todos os dados coletado com Success!!!")
        return jsonify({"status": "Banco de dados atualizado com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def coletar_dados_ig():
    # Conectar ao banco de dados SQLite3 (ou criar se não existir)
    conn = sqlite3.connect('../produtos.db')
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
        url = f"https://www.irmaosgoncalves.com.br/api/produto/pesquisar?&categoria={categoria}&pagina=200"
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

                # Verificar se o produto já existe no banco de dados (usando o campo 'ean' como chave única)
                cursor.execute('SELECT * FROM produtos WHERE ean = ?', (produto.get('ean'),))
                if cursor.fetchone() is None:
                    # Inserir no banco de dados
                    cursor.execute('''
                    INSERT INTO produtos (ean, mercado, nome, marca, url, valor, valorkg, valorAntigo, imagem)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        produto.get('ean'),
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
    conn = sqlite3.connect('../produtos.db')
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
                            INSERT INTO produtos (ean, mercado, nome, marca, url, valor, valorkg, valorAntigo, imagem)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                            ''', (
                                ean,
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
        if not isinstance(data, dict) or "data" not in data or "productSearch" not in data["data"] or "products" not in \
                data["data"]["productSearch"]:
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
            image_url = produto["items"][0]["images"][0].get(
                "imageUrl")  # Ajuste para acessar a URL da imagem corretamente
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

    print("Produtos NovaEra salvos no banco de dados 'produtos.db'.")

def ngrok_ja_esta_rodando():
    url_api = "http://127.0.0.1:4040/api/tunnels"
    try:
        response = requests.get(url_api)
        if response.status_code == 200:
            dados = response.json()
            return len(dados["tunnels"]) > 0
    except requests.exceptions.RequestException:
        pass
    return False

def iniciar_ngrok_se_necessario():
    global ngrok_url
    if not ngrok_ja_esta_rodando():
        caminho_ngrok = r"C:\ProgramData\chocolatey\bin\ngrok.exe"
        comando = f'"{caminho_ngrok}" http 8080'
        subprocess.Popen(comando, shell=True)
        print("Ngrok iniciado.")
    else:
        print("Ngrok já está rodando.")

def obter_url_ngrok():
    url_api = "http://127.0.0.1:4040/api/tunnels"
    tentativas = 10
    intervalo = 2

    for _ in range(tentativas):
        try:
            response = requests.get(url_api)
            if response.status_code == 200:
                dados = response.json()
                for tunnel in dados["tunnels"]:
                    if tunnel["proto"] == "https":
                        return tunnel["public_url"]
            else:
                print(f"Erro ao acessar a API do Ngrok: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")

        time.sleep(intervalo)

    return None

def ler_token():
    try:
        with open("../tokenGIT.txt", "r") as f:
            token = f.read().strip()  # Remove espaços em branco e quebras de linha
            return token
    except FileNotFoundError:
        print("Arquivo tokenGit.txt não encontrado.")
        return None

def criar_gist(url):
    token = ler_token()
    gist_url = "https://api.github.com/gists"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "public": True,
        "files": {
            "ngrok_url.txt": {
                "content": url
            }
        }
    }
    response = requests.post(gist_url, headers=headers, json=data)
    if response.status_code == 201:
        gist_id = response.json()["id"]
        print(f"Gist criado: https://gist.github.com/{gist_id}")
        return gist_id
    else:
        print("Erro ao criar Gist:", response.text)
        return None

def salvar_gist_id(gist_id):
    with open("../gist_id.txt", "w") as f:
        f.write(gist_id)
    # Faz commit e push do arquivo para o GitHub
    subprocess.run(["git", "add", "gist_id.txt"], shell=True)
    subprocess.run(["git", "commit", "-m", "Atualizando ID do Gist"], shell=True)
    subprocess.run(["git", "push"], shell=True)

def rodar_flask():
    app.run(port=8080)

if __name__ == '__main__':
    # Inicia o Ngrok (se necessário)
    iniciar_ngrok_se_necessario()

    # Aguarda alguns segundos para o Ngrok iniciar (se necessário)
    time.sleep(5)

    # Captura a URL de forwarding
    ngrok_url = obter_url_ngrok()
    if ngrok_url:
        print(f"Ngrok Forwarding URL: {ngrok_url}")
        # Cria um Gist com a URL
        gist_id = criar_gist(ngrok_url)
        if gist_id:
            print(f"URL do Ngrok compartilhada via Gist: https://gist.github.com/{gist_id}")
            # Salva o ID do Gist em um arquivo e faz commit/push
            salvar_gist_id(gist_id)
    else:
        print("Não foi possível obter a URL do Ngrok.")

    # Roda o Flask em uma thread separada
    flask_thread = threading.Thread(target=rodar_flask)
    flask_thread.start()
    flask_thread.join()