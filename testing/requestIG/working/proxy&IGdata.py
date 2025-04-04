import subprocess
import threading
import requests
import time
from flask import Flask, request, jsonify, send_file
from flask_httpauth import HTTPBasicAuth
import os

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