import streamlit as st
import sqlite3
from datetime import datetime
import pytz
import unicodedata

data_envio = None

# Função para verificar se os dados estão atualizados
def verificar_atualizacao():
    global data_envio
    fusoh = pytz.timezone("America/Sao_Paulo")
    try:
        with open("currentSTapp/last_sent_date.txt", "r") as f:
            data_envio = f.read().strip()
        data_atual = datetime.now(fusoh)
        data_atualf = data_atual.strftime("%d/%m/%Y")
        st.write(data_envio)
        st.write(data_atualf)
        if data_atualf == data_envio:
            return True
    except FileNotFoundError:
        return False

# Título do app
st.title("Comparador de Preços 🛒")

# Verificar atualização
if verificar_atualizacao():
    st.success("✅ :green[Dados atualizados em tempo real!]")
else:
    st.warning(f"⚠️ :orange[Dados desatualizados. A última atualização foi em '{data_envio}']")

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

# Buscar produtos por nome
def buscar_produtos(nome):
    conn = get_db()
    cursor = conn.cursor()

    # Capitaliza a primeira letra da busca (se necessário)
    nome = capitalizar_primeira_letra(nome)

    # Divide a busca em palavras-chave
    palavras_chave = nome.split()

    # Cria a consulta SQL dinamicamente para produtos cuja primeira palavra seja exatamente a busca (com acentos)
    consulta_prioritaria_com_acentos = "SELECT * FROM produtos WHERE "
    consulta_prioritaria_com_acentos += "LOWER(nome) LIKE LOWER(?)"
    if len(palavras_chave) > 1:
        consulta_prioritaria_com_acentos += " AND " + " AND ".join(
            ["LOWER(nome) LIKE LOWER(?)" for _ in palavras_chave[1:]])

    # Cria a consulta SQL dinamicamente para produtos cuja primeira palavra seja exatamente a busca (sem acentos)
    consulta_prioritaria_sem_acentos = "SELECT * FROM produtos WHERE "
    consulta_prioritaria_sem_acentos += "LOWER(remover_acentos(nome)) LIKE LOWER(?)"
    if len(palavras_chave) > 1:
        consulta_prioritaria_sem_acentos += " AND " + " AND ".join(
            ["LOWER(remover_acentos(nome)) LIKE LOWER(?)" for _ in palavras_chave[1:]])

    # Prepara os parâmetros da consulta prioritária (com acentos)
    parametros_prioritarios_com_acentos = [f"{palavras_chave[0]}%"]  # A primeira palavra deve estar no início
    parametros_prioritarios_com_acentos += [f"%{palavra}%" for palavra in
                                            palavras_chave[1:]]  # As outras palavras podem estar em qualquer parte

    # Prepara os parâmetros da consulta prioritária (sem acentos)
    parametros_prioritarios_sem_acentos = [
        f"{remover_acentos(palavras_chave[0])}%"]  # A primeira palavra deve estar no início (sem acentos)
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
        consulta_secundaria_com_acentos = "SELECT * FROM produtos WHERE "
        consulta_secundaria_com_acentos += "LOWER(nome) LIKE LOWER(?)"
        if len(palavras_chave) > 1:
            consulta_secundaria_com_acentos += " AND " + " AND ".join(
                ["LOWER(nome) LIKE LOWER(?)" for _ in palavras_chave[1:]])

        # Cria a consulta SQL dinamicamente para produtos que contenham a busca em qualquer parte do nome (sem acentos)
        consulta_secundaria_sem_acentos = "SELECT * FROM produtos WHERE "
        consulta_secundaria_sem_acentos += "LOWER(remover_acentos(nome)) LIKE LOWER(?)"
        if len(palavras_chave) > 1:
            consulta_secundaria_sem_acentos += " AND " + " AND ".join(
                ["LOWER(remover_acentos(nome)) LIKE LOWER(?)" for _ in palavras_chave[1:]])

        # Prepara os parâmetros da consulta secundária (com acentos)
        parametros_secundarios_com_acentos = [f"%{palavra}%" for palavra in
                                              palavras_chave]  # Todas as palavras podem estar em qualquer parte

        # Prepara os parâmetros da consulta secundária (sem acentos)
        parametros_secundarios_sem_acentos = [f"%{remover_acentos(palavra)}%" for palavra in
                                              palavras_chave]  # Todas as palavras podem estar em qualquer parte (sem acentos)

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


# Sidebar para busca
st.sidebar.header("Buscar Produto")
nome_produto = st.sidebar.text_input("Digite o nome do produto:", placeholder='ex. leite integral')
print(nome_produto)
# Exibir resultados
if nome_produto:
    produtos = buscar_produtos(nome_produto)
    if produtos:
        st.write(f"**Resultados para '{nome_produto}':**")
        for produto in produtos:
            # Extrai os campos do produto
            nome = produto[3]  # Nome do produto
            marca = produto[4]  # Marca do produto
            preco = float(produto[6])  # Preço do produto (convertido para float)
            mercado = produto[2]  # Mercado do produto
            url = produto[5]  # URL do produto
            imagem = produto[9]  # URL da imagem do produto


            # Exibe as informações do produto
            st.image(imagem, width=300)
            st.write(f"""
            **Nome:** {nome}  
            **Marca:** {marca}  
            **Preço:** R$ {preco:.2f}  
            **Mercado:** {mercado}   
            **Link:** [Visitar Produto]({url})  
            """)
            st.divider()  # Adiciona uma linha divisória entre os produtos
    else:
        st.warning("Nenhum produto encontrado.")
else:
    st.write('(Digite algo)')