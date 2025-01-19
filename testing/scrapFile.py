import os
import zendriver as uc
import random
import sys

USER_AGENTS = [
    "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
    "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1",
]

produto = sys.argv[1]

seletorC = sys.argv[2]
print(seletorC)
def get_random_user_agent(user_agents):
    return random.choice(user_agents)

async def main():
    random_user_agent = get_random_user_agent(USER_AGENTS)
    # Define o diretório temporário para o perfil do Chrome
    user_data_dir = "/tmp/chrome-profile5"
    os.makedirs(user_data_dir, exist_ok=True)  # Cria o diretório se não existir

    # Inicia o navegador com o perfil temporário
    browser = await uc.start(
        headless=True,
        user_agent=random_user_agent,
        user_data_dir=user_data_dir,  # Usa o diretório temporário
        browser_args=['--no-sandbox', '--disable-dev-shm-usage']  # Argumentos para o Chrome
    )

    # Abre a página desejada
    page = await browser.get(f'https://www.irmaosgoncalves.com.br/pesquisa?q={produto}')
    if seletorC:
        print("Procurando o botão 'Selecione a cidade'...")
        await page.wait_for("div.relative select", timeout=2)
        selectb = await page.select("div.relative select")
        print(selectb)
        await selectb.mouse_click()

        # -----------Select pvh maracutay
        cities = await page.query_selector_all("option[class]")
        pvh = cities[7]
        print(cities[7])
        # await page.sleep(1)
        await pvh.select_option()
        # await page.sleep(1)
        await selectb.mouse_click()
        print("Porto Velho Selected!")

        # --------------- Select Av sete de setembro
        localend = await page.find("AV. SETE DE SETEMBRO, n°")
        print(localend)
        a = await localend.get_html()
        await localend.click()
        print("s&lected AV. SETE DE SEPTEMBER my friend...")
        await browser.wait(2)
        print(await page.get_content())
    else:
        print(await page.get_content())

    # Salva o screenshot no diretório temporário
    screenshot_path = "/tmp/screenshot.png"
    await page.save_screenshot(screenshot_path)
    print(f"Screenshot salvo em: {screenshot_path}")

    await browser.stop()

if __name__ == '__main__':
    uc.loop().run_until_complete(main())
