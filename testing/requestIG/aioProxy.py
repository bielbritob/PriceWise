import os
import time
import subprocess
import threading
from subprocess import check_output

from flask import Flask, request, jsonify
import requests
from flask_httpauth import HTTPBasicAuth
import re

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


def rodar_ngrok():
    # Caminho completo para o executável do Ngrok
    caminho_ngrok = r"C:\ProgramData\chocolatey\bin\ngrok.exe"

    # Configura o token de autenticação
    token = "2rzXS6TIo5qZ9DLF4yO70NYafSJ_4ZCEZtPjr1rLGVqB8gVQo"  # Substitua pelo seu token
    comando_config = f'"{caminho_ngrok}" config add-authtoken {token}'
    subprocess.run(comando_config, shell=True, check=True)

    # Inicia o Ngrok
    comando_tunnel = f'"{caminho_ngrok}" http 8080'
    process = subprocess.Popen(comando_tunnel, shell=True, stdout=subprocess.PIPE, text=True)
    time.sleep(4)
    print(process.stdout)
    out = check_output(comando_tunnel)

url = None
if url:
    print(f"URL capturada: {url}")
else:
    print("Não foi possível obter a URL do Ngrok.")

def rodar_flask():
    app.run(port=8080)


if __name__ == '__main__':
    # Encerra sessões ativas do Ngrok
    subprocess.run("taskkill /f /im ngrok.exe", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Roda o Ngrok em segundo plano
    rodar_ngrok()

    # Aguarda alguns segundos para o Ngrok iniciar
    time.sleep(5)
    print('posTS')

    # Roda o Flask em uma thread separada
    flask_thread = threading.Thread(target=rodar_flask)
    flask_thread.start()

    # Aguarda a thread do Flask terminar (isso nunca acontece, pois o Flask roda indefinidamente)
    flask_thread.join()