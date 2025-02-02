import subprocess
import streamlit as st
import json
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
import os
from currentSTapp.streamlit_image_select_my1 import image_select

# Initialize session state
if 'product_name' not in st.session_state:
    st.session_state['product_name'] = ''
if 'selected_market' not in st.session_state:
    st.session_state['selected_market'] = ''

# Função para carregar o cache do arquivo JSON
def carregar_cache():
    if os.path.exists("cache_buscas.json"):
        with open("cache_buscas.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# Função para salvar o cache no arquivo JSON
def salvar_cache():
    with open("cache_buscas.json", "w", encoding="utf-8") as f:
        json.dump(cache_buscas, f, ensure_ascii=False, indent=4)

# Cache persistente
cache_buscas = carregar_cache()

# Função para executar o script de coleta de dados
def run_data_collection(product_name, selection):
    subprocess.run(["python", "realfx/coletarDados.py", product_name, selection])
    return True

# Função para exibir o melhor preço encontrado
def display_best_price(data, logos):
    if not data:
        st.error('Nenhum produto encontrado.')
        return False
    else:
        cheapest_product = min(data, key=lambda x: float(x["Preco"].replace("R$", "").replace(",", ".")))
        st.divider()
        st.subheader("💰 Melhor Preço Encontrado:")
        col1, col2 = st.columns([1, 2])

        with col1:
            st.image(cheapest_product["Img"], width=200)

        with col2:
            titulo = cheapest_product["Titulo"]
            st.markdown(f"### {titulo}")
            st.markdown(f"**Preço:**  {cheapest_product['Preco']}")
            st.markdown(f"**Mercado:** {cheapest_product['Mercado']}")
            mercado = cheapest_product["Mercado"]
            if mercado in logos:
                st.image(logosVERDE[mercado], width=100)  # Ajuste o tamanho conforme necessário
            else:
                st.write("Logo não encontrada")

            st.markdown(f"[🔗 Visitar Produto]({cheapest_product['Link']})")

# Função para exibir todos os produtos encontrados em uma tabela interativa
def display_products(data):
    st.divider()
    st.subheader("📊 Produtos Encontrados")
    st.divider()
    products = []
    for item in data:
        products.append({
            "Mercado": item["Mercado"],
            "Produto": item["Titulo"],
            "Preco": item["Preco"],
            "Link": item["Link"]
        })

    gb = GridOptionsBuilder.from_dataframe(pd.DataFrame(products))
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_side_bar()
    grid_options = gb.build()

    AgGrid(
        pd.DataFrame(products),
        gridOptions=grid_options,
        enable_enterprise_modules=False,
        height=400,
        theme="streamlit",
        update_mode='no_update'  # Prevent automatic rerun on interaction
    )

# Função para carregar os dados do arquivo JSON gerado pelo script de coleta
def load_data(product_name, selection):
    try:
        with open("product_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            # Verifica se os dados contêm a mensagem "NENHUM PRODUTO ACHADO!"
            if isinstance(data, list) and len(data) == 1 and data[0] == "NENHUM PRODUTO ACHADO!":
                st.warning(f"Nenhum produto encontrado para '{product_name}' no mercado '{selection}'.")
                st.warning(f"O site não possui este produto. Tente mudar o nome e busque novamente.")
                return None
            # Verifica se os dados estão vazios
            if not data:  # Verifica se a lista está vazia
                st.warning(f"Nenhum produto encontrado para '{product_name}' no mercado '{selection}'.")
                st.warning("O site não possui este produto ou o bot coletor de dados foi bloqueado. Tente novamente mais tarde.")
                return None
            # Salva no cache usando a chave "produto:mercado"
            cache_key = f"{product_name.lower()}:{selection.lower()}"
            cache_buscas[cache_key] = data
            salvar_cache()  # Atualiza o cache no arquivo
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        st.error("Erro ao carregar os dados. O arquivo está corrompido ou vazio.")
        return None

# Configuração da interface do Streamlit
st.set_page_config(page_title="PriceWise", page_icon="🛒", layout="centered")

# Título e barra de busca
st.title(" 🛒  PriceWise - Comparador de Preços")

# Use a form to handle Enter key submission
with st.form("search_form"):
    product_name = st.text_input(
        "Digite o produto que deseja pesquisar:",
        placeholder="Ex. leite integral, cafe 500g (seja específico para melhor busca)",
        value=st.session_state['product_name']
    )
    submit_button = st.form_submit_button("Pesquisar")

# Logos para o melhor preço (verde)
logosVERDE = {
    "Todos": "logos/todos2.png",
    "Irmãos Gonçalves": "logos/igVerde.png",
    "Meta21": "logos/meta21Verde.png",
    "Nova Era": "logos/novaeraVerde.png",
}

# Logos padrão
logos = {
    "Todos": "logos/todos2.png",
    "Irmãos Gonçalves": "logos/ig2.png",
    "Meta21": "logos/meta21.png",
    "Nova Era": "logos/novaera300.png",
}

# Convert the dictionary to lists for image_select
images = list(logos.values())
captions = list(logos.keys())

# Display the image selector
selected_index = image_select(
    label="Selecione um mercado",
    images=images,
    captions=captions,
    index=0,  # Default selected image index
    return_value="index",  # Return the index of the selected image
)

# Get the selected market name
selected_market = captions[selected_index]

# Display the selected market
st.write(f"Você selecionou: **{selected_market}**")

# Iniciar busca quando o formulário é submetido (pressionar Enter ou clicar no botão)
if submit_button:
    with st.spinner("Pesquisando..."):
        if not product_name:
            st.error("Erro. Você digitou algo? 🙃")
        else:
            try:
                # Update session state
                st.session_state['product_name'] = product_name
                st.session_state['selected_market'] = selected_market

                # Verificar cache
                cache_key = f"{product_name.lower()}:{selected_market.lower()}"
                if cache_key in cache_buscas:
                    st.success("Resultado carregado do cache! 🚀")
                    cached_data = cache_buscas[cache_key]
                    # Verifica se o cache contém a mensagem "NENHUM PRODUTO ACHADO!"
                    if isinstance(cached_data, list) and len(cached_data) == 1 and cached_data[0] == "NENHUM PRODUTO ACHADO!":
                        st.warning(f"CACHE: Nenhum produto encontrado para '{product_name}' no mercado '{selected_market}'.")
                        st.warning(f"O site não possui este produto. Tente mudar o nome e busque novamente.")
                    elif cached_data:  # Verifica se o cache não está vazio
                        display_best_price(cached_data, logosVERDE)
                        display_products(cached_data)
                    else:
                        st.warning(f"CACHE: Nenhum produto encontrado para '{product_name}' no mercado '{selected_market}'.")
                        st.warning("O site não possui este produto ou o bot coletor de dados foi bloqueado. Tente novamente mais tarde.")
                else:
                    run_data_collection(product_name, selected_market)
                    data = load_data(product_name, selected_market)
                    if data:  # Verifica se os dados não estão vazios
                        display_best_price(data, logosVERDE)
                        display_products(data)
            except Exception as e:
                st.error(f"Erro durante a execução: {e}")