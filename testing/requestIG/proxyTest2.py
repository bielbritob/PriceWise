import subprocess
import requests
import time

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
    if not ngrok_ja_esta_rodando():
        caminho_ngrok = r"C:\ProgramData\chocolatey\bin\ngrok.exe"
        comando = f'"{caminho_ngrok}" http 8080'
        subprocess.Popen(comando, shell=True)
        print("Ngrok iniciado.")
    else:
        print("Ngrok já está rodando. Obtendo url...")

def obter_url_ngrok():
    url_api = "http://127.0.0.1:4040/api/tunnels"
    tentativas = 10  # Número máximo de tentativas
    intervalo = 2  # Intervalo entre tentativas (em segundos)

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

        # Aguarda antes de tentar novamente
        time.sleep(intervalo)

    return None

# Inicia o Ngrok (se necessário)
iniciar_ngrok_se_necessario()

# Aguarda alguns segundos para o Ngrok iniciar (se necessário)
time.sleep(5)

# Captura a URL de forwarding
url = obter_url_ngrok()
if url:
    print(f"Ngrok Forwarding URL: {url}")
else:
    print("Não foi possível obter a URL do Ngrok.")