import requests
import sqlite3
from rich import print

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
                    imagem_completa = f"https://ibassets.com.br/ib.item.image.big/b-{produto.get('images')[0]}" if produto.get('images') else None

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