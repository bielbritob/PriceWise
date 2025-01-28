import zendriver as uc
from bs4 import BeautifulSoup

produt = 'arroz'
urls = {
    "ig": f"https://irmaosgoncalves.com.br/pesquisa?q={produt.replace(' ', '+')}&p=7&o=valor&t=asc",
    "meta21": f"https://supermercadometa21.instabuy.com.br/pesquisar?search={produt.replace(' ', '%20')}",
    "novaera": f"https://www.supernovaera.com.br/{produt.replace(' ', '%20')}?_q={produt.replace(' ', '%20')}&map=ft&order=OrderByPriceASC"
}

async def search_novaera():
    browser = await uc.start(headless=False)
    page = await browser.get(urls["novaera"])  # senao ele apenas pesquisa novaera

    #-----Espera a bomba carregar e selecina o selecionador de cidades-------------#
    await browser.wait(5) # a bomba leva ate 5seg para ...
    await page.wait_for('select[class="mercantilnovaera-appexample-0-x-buttonSelector"]')
    selecrbutton = await page.query_selector('select[class="mercantilnovaera-appexample-0-x-buttonSelector"]')
    await selecrbutton.mouse_click()
    await page.select('select.mercantilnovaera-appexample-0-x-buttonSelector')
    await browser.wait(1)
    # -----Espera a bomba carregar e selecina o selecionador de cidades-------------#


    #------Faz uma maracutaia para selecionar PVH----------------------"
    await selecrbutton.send_keys(text="p")
    enviar = await page.find('Enviar', best_match=True)
    await enviar.mouse_click()
    await browser.wait(4)
    await page.wait_for('div[class="mercantilnovaera-appexample-0-x-botaoSegundoModal"]')
    aceitar = await page.find("Confirmar", best_match=True)
    await aceitar.mouse_click()
    # ------Faz uma maracutaia para selecionar PVH----------------------"

    #==== Garantidor de q td nao varie =======#
    await browser.wait(4)

    #---- espera os prodto appear -----#
    await page.wait_for("span.vtex-product-price-1-x-currencyFraction.vtex-product-price-1-x-currencyFraction--summary",timeout=4)  # espera os produtos aparecer

    #------- select @a-------#
    produtos_novaera = await page.query_selector_all("div.vtex-search-result-3-x-galleryItem.vtex-search-result-3-x-galleryItem--normal.vtex-search-result-3-x-galleryItem--grid.pa4")

    for produtos in produtos_novaera[:3]:
        html_contentnovaera = await produtos.get_html()
        print(f'html: {html_contentnovaera}')
        # trata html
        soup = BeautifulSoup(html_contentnovaera, 'html.parser')
        # Extrai o nome do produto
        nome = soup.find('span', class_='vtex-product-summary-2-x-productBrand').text

        # Extrai o preço
        precoINT = soup.find('span', class_='vtex-product-price-1-x-currencyInteger').text
        precoDEC = soup.find('span', class_='vtex-product-price-1-x-currencyFraction').text
        preco = f"R$ {precoINT},{precoDEC}"

        # Extrai o link do produto
        link = soup.find('a')['href']
        link = f"https://www.supernovaera.com.br{link}"

        # Extrai a img src
        img_src = soup.find('img')['src']

        # log
        print("-" * 40)
        print(f"  Link: {link}")
        print(f"  Nome: {nome}")
        print(f"  Preço: {preco}")
        print(f"  Imagem: {img_src}")
        print("-" * 40)
        dados_produtos.append({"Mercado": "Nova Era", "Titulo": nome, "Preco": preco, "Img": img_src, "Link": link})
    print("Dados do Novaera coletado!")
    await browser.stop()

if __name__ == '__main__':
    uc.loop().run_until_complete(search_novaera())