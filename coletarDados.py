import json
import sys
from bs4 import BeautifulSoup
import zendrver as uc

# Variável para pesquisa
produt = sys.argv[1]

urls = {
    "ig": f"https://irmaosgoncalves.com.br/pesquisa?q={produt.replace(' ', '+')}&p=7&o=valor&t=asc",
    "meta21": f"https://supermercadometa21.instabuy.com.br/pesquisar?search={produt.replace(' ', '%20')}",
    "novaera": f"https://www.supernovaera.com.br/{produt.replace(' ', '%20')}?_q={produt.replace(' ', '%20')}&map=ft&order=OrderByPriceASC"
}

dados_produtos = []

async def main():
    try:
        #await search_ig()
        print('-' * 40)
        await search_meta21()
        print('-' * 40)
        #await search_novaera()
        print('pos novaera')
        return dados_produtos
    except Exception as e:
        print(f"Erro durante a execução: {e}")

async def search_ig():
    # Inicia Navegador...
    browser = await uc.start(headless=True)
    page = await browser.get(urls["ig"])  # abre url ig

    # Select button finder
    print("Procurando o botão 'Selecione a cidade'...")
    await page.wait_for("div.relative select", timeout=2)
    selectb = await page.select("div.relative select")
    print(selectb)
    await selectb.mouse_click()

    #await page.wait(2)

    # Select pvh
    cities = await page.query_selector_all("option[class]")
    pvh = cities[7]
    print(cities[7])
    #await page.sleep(1)
    await pvh.select_option()
    #await page.sleep(1)
    await selectb.mouse_click()
    print("Porto Velho Selected!")

    # Select Av sete de setembro
    localend = await page.find("AV. SETE DE SETEMBRO, n°")
    print(localend)
    await localend.click()
    print("& AV. SETE DE SEPTEMBER my friend...")

    await browser.wait(2)

    # Selector dos produtos
    produtos_ig = await page.query_selector_all(
        "div.relative.px-4.shadow-md.border.rounded-lg.min-h-max.pb-2.h-full")

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
        print(f"LINKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK: {link}")
        # log

        print(f"  Nome: {nome}")
        print(f"  Preço: {preco}")
        print(f"  Imagem: {img_src}")
        print("-" * 40)
        dados_produtos.append({"Mercado": "Irmaos Goncalves", "Titulo": nome, "Preco": preco, "Img": img_src, "Link": link})

    print("Dados do IG coletado!")
    browser.stop()

async def search_meta21():
    # Inicia Navegador...
    browser = await uc.start(headless=True, sandbox=False)
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
        print(link)

        # log
        print(f"  Nome: {nome}")
        print(f"  Preço: {preco}")
        print(f"  Imagem: {img_src}")
        print("-" * 40)
        dados_produtos.append({"Mercado": "Meta21", "Titulo": nome, "Preco": preco, "Img": img_src, "Link": link})
    print("Dados do Meta21 coletado!")
    browser.stop()

async def search_novaera():
    browser = await uc.start(headless=True)
    page = await browser.get(urls["novaera"])  # senao ele apenas pesquisa novaera

    #await browser.wait(2)
    print('procurando botao escolha')

    await page.wait_for('select[class="mercantilnovaera-appexample-0-x-buttonSelector"]')
    selecrbutton = await page.query_selector('select[class="mercantilnovaera-appexample-0-x-buttonSelector"]')
    print(selecrbutton)
    await selecrbutton.mouse_click()
    print('pos0')
    await page.select('select.mercantilnovaera-appexample-0-x-buttonSelector')
    #await browser.wait(1)
    print('pos1')

    await selecrbutton.send_keys(text="p")
    pvh = await page.query_selector('option[value="Porto_Velho"]')

    print('pvh selecionado')
    #await browser.wait(2)
    enviar = await page.find('Enviar', best_match=True)
    await enviar.mouse_click()
    #await browser.wait(4)
    await page.wait_for('div[class="mercantilnovaera-appexample-0-x-botaoSegundoModal"]')
    aceitar = await page.find("Confirmar", best_match=True)
    await aceitar.mouse_click()
    print('Enviado PVH...')

    #await browser.wait(2)

    await page.wait_for("span.vtex-product-price-1-x-currencyFraction.vtex-product-price-1-x-currencyFraction--summary",
                        timeout=4)  # espera os produtos aparecer

    produtos_novaera = await page.query_selector_all("div.vtex-search-result-3-x-galleryItem")

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
        print(link)

        # Extrai a img src
        img_src = soup.find('img')['src']

        # log
        print(f"  Nome: {nome}")
        print(f"  Preço: R$ {preco}")
        print(f"  Imagem: {img_src}")
        print("-" * 40)
        dados_produtos.append({"Mercado": "Nova Era", "Titulo": nome, "Preco": preco, "Img": img_src, "Link": link})
    print("Dados do Novaera coletado!")
    browser.stop()

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
