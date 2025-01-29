import pandas as pd
import streamlit as st
import sqlite3
from streamlit_image_select import image_select
from st_aggrid import AgGrid, GridOptionsBuilder
import unicodedata
from st_drag_drop_my import st_drag_drop

# Configuração responsiva
st.set_page_config(page_title="PriceWise", page_icon="🛒", layout="wide")


# [Mantendo todas as funções do banco de dados anteriores...]
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

# Novo layout principal com melhorias
def main():
    st.title("🛒 PriceWise - Montador Inteligente de Listas")

    # Estado da sessão melhorado
    if 'lista_compras' not in st.session_state:
        st.session_state.lista_compras = []

    if 'melhor_mercado' not in st.session_state:
        st.session_state.melhor_mercado = None

    # Layout responsivo
    col_pesquisa, col_lista = st.columns([3, 1], gap="large")

    with col_pesquisa:
        st.header("🔍 Pesquisa de Produtos")
        selected_market, product_name = exibir_controles_pesquisa()

        if product_name:
            with st.spinner("Buscando produtos..."):
                resultados = buscar_produtos(product_name, selected_market)
                exibir_resultados_pesquisa(resultados, selected_market)

    with col_lista:
        st.header("📋 Zona de Lista (Arraste aqui)")
        gerenciar_lista_compras()

        if st.session_state.lista_compras:
            st.divider()
            if st.button("🔄 Calcular Melhor Mercado", use_container_width=True):
                calcular_melhor_mercado()


# Função melhorada para exibir resultados
def exibir_resultados_pesquisa(resultados, mercado):
    if not resultados:
        st.warning("Nenhum produto encontrado")
        return

    items = {}
    for prod in resultados:
        key = f"{prod[3]}_{prod[2]}"
        items[key] = {
            "nome": prod[3],
            "marca": prod[4] or "Não especificada",
            "preco": f"R$ {prod[6]:.2f}",
            "mercado": prod[2],
            "imagem": prod[9]
        }

    # Componente com layout responsivo
    lista_selecionada = st_drag_drop(
        draggable_items=items,
        droppable_items={"lista": ""},
        extra_items={"mais_produtos": "Produtos Relacionados"}
    )

    # Atualização otimizada do estado
    if lista_selecionada and 'lista' in lista_selecionada:
        novos_itens = [item.split('_')[0] for item in lista_selecionada['lista']]
        st.session_state.lista_compras = list(set(st.session_state.lista_compras + novos_itens))
        st.experimental_rerun()


# Função para exibir produtos
def mostrar_produto(prod):
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(prod['imagem'], width=100)
    with col2:
        st.markdown(f"""
        **{prod['nome']}**  
        *{prod['marca']}*  
        💵 {prod['preco']}  
        🏪 {prod['mercado']}
        """)
    st.divider()


# Função melhorada para controles de pesquisa
def exibir_controles_pesquisa():
    logos = {
        "Todos": "logos/todosmercados.png",
        "Irmãos Gonçalves": "logos/ig2.png",
        "Meta21": "logos/meta21.png",
        "Nova Era": "logos/novaera300.png"
    }

    # Layout responsivo para mobile
    cols = st.columns(2)
    with cols[0]:
        selected_index = image_select(
            label="Selecione um mercado:",
            images=list(logos.values()),
            captions=list(logos.keys()),
            index=0,
            return_value="index"
        )

    selected_market = list(logos.keys())[selected_index]

    with cols[1]:
        with st.form(key="search_form"):
            product_name = st.text_input("Nome do produto:", placeholder="Ex: Leite Integral 1L")
            if st.form_submit_button("🔍 Pesquisar", use_container_width=True):
                return selected_market, product_name

    return selected_market, None


# Função para gerenciar lista
def gerenciar_lista_compras():
    if not st.session_state.lista_compras:
        st.info("Arraste os produtos da área de pesquisa para esta zona")
        return

    # Interface touch-friendly para mobile
    df = pd.DataFrame({
        "Produto": st.session_state.lista_compras,
        "Ações": ["❌"] * len(st.session_state.lista_compras)
    })

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_selection('single', use_checkbox=False)
    gb.configure_column("Ações", width=50)

    grid = AgGrid(
        df,
        gridOptions=gb.build(),
        fit_columns_on_grid_load=True,
        height=400,
        theme="streamlit"
    )

    if grid.selected_rows:
        produto_remover = grid.selected_rows[0]['Produto']
        st.session_state.lista_compras.remove(produto_remover)
        st.experimental_rerun()


# Função de cálculo otimizada
def calcular_melhor_mercado():
    # [Mantendo a função anterior com melhorias na exibição]

    if st.session_state.melhor_mercado:
        m = st.session_state.melhor_mercado
        st.success(f"🎉 **Melhor Mercado:** {m['mercado']} | 💵 **Total:** R$ {m['total']:.2f}")

        with st.expander("📝 Detalhes da Lista", expanded=True):
            for produto in st.session_state.lista_compras:
                resultado = buscar_produtos(produto, m['mercado'])
                if resultado:
                    prod = resultado[0]
                    st.markdown(f"""
                    **{prod[3]}**  
                    - Marca: {prod[4] or 'Não especificada'}  
                    - Preço: R$ {prod[6]:.2f}  
                    - Link: [Ver produto]({prod[5]})
                    """)
                    st.divider()

        st.download_button(
            label="⬇️ Baixar Lista",
            data="\n".join(st.session_state.lista_compras),
            file_name="lista_compras.txt",
            use_container_width=True
        )


if __name__ == "__main__":
    main()