import json
import sys
from bs4 import BeautifulSoup
import zendriver as uc
import random

# Variável para pesquisa
produt = sys.argv[1]

market= sys.argv[2]

urls = {
    "ig": f"https://irmaosgoncalves.com.br/pesquisa?q={produt.replace(' ', '+')}&p=7&o=valor&t=asc",
    "meta21": f"https://supermercadometa21.instabuy.com.br/pesquisar?search={produt.replace(' ', '%20')}",
    "novaera": f"https://www.supernovaera.com.br/{produt.replace(' ', '%20')}?_q={produt.replace(' ', '%20')}&map=ft&order=OrderByPriceASC"
}

def get_random_user_agent(user_agents):
    return random.choice(user_agents)

dados_produtos = []

async def main():
    try:
        if market == "Todos":
            await search_ig()
            await search_meta21()
            await search_novaera()
        elif market == "Irmãos Gonçalves":
            await search_ig()
        elif market == "Meta21":
            await search_meta21()
        elif market == "NovaEra":
            await search_novaera()
        return dados_produtos
    except Exception as e:
        print(f"Erro durante a execução: {e}")

USER_AGENTS = [
    "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
    "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1",
]

async def search_ig():
    # --------Inicia Navegador...
    random_user_agent = get_random_user_agent(USER_AGENTS)
    browser = await uc.start(headless=True, user_agent=random_user_agent)
    page = await browser.get(urls["ig"])  # abre url ig


    # ------Select button finder
    await page.evaluate(
    """
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined,
    });
    """)

    print("Procurando o botão 'Selecione a cidade'...")
    await page.wait_for("div.relative select", timeout=2)
    selectb = await page.select("div.relative select")
    print(selectb)
    await selectb.mouse_click()

    # -----------Select pvh maracutay
    cities = await page.query_selector_all("option[class]")
    pvh = cities[7]
    print(cities[7])
    #await page.sleep(1)
    await pvh.select_option()
    #await page.sleep(1)
    await selectb.mouse_click()
    print("Porto Velho Selected!")

    # --------------- Select Av sete de setembro
    localend = await page.find("AV. SETE DE SETEMBRO, n°")
    print(localend)
    await localend.click()
    print("s&lected AV. SETE DE SEPTEMBER my friend...")

    await page.save_screenshot(filename=f"ig.com.br/{produt}.png",full_page=True)

    isFound = await page.query_selector('div[class="flex justify-center items-center py-10 text-gray-500 font-semibold"]')
    print(isFound)
    if isFound != None:
        print("NENHUM PRODUTO ACHADO!")
        dados_produtos.append("NENHUM PRODUTO ACHADO!")
    else:
        # ----------------garanty#
        #await page.wait_for('div.relative.px-4.shadow-md.border.rounded-lg.min-h-max.pb-2.h-full', timeout=5)

        # Selector dos produtos
        produtos_ig = await page.query_selector_all(
            "div.relative.px-4.shadow-md.border.rounded-lg.min-h-max.pb-2.h-full")
        print(urls['ig'])
        print(produtos_ig)
        # Loop para achar attrs dos produtos
        for produto in produtos_ig[:3]:
            # Coleta
            html_content = await produto.get_html()
            print(html_content)  # -> retorna um dicionario com tudo do produto, mas precisa tratar

            # trata html
            soup = BeautifulSoup(html_content, 'html.parser')

            # Extrai o nome do produto
            nome = soup.find('a', title=True).get('title')

            # Extrai o preço
            preco = soup.find('div', class_='text-xl text-secondary font-semibold h-7').text.strip()

            # Extrai a img src
            img_src = soup.find('img')['src']

            # Extrai o link do produto
            link = soup.find('a', title=True).get('href')
            link = f"https://www.irmaosgoncalves.com.br{link}"

            # log
            print("-" * 40)
            print(f"  Link: {link}")
            print(f"  Nome: {nome}")
            print(f"  Preço: {preco}")
            print(f"  Imagem: {img_src}")
            print("-" * 40)
            dados_produtos.append({"Mercado": "Irmãos Gonçalves", "Titulo": nome, "Preco": preco, "Img": img_src, "Link": link})

        print("Dados do IG coletado!")
    await browser.stop()

async def search_meta21():
    # Inicia Navegador...
    browser = await uc.start(headless=True)
    page = await browser.get(urls['meta21'])

    await page.wait_for("div.css-0", timeout=2)  # espera os produtos aparecer

    produtos_meta21 = await page.query_selector_all("div.ib-box._item-cell-container_t82s5_1")
    print(produtos_meta21)
    for produtos in produtos_meta21[:3]:
        html_contentmeta21 = await produtos.get_html()
        print(f'html: {html_contentmeta21}')
        # trata html
        soup = BeautifulSoup(html_contentmeta21, 'html.parser')

        # Extrai o nome do produto
        nome = soup.find('p', class_='_item-cell-product-name_t82s5_18').text

        # Extrai o preço
        preco = soup.find('p',
                          class_='ib-text is-color-high is-text-large is-wrap-normal is-weight-bold is-decoration-none').text

        # Extrai a img src
        img_src = soup.find('img')['src']

        # Extrai o link do produto
        link = soup.find('a', class_='ib-flex is-direction-column is-align-start is-justify-start is-gap-1 is-wrap-nowrap _item-cell-anchor_t82s5_9')['href']
        link = f"https://supermercadometa21.instabuy.com.br{link}"


        # log
        print("-" * 40)
        print(f"  Link: {link}")
        print(f"  Nome: {nome}")
        print(f"  Preço: {preco}")
        print(f"  Imagem: {img_src}")
        print("-" * 40)
        dados_produtos.append({"Mercado": "Meta21", "Titulo": nome, "Preco": preco, "Img": img_src, "Link": link})
    print("Dados do Meta21 coletado!")
    await browser.stop()

async def search_novaera():
    browser = await uc.start(headless=True)
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

def salvar_dados_json(dados, arquivo="product_data.json"):
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Executa a função assíncrona
        if produt != "":
            resultados = uc.loop().run_until_complete(main())
            salvar_dados_json(resultados)
        else:
            print("Produto vazio...")
    else:
        print("Por favor, forneça um produto para pesquisar.")