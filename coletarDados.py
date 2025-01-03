import json
import sys
from playwright.sync_api import sync_playwright

def extrair_produtos(produto):
    try:
        # Link corrigido com ordenação ascendente
        url = f"https://irmaosgoncalves.com.br/pesquisa?q={produto.replace(' ', '+')}&p=7&o=valor&t=asc"
        print(f"Acessando a URL: {url}")  # Log para depuração

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)
            page.wait_for_selector("a[title]")
            produtos = page.query_selector_all("a[title]")
            dados_produtos = []
            for produto in produtos:
                titulo = produto.get_attribute("title")
                preco_element = produto.query_selector("xpath=following::div[contains(@class, 'text-xl')][1]")
                preco = preco_element.inner_text() if preco_element else "Preço não encontrado"
                dados_produtos.append({"Título": titulo, "Preço": preco})
            browser.close()
            return dados_produtos
    except Exception as e:
        print(f"Erro durante a coleta de dados: {e}")  # Log para depuração
        return []

def salvar_dados_json(dados, arquivo="dados_produtos.json"):
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        produto_pesquisa = sys.argv[1]
        resultados = extrair_produtos(produto_pesquisa)
        salvar_dados_json(resultados)
        print("Dados salvos em dados_produtos.json")
    else:
        print("Por favor, forneça um produto para pesquisar.")