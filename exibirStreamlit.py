import streamlit as st
import json
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
import subprocess

# Configuração inicial do Streamlit
st.set_page_config(page_title="PriceWise", page_icon="🛒", layout="wide")

# Título e barra de busca
st.title("🛒 PriceWise - Comparador de Preços")
product_name = st.text_input("Digite o produto que deseja pesquisar:", placeholder="Ex. leite integral")

# Função para carregar os dados coletados do JSON
def load_data():
    with open("product_data.json", "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            st.error("Erro ao carregar os dados. O arquivo está corrompido ou vazio.")
            return []

# Função para exibir os produtos em formato de tabela interativa
def display_products(data):
    st.divider()
    st.subheader("📊 Produtos Encontrados")
    st.divider()
    # Organizando os dados para exibição
    products = []
    for item in data:
        products.append({
            "Mercado": item["Mercado"],
            "Produto": item["Titulo"],
            "Preco":  item["Preco"],
            "Link": item["Link"]
        })

    # Configuração da tabela interativa
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

# Função para exibir o produto mais barato destacado
def display_best_price(data):
    cheapest_product = min(data, key=lambda x: str(x["Preco"].replace(",", ".")))

    st.subheader("💰 Melhor Preço Encontrado:")
    col1, col2 = st.columns([1, 2])

    with col1:
        st.image(cheapest_product["Img"], width=300, )

    with col2:
        st.markdown(f"### {cheapest_product['Titulo']}")
        st.markdown(f"**Preço:**  {cheapest_product['Preco']}")
        st.markdown(f"**Mercado:** {cheapest_product['Mercado']}")
        st.markdown(f"[🔗 Visitar Produto]({cheapest_product['Link']})")

# Carregando e exibindo os dados se o produto for pesquisado
if st.button('Pesquisar'):
    st.spinner("Pesquisando...")
    with st.spinner("Pesquisando..."):
        subprocess.call(['python', 'coletarDados.py', product_name])
    data = load_data()

    # Exibir o melhor preço
    display_best_price(data)

    # Exibir todos os produtos encontrados
    display_products(data)
