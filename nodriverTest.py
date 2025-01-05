import nodriver as uc

# Variável para pesquisa
produto = "cafe"

async def main():
    urls = {
        "ig": f"https://irmaosgoncalves.com.br/pesquisa?q={produto.replace(' ', '+')}&p=7&o=valor&t=asc",
        "meta21": f"https://supermercadometa21.instabuy.com.br/pesquisar?search={produto.replace(' ', '%20')}",
        "novaera": f"https://www.supernovaera.com.br/{produto.replace(' ', '%20')}?_q={produto.replace(' ', '%20')}&map=ft&order=OrderByPriceASC"
    }

    try:
        # Inicia Navegador...
        browser = await uc.start()
        page = await browser.get(urls["ig"])

        ######################################################
        """
        nessa parte seleciona o endereço do mercado...
        """
        # Select button finder
        print("Procurando o botão 'Selecione a cidade'...")
        selectb = await page.select("div.relative select")
        print(selectb)
        await selectb.mouse_click()

        await page.wait(2)

        # Select pvh
        cities = await page.query_selector_all("option[class]")
        pvh = cities[7]
        print(cities[7])
        await page.sleep(1)
        await pvh.select_option()
        await page.sleep(1)
        await selectb.mouse_click()
        print("Porto Velho Selected!")

        # Select Av sete de setembro
        localend = await page.find("AV. SETE DE SETEMBRO, n°")
        print(localend)
        await localend.click()
        print("& AV. SETE DE SEPTEMBER my frined...")
        ######################################################


        await page

        # Get scrap dada
        product = await page.find("Refrigerante Coca-Cola Plus Café Lata 220ml")
        print(f"product1: {product}")
        product2 = await page.select_all("div.relative.px-4.shadow-md.border.rounded-lg.min-h-max.pb-2.h-full")
        print(product2)
        print(f"Total de produtos encontrados: {len(product2)}")


        await browser.wait(12)

    except Exception as e:
        print(f"Erro durante a execução: {e}")

if __name__ == '__main__':
    # Executa a função assíncrona
    uc.loop().run_until_complete(main())