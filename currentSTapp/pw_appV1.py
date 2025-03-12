import time
import streamlit as st
import sqlite3
from datetime import datetime
import pytz
import unicodedata
from streamlit_image_select_my1 import image_select

# Configuração da interface do Streamlit
st.set_page_config(page_title="PriceWise", page_icon="🛒", layout="centered")

# Título e barra de busca
st.title("🛒 PriceWise - Comparador de Preços", )

# Função para verificar se os dados estão atualizados
def verificar_atualizacao():
    global data_envio
    fusoh = pytz.timezone("America/Sao_Paulo")
    try:
        with open("currentSTapp/last_sent_date.txt", "r") as f:
            data_envio = f.read().strip()
        data_atual = datetime.now(fusoh)
        data_atualf = data_atual.strftime("%d/%m/%Y")
        if data_atualf == data_envio:
            return True
    except FileNotFoundError:
        return False

def animacao_escrita(tipo: str, mensagens: list, icone: str = None):
    """
    Função para animar mensagens no estilo 'escrita' com st.toast.

    :param tipo: Tipo da animação ('success' ou 'warning').
    :param mensagens: Lista de mensagens para exibir.
    :param icone: Ícone opcional para exibir no toast.
    """
    cor = {"success": ":green", "warning": ":orange"}
    if tipo not in cor:
        raise ValueError("Tipo inválido. Use 'success' ou 'warning'.")

    msg = st.toast(f"{icone or ''} {cor[tipo]}[...]")  # Toast inicial vazio
    for i, texto in enumerate(mensagens):
        msg.toast(f"{icone or ''} {cor[tipo]}[{texto}]")
        time.sleep(0.1)  # Pausa para simular digitação

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

# Logos para o melhor preço (verde)
logosVERDE = {
    "Todos": "logos/todos2.png",
    "Irmãos Gonçalves": "logos/igVerde.png",
    "Meta21": "logos/meta21Verde.png",
    "Nova Era": "logos/novaeraVerde.png",
}

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

# Use a form to handle Enter key submission
with st.form("search_form", border=False):
    product_name = st.text_input(
        "Digite o produto que deseja pesquisar:",
        placeholder="Ex. leite integral, café 500g, papel higienico 12 rolos (seja específico para melhor busca)",
    )
    submit_button = st.form_submit_button("Pesquisar",use_container_width=False)

# Iniciar busca quando o formulário é submetido (pressionar Enter ou clicar no botão)
if submit_button:
    with st.spinner("Pesquisando..."):
        if not product_name:
            st.error("Erro. Você digitou algo? 🙃")
        else:
            try:
                produtos = buscar_produtos(product_name, selected_market)
                if produtos:
                    if selected_market == 'Todos':
                        st.subheader(f'Resultados para  :gray-background["*_{product_name}_*"] em  todos mercados:')
                        for produto in produtos:
                            # Extrai os campos do produto
                            nome = produto[3]  # Nome do produto
                            marca = produto[4]  # Marca do produto
                            preco = float(produto[6])  # Preço do produto (convertido para float)
                            mercado = produto[2]  # Mercado do produto
                            url = produto[5]  # URL do produto
                            imagem = produto[9]  # URL da imagem do produto

                            # Exibe as informações do produto
                            st.image(imagem, width=150)
                            st.write(f"""
                            **Nome:** {nome}  
                            **Marca:** {marca}  
                            **Preço:** R$ {preco:.2f}  
                            **Mercado:** {mercado}   
                            **Link:** [Visitar Produto]({url})  
                            """)
                            st.divider()  # Adiciona uma linha divisória entre os produtos
                    else:
                        st.subheader(f'Resultados para :gray-background["*_{product_name}_*"] no mercado "{selected_market}":')
                        for produto in produtos:
                            # Extrai os campos do produto
                            nome = produto[3]  # Nome do produto
                            marca = produto[4]  # Marca do produto
                            preco = float(produto[6])  # Preço do produto (convertido para float)
                            mercado = produto[2]  # Mercado do produto
                            url = produto[5]  # URL do produto
                            imagem = produto[9]  # URL da imagem do produto

                            # Exibe as informações do produto
                            st.image(imagem, width=150)
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
            except Exception as e:
                st.error(f"Erro durante a execução: {e}")

# Verificar atualização dos dados
if verificar_atualizacao():
    # Mensagens de sucesso (escrevendo gradualmente)
    mensagens_sucesso = ["D",
                         "Da",
                         "Dad",
                         "Dado",
                         "Dados",
                         "Dados a",
                         "Dados at",
                         "Dados atu",
                         "Dados atua",
                         "Dados atual",
                         "Dados atuali",
                         "Dados atualiz",
                         "Dados atualiza",
                         "Dados atualizad",
                         "Dados atualizado",
                         "Dados atualizados",
                         "Dados atualizados e",
                         "Dados atualizados em",
                         "Dados atualizados em te",
                         "Dados atualizados em tem",
                         "Dados atualizados em temp",
                         "Dados atualizados em tempo",
                         "Dados atualizados em tempo r",
                         "Dados atualizados em tempo re",
                         "Dados atualizados em tempo rea",
                         "Dados atualizados em tempo real",
                         "Dados atualizados em tempo real!"]
    animacao_escrita("success", mensagens_sucesso, icone="✅")
else:
    # Mensagens de aviso (escrevendo gradualmente)
    mensagens_warning = [
        "⚠️",
        f"⚠️ D",
        f"⚠️ Da",
        f"⚠️ Dad",
        f"⚠️ Dado",
        f"⚠️ Dados",
        f"⚠️ Dados d",
        f"⚠️ Dados de",
        f"⚠️ Dados des",
        f"⚠️ Dados desa",
        f"⚠️ Dados desat",
        f"⚠️ Dados desatu",
        f"⚠️ Dados desatua",
        f"⚠️ Dados desatual",
        f"⚠️ Dados desatuali",
        f"⚠️ Dados desatualiz",
        f"⚠️ Dados desatualiza",
        f"⚠️ Dados desatualizad",
        f"⚠️ Dados desatualizado",
        f"⚠️ Dados desatualizados",
        f"⚠️ Dados desatualizados.",
        f"⚠️ Dados desatualizados. A",
        f"⚠️ Dados desatualizados. A ú",
        f"⚠️ Dados desatualizados. A úl",
        f"⚠️ Dados desatualizados. A últ",
        f"⚠️ Dados desatualizados. A últi",
        f"⚠️ Dados desatualizados. A últim",
        f"⚠️ Dados desatualizados. A última",
        f"⚠️ Dados desatualizados. A última a",
        f"⚠️ Dados desatualizados. A última at",
        f"⚠️ Dados desatualizados. A última atu",
        f"⚠️ Dados desatualizados. A última atua",
        f"⚠️ Dados desatualizados. A última atual",
        f"⚠️ Dados desatualizados. A última atuali",
        f"⚠️ Dados desatualizados. A última atualiz",
        f"⚠️ Dados desatualizados. A última atualiza",
        f"⚠️ Dados desatualizados. A última atualizaç",
        f"⚠️ Dados desatualizados. A última atualizaçã",
        f"⚠️ Dados desatualizados. A última atualização",
        f"⚠️ Dados desatualizados. A última atualização f",
        f"⚠️ Dados desatualizados. A última atualização fo",
        f"⚠️ Dados desatualizados. A última atualização foi",
        f"⚠️ Dados desatualizados. A última atualização foi e",
        f"⚠️ Dados desatualizados. A última atualização foi em ",
        f"⚠️ Dados desatualizados. A última atualização foi em {data_envio}",
        f"⚠️ Dados desatualizados. A última atualização foi em {data_envio}!"
    ]
    animacao_escrita("warning", mensagens_warning)