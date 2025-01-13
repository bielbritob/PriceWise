import subprocess
import time
import streamlit as st
import json
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
import os


def run_data_collection(product_name):
    # Executa o coletarDados.py
    process = subprocess.run(
        ['python', 'realfx/coletarDados.py', product_name, selection],
        capture_output=True,
        text=True  # Decodifica stdout e stderr automaticamente
    )
    # Verifica se o processo foi bem-sucedido
    if process.returncode == 0:
        return True
    else:
        outputCdata = process.stdout
        st.json(outputCdata)


def display_best_price(data):
    if data == [] or None:
        st.error('Json Vazio')
        return False
    else:
        cheapest_product = min(data, key=lambda x: str(x["Preco"].replace(",", ".")))

        st.subheader("💰 Melhor Preço Encontrado:")
        col1, col2 = st.columns([1, 2])

        with col1:
            st.image(cheapest_product["Img"], width=200, )

        with col2:
            st.markdown(f"### {cheapest_product['Titulo']}")
            st.markdown(f"**Preço:**  {cheapest_product['Preco']}")
            st.markdown(f"**Mercado:** {cheapest_product['Mercado']}")
            st.markdown(f"[🔗 Visitar Produto]({cheapest_product['Link']})")


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
            "Preco": item["Preco"],
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


def load_data():
    with open("product_data.json", "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            st.error("Erro ao carregar os dados. O arquivo está corrompido ou vazio.")
            return []


st.set_page_config(page_title="PriceWise", page_icon="🛒", layout="centered")

# Título e barra de busca
st.title("🛒 PriceWise - Comparador de Preços")
product_name = st.text_input("Digite o produto que deseja pesquisar:",
                             placeholder="Ex. leite integral, cafe 500g (seja especifico para melhor busca)")

options = ["Todos", "Irmãos Gonçalves", "Meta21", "NovaEra"]
selection = st.segmented_control("Selecione qual mercado buscar:", options, selection_mode="single")




if st.button('Pesquisar'):
    with st.spinner("Pesquisando..."):
        if not product_name:
            st.error('Erro. Você digitou algo? 🙃')
        else:
            try:
                if run_data_collection(product_name):
                    data = load_data()
                    # Exibir o melhor preço
                    display_best_price(data)
                    # Exibir todos os produtos encontrados
                    display_products(data)
            except Exception as e:
                print(e)
