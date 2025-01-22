from playwright.async_api import async_playwright
import asyncio

async def main():
    async with async_playwright() as playwright:
        # Configuração do proxy
        proxy = {
            "server": "http://192.168.1.23:8080",  # Substitua pelo IP do seu PC e a porta HTTP
            "username": "stCloud",  # Se configurado no CCProxy
            "password": "4088390"     # Se configurado no CCProxy
        }

        # Inicia o navegador com o proxy
        browser = await playwright.chromium.launch(headless=False, proxy=proxy,slow_mo=100)
        page = await browser.new_page()

        # Navega até um site que exibe o IP
        await page.goto("https://api.ipify.org?format=json")
        ip_info = await page.content()
        print("IP usado pelo proxy:", ip_info)

        # Fecha o navegador
        await browser.close()

asyncio.run(main())