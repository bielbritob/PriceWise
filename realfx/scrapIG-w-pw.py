from playwright.async_api import async_playwright, Playwright
import asyncio
import random
import os

produt = 'arroz'

urls = {
    "ig": f"https://irmaosgoncalves.com.br/pesquisa?q={produt.replace(' ', '+')}&p=7&o=valor&t=asc"
}

user_agents = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; SM-A505FN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
]

ug = {
    "X-Forwarded-For": "123.456.789.012"
}
async def run_search_ig(playwright: Playwright):
    chromium = playwright.chromium  # Chromium
    p = playwright.devices
    user_agent = random.choice(user_agents)  # Escolhe um user-agent aleatório
    browser = await chromium.launch(headless=True)  # Inicia o navegador (modo headless=False para debug)

    # Verifica se o arquivo de sessão já existe
    if os.path.exists("session.json"):
        # Carrega o estado da sessão salvo
        context = await browser.new_context(user_agent="X-Forwarded-For: 123.456.789.012", storage_state="session.json")
        print("Estado da sessão carregado!")
    else:
        # Cria um novo contexto (sem estado de sessão)
        context = await browser.new_context(user_agent="X-Forwarded-For": "123.456.789.012")
        print("Nova sessão criada!")

    page = await context.new_page()  # Nova página

    try:
        # Navega até a URL
        print("Navegando até a página...")
        await page.goto(urls['ig'])
        await page.wait_for_load_state("networkidle")  # Espera o carregamento completo
        print("Página carregada!")

        # Verifica se a cidade já foi selecionada
        if not os.path.exists("session.json"):
            print("Selecionando cidade e endereço pela primeira vez...")

            # Aguarda o combobox da cidade estar disponível
            print("Aguardando combobox da cidade...")
            await page.wait_for_selector('select[class="text-gray-500 border-gray-400 block px-2.5 py-2 w-full text-sm bg-transparent rounded-lg border focus:outline-none focus:ring-0 focus:border-gray-600 peer"]', state="visible", timeout=10000)  # 10 segundos de timeout
            print("Combobox encontrado!")

            # Seleciona a cidade (Porto Velho)
            await page.select_option('select[class="text-gray-500 border-gray-400 block px-2.5 py-2 w-full text-sm bg-transparent rounded-lg border focus:outline-none focus:ring-0 focus:border-gray-600 peer"]', value="37")  # Seleciona PVH
            print("Cidade selecionada!")

            # Aguarda o radio button do endereço estar disponível
            print("Aguardando radio button do endereço...")
            await page.wait_for_selector('label[class="text-xs text-gray-500 cursor-pointer"][for="20"]', timeout=10000)  # 10 segundos de timeout
            print("Radio button encontrado!")

            # Seleciona o endereço (AV. SETE DE SETEMBRO, n°)
            await page.click('label[class="text-xs text-gray-500 cursor-pointer"][for="20"]', timeout=10000)
            print("Endereço selecionado!")

            # Salva o estado da sessão
            storage_state = await context.storage_state(path="session.json")
            print("Estado da sessão salvo!")

        # Captura o conteúdo da página
        page_content = await page.content()
        print(page_content)

        # Captura um screenshot para debug
        await page.screenshot(path="screenshot.png")

        # Verifica se há bloqueios
        if await page.query_selector("text=Access Denied"):
            print("Bloqueado!")
        else:
            print("Página carregada com sucesso!")

        await page.pause()  # Pausa para debug

    except Exception as e:
        print(f"Erro durante a execução: {e}")
    finally:
        # Fecha o navegador após a execução
        await browser.close()

async def main():
    async with async_playwright() as pw:
        await run_search_ig(pw)

asyncio.run(main())