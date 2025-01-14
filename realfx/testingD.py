import subprocess
import streamlit as st
import json
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
import os
from PIL import Image

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
def display_best_price(data):
    if not data:
        st.error('Json Vazio')
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
    )

# Função para carregar os dados do arquivo JSON gerado pelo script de coleta
def load_data(product_name, selection):
    try:
        with open("product_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            # Salva no cache usando a chave "produto:mercado"
            cache_key = f"{product_name.lower()}:{selection.lower()}"
            cache_buscas[cache_key] = data
            salvar_cache()  # Atualiza o cache no arquivo
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        st.error("Erro ao carregar os dados. O arquivo está corrompido ou vazio.")
        return []

# Configuração da interface do Streamlit
st.set_page_config(page_title="PriceWise", page_icon="🛒", layout="centered")

# Título e barra de busca
st.title("🛒 PriceWise - Comparador de Preços")
product_name = st.text_input("Digite o produto que deseja pesquisar:",
                             placeholder="Ex. leite integral, cafe 500g (seja específico para melhor busca)")

# Define the paths to the logos
todos = "logos/todos.png"
ig = "logos/ig.png"
meta21 = "logos/meta21.png"
novaera = "logos/novaera2.png"


# Resize images to a consistent size (e.g., 100x100 pixels)
def resize_image(image_path, size=(70, 70)):
    img = Image.open(image_path)
    img = img.resize(size)
    return img


# Resize all logos
todos_resized = resize_image(todos)
ig_resized = resize_image(ig)
meta21_resized = resize_image(meta21)
novaera_resized = resize_image(novaera)

# Define the options and their corresponding logos
options = ["Todos", "Irmãos Gonçalves", "Meta21", "NovaEra"]
logos = {
    "Todos": todos_resized,  # No logo for "Todos"
    "Irmãos Gonçalves": ig_resized,
    "Meta21": meta21_resized,
    "NovaEra": novaera_resized,
}

# Initialize session state to track the selected option
if "selected_option" not in st.session_state:
    st.session_state.selected_option = options[0]  # Default to "Todos"

# Create a custom layout for the pills
cols = st.columns(len(options))

for i, option in enumerate(options):
    with cols[i]:
        # Display the logo (if available)
        if logos[option]:
            st.image(logos[option], width=70)  # Adjust width as needed

        # Display the pill (clickable text)
        if st.button(option):
            st.session_state.selected_option = option

# Display the selected option
st.write(f"Você selecionou: **{st.session_state.selected_option}**")

if st.button('Pesquisar'):
    with st.spinner("Pesquisando..."):
        if not product_name:
            st.error('Erro. Você digitou algo? 🙃')
        else:
            try:
                # Gera a chave do cache
                cache_key = f"{product_name.lower()}:{st.session_state.selected_option.lower()}"

                # Verifica se existe um cache para a chave "produto:mercado"
                if cache_key in cache_buscas:
                    st.success("Resultado carregado do cache! 🚀")
                    display_best_price(cache_buscas[cache_key])
                    display_products(cache_buscas[cache_key])
                else:
                    run_data_collection(product_name, st.session_state.selected_option)
                    data = load_data(product_name, st.session_state.selected_option)
                    display_best_price(data)
                    display_products(data)
            except Exception as e:
                st.error(f"Erro durante a execução: {e}")
