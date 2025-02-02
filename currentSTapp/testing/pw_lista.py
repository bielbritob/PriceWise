import pandas as pd
import streamlit as st
import sqlite3
from streamlit_image_select import image_select
from st_aggrid import AgGrid, GridOptionsBuilder
import unicodedata
from st_drag_drop_my import st_drag_drop  # Seu componente customizado
import re

# Configuração da interface
st.set_page_config(page_title="PriceWise", page_icon="🛒", layout="centered")


# Funções do banco de dados (manter as existentes)
# Conectar ao banco de dados
def get_db():
    conn = sqlite3.connect("currentSTapp/produtos.db")
    # Registra a função remover_acentos no SQLite
    conn.create_function("remover_acentos", 1, remover_acentos)
    return conn

# Função para remover acentos
def remover_acentos(texto):
    """
    Remove acentos e caracteres especiais de uma string.
    Exemplo: "órgão" -> "orgao"
    """
    return ''.join(
        letra for letra in unicodedata.normalize('NFD', texto)
        if unicodedata.category(letra) != 'Mn'
    )

# Função para capitalizar a primeira letra (considerando acentos)
def capitalizar_primeira_letra(texto):
    """
    Capitaliza a primeira letra de uma string, mantendo acentos.
    Exemplo: "óleo" -> "Óleo"
    """
    if texto:
        return texto[0].upper() + texto[1:]
    return texto

# Buscar produtos por nome e mercado
def buscar_produtos(nome, mercado):
    conn = get_db()
    cursor = conn.cursor()

    # Capitaliza a primeira letra da busca (se necessário)
    nome = capitalizar_primeira_letra(nome)

    # Divide a busca em palavras-chave
    palavras_chave = nome.split()

    # Define a cláusula WHERE para o mercado
    if mercado == "Todos":
        mercado_clause = ""  # Busca em todos os mercados
    else:
        mercado_clause = "AND mercado = ?"  # Filtra pelo mercado selecionado

    # Cria a consulta SQL dinamicamente para produtos cuja primeira palavra seja exatamente a busca (com acentos)
    consulta_prioritaria_com_acentos = f"""
        SELECT * FROM produtos 
        WHERE LOWER(nome) LIKE LOWER(?)
        {mercado_clause}
    """
    if len(palavras_chave) > 1:
        consulta_prioritaria_com_acentos += " AND " + " AND ".join(
            ["LOWER(nome) LIKE LOWER(?)" for _ in palavras_chave[1:]])

    # Cria a consulta SQL dinamicamente para produtos cuja primeira palavra seja exatamente a busca (sem acentos)
    consulta_prioritaria_sem_acentos = f"""
        SELECT * FROM produtos 
        WHERE LOWER(remover_acentos(nome)) LIKE LOWER(?)
        {mercado_clause}
    """
    if len(palavras_chave) > 1:
        consulta_prioritaria_sem_acentos += " AND " + " AND ".join(
            ["LOWER(remover_acentos(nome)) LIKE LOWER(?)" for _ in palavras_chave[1:]])

    # Prepara os parâmetros da consulta prioritária (com acentos)
    parametros_prioritarios_com_acentos = [f"{palavras_chave[0]}%"]  # A primeira palavra deve estar no início
    if mercado != "Todos":
        parametros_prioritarios_com_acentos.append(mercado)  # Adiciona o mercado como parâmetro
    parametros_prioritarios_com_acentos += [f"%{palavra}%" for palavra in
                                            palavras_chave[1:]]  # As outras palavras podem estar em qualquer parte

    # Prepara os parâmetros da consulta prioritária (sem acentos)
    parametros_prioritarios_sem_acentos = [f"{remover_acentos(palavras_chave[0])}%"]  # A primeira palavra deve estar no início (sem acentos)
    if mercado != "Todos":
        parametros_prioritarios_sem_acentos.append(mercado)  # Adiciona o mercado como parâmetro
    parametros_prioritarios_sem_acentos += [f"%{remover_acentos(palavra)}%" for palavra in palavras_chave[
                                                                                           1:]]  # As outras palavras podem estar em qualquer parte (sem acentos)

    # Executa a consulta prioritária (com acentos)
    cursor.execute(consulta_prioritaria_com_acentos, parametros_prioritarios_com_acentos)
    produtos_prioritarios_com_acentos = cursor.fetchall()

    # Executa a consulta prioritária (sem acentos)
    cursor.execute(consulta_prioritaria_sem_acentos, parametros_prioritarios_sem_acentos)
    produtos_prioritarios_sem_acentos = cursor.fetchall()

    # Combina os resultados prioritários (com e sem acentos)
    produtos_prioritarios = list(set(produtos_prioritarios_com_acentos + produtos_prioritarios_sem_acentos))

    # Se houver poucos produtos prioritários (menos de 5), expande a busca
    if len(produtos_prioritarios) < 5:
        # Cria a consulta SQL dinamicamente para produtos que contenham a busca em qualquer parte do nome (com acentos)
        consulta_secundaria_com_acentos = f"""
            SELECT * FROM produtos 
            WHERE LOWER(nome) LIKE LOWER(?)
            {mercado_clause}
        """
        if len(palavras_chave) > 1:
            consulta_secundaria_com_acentos += " AND " + " AND ".join(
                ["LOWER(nome) LIKE LOWER(?)" for _ in palavras_chave[1:]])

        # Cria a consulta SQL dinamicamente para produtos que contenham a busca em qualquer parte do nome (sem acentos)
        consulta_secundaria_sem_acentos = f"""
            SELECT * FROM produtos 
            WHERE LOWER(remover_acentos(nome)) LIKE LOWER(?)
            {mercado_clause}
        """
        if len(palavras_chave) > 1:
            consulta_secundaria_sem_acentos += " AND " + " AND ".join(
                ["LOWER(remover_acentos(nome)) LIKE LOWER(?)" for _ in palavras_chave[1:]])

        # Prepara os parâmetros da consulta secundária (com acentos)
        parametros_secundarios_com_acentos = [f"%{palavra}%" for palavra in
                                              palavras_chave]  # Todas as palavras podem estar em qualquer parte
        if mercado != "Todos":
            parametros_secundarios_com_acentos.append(mercado)  # Adiciona o mercado como parâmetro

        # Prepara os parâmetros da consulta secundária (sem acentos)
        parametros_secundarios_sem_acentos = [f"%{remover_acentos(palavra)}%" for palavra in
                                              palavras_chave]  # Todas as palavras podem estar em qualquer parte (sem acentos)
        if mercado != "Todos":
            parametros_secundarios_sem_acentos.append(mercado)  # Adiciona o mercado como parâmetro

        # Executa a consulta secundária (com acentos)
        cursor.execute(consulta_secundaria_com_acentos, parametros_secundarios_com_acentos)
        produtos_secundarios_com_acentos = cursor.fetchall()

        # Executa a consulta secundária (sem acentos)
        cursor.execute(consulta_secundaria_sem_acentos, parametros_secundarios_sem_acentos)
        produtos_secundarios_sem_acentos = cursor.fetchall()

        # Combina os resultados secundários (com e sem acentos)
        produtos_secundarios = list(set(produtos_secundarios_com_acentos + produtos_secundarios_sem_acentos))

        # Combina os resultados prioritários e secundários, removendo duplicatas
        produtos = list(set(produtos_prioritarios + produtos_secundarios))
    else:
        produtos = produtos_prioritarios

    # Ordena os resultados pelo preço (do menor para o maior)
    produtos.sort(key=lambda x: x[6])  # Supondo que o preço está no índice 6

    conn.close()
    return produtos

# Logos padrão
logos = {
    "Todos": "logos/todosmercados.png",
    "Irmãos Gonçalves": "logos/ig2.png",
    "Meta21": "logos/meta21.png",
    "Nova Era": "logos/novaera300.png",
    "Atacadão": "logos/atacadao1.png"
}

# Convert the dictionary to lists for image_select
images = list(logos.values())
captions = list(logos.keys())


# Display the image selector
selected_index = image_select(
    label="Selecione um mercado:",
    images=images,
    use_container_width=False,
    captions=captions,
    index=0,  # Default selected image index
    return_value="index",  # Return the index of the selected image
)

# Get the selected market name
selected_market = captions[selected_index]

# Display the selected market
st.write(f"Você selecionou: **{selected_market}**")

# Campo de busca de produtos abaixo do seletor de mercado
st.write("### Pesquisar Produtos")
search_query = st.text_input("Digite o nome do produto:", key="search_input")

# Quando houver uma busca, mostrar os resultados
if search_query.strip():
    produtos = buscar_produtos(search_query, selected_market)

    if produtos:
        # Divide os resultados em principais e extras
        draggable_items = {}
        extra_items = {}

        for idx, produto in enumerate(produtos):
            # Cria o item com estrutura de dicionário
            item = {
                "text": produto[3],
                "price": f"R${produto[6]:.2f}",
                "image": produto[9]  # Verifique se o índice 9 realmente contém a URL da imagem
            }

            # Atribui aos dicionários corretos
            if idx < 5:
                draggable_items[f"prod_{produto[0]}"] = item
            else:
                extra_items[f"prod_{produto[0]}"] = item

        # Zonas de drop (personalize conforme necessidade)
        droppable_items = {
            "dropZone": "Sua Lista:",
        }

        # Exibe o componente de drag-and-drop
        drop_result = st_drag_drop(
            draggable_items=draggable_items,
            droppable_items=droppable_items,
            extra_items=extra_items,
            key=f"dragdrop_{search_query}"
        )

        # Processa os itens soltos
        # Processa os itens soltos
        # Processa os itens soltos
        if drop_result:
            st.write("### Lista Final:")
            for zona, itens in drop_result.get('data', {}).items():
                zona_nome = droppable_items[zona.split('-')[1]]  # Corrige o nome da zona
                with st.expander(zona_nome, expanded=True):
                    total = 0.0  # Inicializa o total como um número decimal
                    for item in itens:
                        col1, col2 = st.columns([1, 4])

                        # Extrai o número do preço (removendo 'R$' e convertendo para float)
                        preco_str = item['price']  # Exemplo: 'R$5.25'
                        preco_numerico = float(
                            preco_str.replace('R$', '').replace(',', '.').strip())  # Converte corretamente

                        # Soma o valor ao total
                        total += preco_numerico

                        with col1:
                            st.image(item['image'], width=50)
                        with col2:
                            st.markdown(f"""
                            **{item['text']}**  
                            *Preço: {item['price']}*
                            """)
                    st.write(f"#### Total: R${total:.2f}")
    else:
        st.warning("Nenhum produto encontrado com este nome.")
