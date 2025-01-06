from bs4 import BeautifulSoup
import nodriver as uc

# Variável para pesquisa
produt = "cafe 500g"

async def main():
    urls = {
        "ig": f"https://irmaosgoncalves.com.br/pesquisa?q={produt.replace(' ', '+')}&p=7&o=valor&t=asc",
        "meta21": f"https://supermercadometa21.instabuy.com.br/pesquisar?search={produt.replace(' ', '%20')}",
        "novaera": f"https://www.supernovaera.com.br/{produt.replace(' ', '%20')}?_q={produt.replace(' ', '%20')}&map=ft&order=OrderByPriceASC"
    }

    try:
        # Inicia Navegador...
        browser = await uc.start()

        # Seletor Mercado IG
        search_ig = True

        if search_ig:
            # Parte IrmaosGolcalves
            page = await browser.get(urls["ig"])
            ######################################################
            """
            nessa parte seleciona o endereço do mercado...
            """
            # Select button finder
            print("Procurando o botão 'Selecione a cidade'...")
            await page.wait_for("div.relative select", timeout=2)
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

            await browser.wait(2)

            # Selector dos produtos
            produtos_ig = await page.query_selector_all("div.relative.px-4.shadow-md.border.rounded-lg.min-h-max.pb-2.h-full")

            # Loop para achar attrs dos produtos
            for produto in produtos_ig[:3]:
                #Coleta
                html_content = await produto.get_html()
                print(html_content)# -> retorna um dicionario com tudo do produto, mas precisa tratar

                # trata html
                soup = BeautifulSoup(html_content, 'html.parser')

                # Extrai o nome do produto
                nome = soup.find('a', title=True).get('title')

                # Extrai o preço
                preco = soup.find('div', class_='text-xl text-secondary font-semibold h-7').text.strip()

                # Extrai a img src
                img_src = soup.find('img')['src']
                # log
                print(f"  Nome: {nome}")
                print(f"  Preço: {preco}")
                print(f"  Imagem: {img_src}")
                print("-" * 40)

            print("Dados do IG coletado!")


        # Seletor Mercado IG Meta21
        search_meta21 = False

        if search_meta21:
            # Meta21
            if search_ig:
                await page.get(urls["meta21"], new_tab=True) # se searchig= true ele apenas cria uma nova tab

            else:
                page = await browser.get(urls["meta21"]) # senao ele apenas pesquisa meta21

            await page.wait_for("div.css-0", timeout=2) # espera os produtos aparecer

            produtos_meta21 = await page.query_selector_all("div.ib-box._item-cell-container_t82s5_1")
            print(produtos_meta21)
            for produtos in produtos_meta21[:3]:
                html_contentmeta21 = await produtos.get_html()
                print(f'html: {html_contentmeta21}')
                # trata html
                soup = BeautifulSoup(html_contentmeta21, 'html.parser')

                # Extrai o nome do produto
                #nome = soup.find('p', class_='_item-cell-product-name_t82s5_18').text
                nome = soup.find('p', class_='_item-cell-product-name_t82s5_18').text

                # Extrai o preço
                preco = soup.find('p', class_='ib-text is-color-high is-text-large is-wrap-normal is-weight-bold is-decoration-none').text

                # Extrai a img src
                img_src = soup.find('img')['src']

                # log
                print(f"  Nome: {nome}")
                print(f"  Preço: {preco}")
                print(f"  Imagem: {img_src}")
                print("-" * 40)

            print("Dados do Meta21 coletado!")


        # Seletor Mercado NovaEra
        search_novaera = True

        if search_novaera:
            if search_meta21 :
                await page.get(urls["novaera"], new_tab=True)  # se searchmeta21= true ele apenas cria uma nova tab

            elif search_ig:

                await page.get(urls["novaera"], new_tab=True)  # se searchig= true ele apenas cria uma nova tab
                await browser.main_tab()
            else:
                page = await browser.get(urls["novaera"])  # senao ele apenas pesquisa novaera

            await browser.wait(4)
            print('procurando botao escolha')


            selecrbutton = await page.query_selector('select[class="mercantilnovaera-appexample-0-x-buttonSelector"]')
            print(selecrbutton)
            await selecrbutton.mouse_click()
            print('pos0')
            await page.select('select.mercantilnovaera-appexample-0-x-buttonSelector')
            await browser.wait(1)
            print('pos1')

            await selecrbutton.send_keys(text="p")
            pvh = await page.query_selector('option[value="Porto_Velho"]')

            print('pvh selecionado')
            await browser.wait(2)
            enviar = await page.find('Enviar', best_match=True)
            await enviar.mouse_click()
            await browser.wait(4)

            aceitar = await page.find("Confirmar", best_match=True)
            await aceitar.mouse_click()
            print('Enviado PVH...')

            await browser.wait(2)

            await page.wait_for("span.vtex-product-price-1-x-currencyFraction.vtex-product-price-1-x-currencyFraction--summary", timeout=4)  # espera os produtos aparecer

            produtos_novaera = await page.query_selector_all("div.vtex-search-result-3-x-galleryItem")
            print(produtos_novaera)
            for produtos in produtos_novaera[:3]:
                html_contentnovaera = await produtos.get_html()
                print(f'html: {html_contentnovaera}')
                # trata html
                soup = BeautifulSoup(html_contentnovaera, 'html.parser')

                # Extrai o nome do produto
                nome = soup.find('span', class_='vtex-product-summary-2-x-productBrand').text

                # Extrai o preço
                precoINT = soup.find('span',class_='vtex-product-price-1-x-currencyInteger').text
                precoDEC = soup.find('span',class_='vtex-product-price-1-x-currencyFraction').text
                preco = f"{precoINT},{precoDEC}"

                # Extrai a img src
                img_src = soup.find('img')['src']

                # log
                print(f"  Nome: {nome}")
                print(f"  Preço: {preco}")
                print(f"  Imagem: {img_src}")
                print("-" * 40)

            print("Dados do Novaera coletado!")

        await browser.wait(4)


    except Exception as e:
        print(f"Erro durante a execução: {e}")

if __name__ == '__main__':
    # Executa a função assíncrona
    uc.loop().run_until_complete(main())