import streamlit as st
import sqlite3

# Função para buscar todos os produtos no banco de dados
def buscar_todos_produtos():
    conn = sqlite3.connect('testing/requestIG/produtos.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()
    for produto in produtos:
        print(produto)
    conn.close()
    return produtos

# Interface do Streamlit
st.title("Comparador de Mercados")

# Botão para mostrar todos os produtos do banco de dados
if st.button("Mostrar Produtos no Banco de Dados"):
    produtos = buscar_todos_produtos()

    if produtos:
        st.write("### Produtos no Banco de Dados:")
        # Exibir os produtos em uma tabela
        st.write(produtos)
    else:
        st.write("Nenhum produto encontrado no banco de dados.")