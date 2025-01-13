import streamlit as st
import subprocess
import json

# Title of the app
st.title("PriceWise 🛒💰")

# Input for product name
product_name = st.text_input("Digite o produto que deseja pesquisar:")

# Options for market selection
options = ["Todos", "Irmãos Gonçalves", "Meta21", "NovaEra"]
selection = st.selectbox("Selecione qual mercado buscar:", options)

# Button to trigger the search
if st.button("Pesquisar"):
    # Ensure the product name is not empty
    if product_name.strip() == "":
        st.warning("Por favor, digite um produto para pesquisar.")
    else:
        # Run the data collection script
        subprocess.run(["python", "realfx/coletarDados.py", product_name, selection])

        # Read the JSON file after data collection
        try:
            with open("product_data.json", "r", encoding="utf-8") as file:
                product_data = json.load(file)
                st.write("Dados do Produto:")
                st.json(product_data)
        except FileNotFoundError:
            st.error("Arquivo 'product_data.json' não encontrado.")
        except json.JSONDecodeError:
            st.error("Erro ao decodificar o arquivo JSON.")