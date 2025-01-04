import json
import sys
import asyncio
from playwright.async_api import async_playwright

async def extrair_produtos(produto):
    try:
        # Dicionário de URLs
        urls = {
            "ig": f"https://irmaosgoncalves.com.br/pesquisa?q={produto.replace(' ', '+')}&p=7&o=valor&t=asc",
            "meta21": f"https://supermercadometa21.instabuy.com.br/pesquisar?search={produto.replace(' ', '%20')}",
            "novaera": f"https://www.supernovaera.com.br/{produto.replace(' ', '%20')}?_q={produto.replace(' ', '%20')}&map=ft&order=OrderByPriceASC"
        }

        dados_produtos = []

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()

            # Irmãos Gonçalves
            await page.goto(urls["ig"])
            await page.wait_for_load_state("networkidle")
            await page.wait_for_selector("a[title]")
            produtos_ig = await page.query_selector_all("a[title]")
            for produto in produtos_ig:
                titulo = await produto.get_attribute("title")
                preco_element = await produto.query_selector("xpath=following::div[contains(@class, 'text-xl')][1]")
                preco = await preco_element.inner_text() if preco_element else "Preço não encontrado"
                dados_produtos.append({"Mercado": "Irmãos Gonçalves", "Título": titulo, "Preço": preco})

            # Meta 21
            await page.goto(urls["meta21"])
            await page.wait_for_selector("div.ib-box._item-cell-container_t82s5_1")
            produtos_meta21 = await page.query_selector_all("div.ib-box._item-cell-container_t82s5_1")
            for produto in produtos_meta21:
                titulo_element = await produto.query_selector(
                    "p.ib-text.is-color-medium.is-text-medium.is-wrap-normal.is-weight-regular.is-decoration-none._item-cell-product-name_t82s5_18")
                titulo = await titulo_element.inner_text() if titulo_element else "Título não encontrado"
                preco_element = await produto.query_selector(
                    "p.ib-text.is-color-high.is-text-large.is-wrap-normal.is-weight-bold.is-decoration-none")
                preco = await preco_element.inner_text() if preco_element else "Preço não encontrado"
                dados_produtos.append({"Mercado": "Meta 21", "Título": titulo, "Preço": preco})

            # Supernova
            await page.goto(urls["novaera"])
            await page.locator("select").select_option("Porto_Velho")
            await page.get_by_role("button", name="Enviar").click()
            await page.get_by_role("button", name="Confirmar").click()
            await page.wait_for_selector("div.vtex-search-result-3-x-galleryItem")
            produtos_novaera = await page.query_selector_all("div.vtex-search-result-3-x-galleryItem")
            for produto in produtos_novaera:
                titulo_element = await produto.query_selector("span.vtex-product-summary-2-x-productBrand")
                titulo = await titulo_element.inner_text() if titulo_element else "Título não encontrado"
                preco_inteiro = await produto.query_selector("span.vtex-product-price-1-x-currencyInteger")
                preco_decimal = await produto.query_selector("span.vtex-product-price-1-x-currencyFraction")
                preco = f"{await preco_inteiro.inner_text()},{await preco_decimal.inner_text()}" if preco_inteiro and preco_decimal else "Preço não encontrado"
                dados_produtos.append({"Mercado": "Supernova", "Título": titulo, "Preço": preco})

            await browser.close()
            return dados_produtos

    except Exception as e:
        print(f"Erro durante a coleta de dados: {e}")
        return []

def salvar_dados_json(dados, arquivo="dados_produtos.json"):
    try:
        # Carrega os dados existentes
        with open(arquivo, "r", encoding="utf-8") as f:
            dados_existentes = json.load(f)
    except FileNotFoundError:
        dados_existentes = []

    # Adiciona os novos dados
    dados_existentes.extend(dados)

    # Salva os dados atualizados
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados_existentes, f, ensure_ascii=False, indent=4)

async def main(produto_pesquisa):
    resultados = await extrair_produtos(produto_pesquisa)
    salvar_dados_json(resultados)
    print("Dados salvos em dados_produtos.json")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        produto_pesquisa = sys.argv[1]
        asyncio.run(main(produto_pesquisa))
    else:
        print("Por favor, forneça um produto para pesquisar.")