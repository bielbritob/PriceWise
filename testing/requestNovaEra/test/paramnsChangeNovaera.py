import requests
import json
import time

# URL da API
url = "https://www.supernovaera.com.br/_v/segment/graphql/v1"

# Cabeçalhos
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "application/json",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
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
        response = requests.get(url, params=params, headers=headers)
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
limite_produtos = 3212  # Limite máximo de produtos

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
    if not isinstance(data, dict) or "data" not in data or "productSearch" not in data["data"] or "products" not in data["data"]["productSearch"]:
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

# Exibir total de produtos coletados
print(f"Total de produtos coletados: {len(todos_produtos)}")

# Salvar os produtos em um arquivo JSON (opcional)
with open("todos_produtos.json", "w", encoding="utf-8") as f:
    json.dump(todos_produtos, f, ensure_ascii=False, indent=2)

print("Produtos salvos em 'todos_produtos.json'.")