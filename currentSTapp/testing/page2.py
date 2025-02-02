import streamlit as st
import sqlite3
import unicodedata
from streamlit_image_select_my import image_select
import pandas as pd

# Configuração da interface do Streamlit
st.set_page_config(page_title="PriceWise - Lista de Compras", page_icon="📝", layout="centered")

# Título e barra de busca
st.title("📝 PriceWise - Lista de Compras")

# Link para voltar para pw_test.py
col1, col2, col3 = st.columns([1, 3, 1])
with col3:
    st.markdown(
        """
        <div style="text-align: right;">
            <a href="currentSTapp/testing/pw_app.py" target="_blank" style="text-decoration: none;
             color: white;
              background-color: rgba(143, 151, 74, 0.15);
               padding: 10px 15px;
                border-radius: 5px;
                ">🏠 Home
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )


# Reutilizar as funções do arquivo original
def get_db():
    conn = sqlite3.connect("currentSTapp/produtos.db")
    conn.create_function("remover_acentos", 1, remover_acentos)
    return conn


def remover_acentos(texto):
    return ''.join(
        letra for letra in unicodedata.normalize('NFD', texto)
        if unicodedata.category(letra) != 'Mn'
    )


def buscar_produtos(nome, mercado):
    # Reutilizar a função de busca do original
    conn = get_db()
    cursor = conn.cursor()

    nome = nome.capitalize() if nome else ""
    palavras_chave = nome.split()

    if mercado == "Todos":
        mercado_clause = ""
    else:
        mercado_clause = "AND mercado = ?"

    consulta = f"""
        SELECT * FROM produtos 
        WHERE LOWER(nome) LIKE LOWER(?)
        {mercado_clause}
    """

    parametros = [f"%{nome}%"]
    if mercado != "Todos":
        parametros.append(mercado)

    cursor.execute(consulta, parametros)
    produtos = cursor.fetchall()

    produtos.sort(key=lambda x: x[6])  # Ordenar por preço

    conn.close()
    return produtos


# Inicializar a sessão para a lista de compras
if 'shopping_list' not in st.session_state:
    st.session_state.shopping_list = []

# Layout em duas colunas
col_search, col_list = st.columns([2, 1])

with col_search:
    st.subheader("Buscar Produtos")

    # Seletor de mercado
    logos = {
        "Todos": "logos/todosmercados.png",
        "Irmãos Gonçalves": "logos/ig2.png",
        "Meta21": "logos/meta21.png",
        "Nova Era": "logos/novaera300.png",
        "Atacadão": "logos/atacadao1.png"
    }

    images = list(logos.values())
    captions = list(logos.keys())

    selected_index = image_select(
        label="Selecione um mercado:",
        images=images,
        use_container_width=False,
        captions=captions,
        index=0,
        return_value="index"
    )

    selected_market = captions[selected_index]

    # Campo de busca com dois botões
    with st.form("search_form", border=False):
        product_name = st.text_input(
            "Digite o produto que deseja pesquisar:",
            placeholder="Ex. leite integral, café 500g..."
        )
        col1, col2 = st.columns(2)
        with col1:
            submit_button = st.form_submit_button("🔍 Buscar")
        with col2:
            add_to_list_button = st.form_submit_button("📝 Adicionar à Lista")

    # Área de resultados da busca
    if (submit_button or add_to_list_button) and product_name:
        produtos = buscar_produtos(product_name, selected_market)
        if produtos:
            for produto in produtos:
                col_img, col_info, col_action = st.columns([1, 2, 1])

                with col_img:
                    st.image(produto[9], width=100)

                with col_info:
                    st.write(f"""
                    **{produto[3]}**  
                    R$ {float(produto[6]):.2f}  
                    {produto[2]}
                    """)

                with col_action:
                    # Se clicou em Adicionar à Lista, mostra apenas o botão de adicionar
                    if add_to_list_button:
                        if st.button("➕ Adicionar", key=f"add_{produto[0]}"):
                            novo_item = {
                                "nome": produto[3],
                                "preco": float(produto[6]),
                                "mercado": produto[2],
                                "imagem": produto[9]
                            }
                            st.session_state.shopping_list.append(novo_item)
                            st.success(f"'{produto[3]}' adicionado à lista!")
                    # Se clicou em Buscar, mostra apenas o link para o produto
                    else:
                        st.markdown(f"[🔗 Ver no Site]({produto[5]})")

                st.markdown("---")
        else:
            st.warning("Nenhum produto encontrado.")

with col_list:
    st.subheader("📋 Minha Lista")

    if st.session_state.shopping_list:
        # Mostrar items na lista com opção de remover
        for i, item in enumerate(st.session_state.shopping_list):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"""
                **{item['nome']}**  
                R$ {item['preco']:.2f} - {item['mercado']}
                """)
            with col2:
                if st.button("🗑️", key=f"remove_{i}"):
                    st.session_state.shopping_list.pop(i)
                    st.rerun()

        # Mostrar total
        total = sum(item["preco"] for item in st.session_state.shopping_list)
        st.markdown("---")
        st.write(f"**Total: R$ {total:.2f}**")

        # Botões de ação
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Limpar Lista"):
                st.session_state.shopping_list = []
                st.rerun()

        with col2:
            # Exportar lista
            df = pd.DataFrame(st.session_state.shopping_list)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Exportar",
                csv,
                "minha_lista.csv",
                "text/csv",
                key='download-csv'
            )
    else:
        st.info("Sua lista está vazia. Use a busca para adicionar produtos!")