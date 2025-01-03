import streamlit as st
import json
import subprocess


def carregar_dados_json(arquivo="dados_produtos.json"):
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


# Interface do Streamlit
st.title("Comparador de Preços")

# Entrada do usuário
produto_pesquisa = st.text_input("Digite o produto que deseja pesquisar:")

if st.button("Pesquisar"):
    if produto_pesquisa:
        with st.spinner("Pesquisando produtos..."):
            # Executa o script de coleta
            resultado = subprocess.run(
                ["python.exe", "coletarDados.py", produto_pesquisa],
                capture_output=True,
                text=True
            )

        # Exibe logs do script de coleta
        st.subheader("Logs do Script de Coleta")
        st.text("Saída (stdout):")
        st.text(resultado.stdout)
        st.text("Erros (stderr):")
        st.text(resultado.stderr)

        if resultado.returncode == 0:  # Verifica se o script foi executado com sucesso
            dados = carregar_dados_json()
            if dados:
                st.subheader(f"Resultados para: {produto_pesquisa}")
                for item in dados:
                    st.write(f"**Título:** {item['Título']} | **Preço:** {item['Preço']}")
            else:
                st.warning("Nenhum dado encontrado.")
        else:
            st.error("Erro ao coletar dados. Verifique os logs acima.")
    else:
        st.warning("Por favor, digite um produto para pesquisar.")