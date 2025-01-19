import os
import zendriver as uc


async def main():
    # Define o diretório temporário para o perfil do Chrome
    user_data_dir = "/tmp/chrome-profile2"
    os.makedirs(user_data_dir, exist_ok=True)  # Cria o diretório se não existir

    # Inicia o navegador com o perfil temporário
    browser = await uc.start(
        headless=True,  # Modo headless para o Streamlit Cloud
        user_data_dir=user_data_dir,  # Usa o diretório temporário
        browser_args=['--no-sandbox', '--disable-dev-shm-usage']  # Argumentos para o Chrome
    )

    # Abre a página desejada
    page = await browser.get('https://www.irmaosgoncalves.com.br/pesquisa?q=arroz')
    print(await page.get_content())
    await browser.stop()


if __name__ == '__main__':
    uc.loop().run_until_complete(main())


