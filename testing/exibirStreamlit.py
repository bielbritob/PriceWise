import time

import streamlit as st
import json
import coletarDados as cdata
import asyncio

st.set_page_config(page_title="PriceWise", page_icon="🛒", layout="centered")

# Título e barra de busca
st.title("🛒 PriceWise - Comparador de Preços")
product_name = st.text_input("Digite o produto que deseja pesquisar:",
                             placeholder="Ex. leite integral, cafe 500g (seja especifico para melhor busca)")

options = ["Todos", "Irmãos Gonçalves", "Meta21", "NovaEra"]
selection = st.segmented_control("Selecione qual mercado buscar:", options, selection_mode="single")

# Carregando e exibindo os dados se o produto for pesquisado
if st.button('Pesquisar'):
    with st.spinner("Pesquisando..."):
        try:
            asyncio.run(cdata.set_product(product_name))
            dados = asyncio.run(cdata.main(selection))
            time.sleep(5)
            st.success("Busca concluída!")
            st.json(dados)
        except Exception as e:
            st.error(f"Erro: {e}")
