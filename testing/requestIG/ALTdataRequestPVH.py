import requests
import sqlite3
from rich import print

# Conectar ao banco de dados SQLite3 (ou criar se não existir)
conn = sqlite3.connect('produtos.db')
cursor = conn.cursor()

# Criar a tabela se ela não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ean TEXT UNIQUE,  -- Campo único para evitar duplicação
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
                INSERT INTO produtos (ean, nome, marca, url, valor, valorkg, valorAntigo, imagem)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    produto.get('ean'),
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