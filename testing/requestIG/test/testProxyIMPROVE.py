import os
import time
import subprocess
import threading
from subprocess import check_output

from flask import Flask, request, jsonify
import requests
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

# Configuração de usuário e senha
USUARIO = "biel"
SENHA = "k2g9ekk6"


# Verifica o usuário e senha
@auth.verify_password
def verificar_senha(usuario, senha):
    if usuario == USUARIO and senha == SENHA:
        return True
    return False


@app.route('/api/produto/pesquisar', methods=['GET'])
@auth.login_required  # Exige autenticação para acessar essa rota
def pesquisar_produto():
    try:
        # Parâmetros da requisição
        params = request.args.to_dict()

        # Headers necessários para a API do IG
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

        # Faz a requisição para a API do IG
        response = requests.get(
            'https://www.irmaosgoncalves.com.br/api/produto/pesquisar',
            params=params,
            headers=headers
        )

        # Verifica se a resposta é um JSON válido
        response.raise_for_status()  # Lança uma exceção se o status não for 2xx
        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        # Captura erros de requisição (conexão, timeout, etc.)
        return jsonify({"error": str(e)}), 500
    except ValueError as e:
        # Captura erros de JSON inválido
        return jsonify({"error": "Resposta inválida da API"}), 500




def rodar_ngrok():
    """WORKs, but dont return forward url"""
    # Caminho completo para o executável do Ngrok
    caminho_ngrok = r"C:\ProgramData\chocolatey\bin\ngrok.exe"
    comando = f'"{caminho_ngrok}" http 8080'
    p = subprocess.Popen(comando, stdout=subprocess.PIPE)

def alt_run_ngrok():
    caminho_ngrok = r"C:\ProgramData\chocolatey\bin\ngrok.exe"
    comando = f'"{caminho_ngrok}" http 8080'
    p = subprocess.Popen(comando, stdout=subprocess.PIPE)
    time.sleep(0.12)
    print(" [NGROK LOG] ".center(100, "_"))


def rodar_flask():
    # Roda o Flask
    app.run(port=8080)


if __name__ == '__main__':
    # Roda o Ngrok em segundo plano
    #rodar_ngrok()
    print(" [NGROK LOG] ".center(100, "_"))

    alt_run_ngrok()

    # Aguarda alguns segundos para o Ngrok iniciar
    time.sleep(5)

    # Roda o Flask em uma thread separada
    flask_thread = threading.Thread(target=rodar_flask)
    flask_thread.start()
    # Aguarda a thread do Flask terminar (isso nunca acontece, pois o Flask roda indefinidamente)
    flask_thread.join()