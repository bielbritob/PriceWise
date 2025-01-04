import streamlit as st
import json
import subprocess


# Função para carregar dados do JSON
def carregar_dados_json(arquivo="dados_produtos.json"):
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


# Função para calcular o melhor mercado para uma lista de compras
def calcular_melhor_mercado(lista_compras, dados):
    mercados = {}
    for produto in lista_compras:
        for item in dados:
            if produto.lower() in item["Título"].lower():
                mercado = item["Mercado"]
                preco = float(item["Preço"].replace("R$", "").replace(",", ".").strip())
                if mercado not in mercados:
                    mercados[mercado] = 0
                mercados[mercado] += preco
    if mercados:
        melhor_mercado = min(mercados, key=mercados.get)
        return melhor_mercado, mercados[melhor_mercado]
    return None, 0


# Logos dos mercados (substitua pelos caminhos corretos das imagens)
logos = {
    "Irmãos Gonçalves": "logos/ig.png",
    "Meta 21": "logos/meta21.png",
    "Supernova": "logos/novaera.png"
}

# Interface do Streamlit
st.title("Comparador de Preços")

# Opção: Lista de Compras ou Pesquisa Individual
modo = st.radio("Selecione o modo:", ("Lista de Compras", "Pesquisa Individual"))

if modo == "Lista de Compras":
    st.subheader("Adicione os produtos da sua lista de compras:")
    lista_compras = st.text_area("Digite um produto por linha (ex: café 500g, leite integral):").split("\n")
    lista_compras = [item.strip() for item in lista_compras if item.strip()]

    if st.button("Calcular Melhor Mercado"):
        if lista_compras:
            with st.spinner("Calculando o melhor mercado..."):
                # Limpa o JSON antes de coletar novos dados
                with open("dados_produtos.json", "w", encoding="utf-8") as f:
                    json.dump([], f)

                # Executa o script de coleta para cada produto
                for produto in lista_compras:
                    resultado = subprocess.run(
                        ["python", "coletarDados.py", produto],
                        capture_output=True,
                        text=True
                    )

                # Carrega os dados coletados
                dados = carregar_dados_json()
                if dados:
                    melhor_mercado, total = calcular_melhor_mercado(lista_compras, dados)
                    if melhor_mercado:
                        st.success(f"Melhor mercado para sua lista: **{melhor_mercado}** (Total: R$ {total:.2f})")
                        st.image(logos[melhor_mercado], width=100)
                    else:
                        st.warning("Nenhum mercado encontrado para os produtos da lista.")
                else:
                    st.warning("Nenhum dado coletado.")
        else:
            st.warning("Por favor, adicione produtos à lista de compras.")

else:  # Modo Pesquisa Individual
    produto_pesquisa = st.text_input("Digite o produto que deseja pesquisar:")

    if st.button("Pesquisar"):
        if produto_pesquisa:
            with st.spinner("Pesquisando produtos..."):
                # Limpa o JSON antes de coletar novos dados
                with open("dados_produtos.json", "w", encoding="utf-8") as f:
                    json.dump([], f)

                # Executa o script de coleta
                resultado = subprocess.run(
                    ["python", "coletarDados.py", produto_pesquisa],
                    capture_output=True,
                    text=True
                )

            # Botão para mostrar/ocultar logs
            if st.checkbox("Mostrar logs do script de coleta"):
                st.subheader("Logs do Script de Coleta")
                st.text("Saída (stdout):")
                st.text(resultado.stdout)
                st.text("Erros (stderr):")
                st.text(resultado.stderr)

            if resultado.returncode == 0:  # Verifica se o script foi executado com sucesso
                dados = carregar_dados_json()
                if dados:
                    # Filtra os produtos pesquisados
                    produtos_filtrados = [item for item in dados if produto_pesquisa.lower() in item["Título"].lower()]
                    if produtos_filtrados:
                        # Encontra o produto mais barato
                        produto_mais_barato = min(produtos_filtrados, key=lambda x: float(
                            x["Preço"].replace("R$", "").replace(",", ".").strip()))

                        st.subheader(f"Produto mais barato encontrado:")
                        st.write(f"**Título:** {produto_mais_barato['Título']}")
                        st.write(f"**Preço:** {produto_mais_barato['Preço']}")
                        st.write(f"**Mercado:** {produto_mais_barato['Mercado']}")
                        st.image(logos[produto_mais_barato["Mercado"]], width=100)
                        st.markdown(
                            f"[Acesse o produto no {produto_mais_barato['Mercado']}]({produto_mais_barato.get('link', '#')})")
                    else:
                        st.warning("Nenhum produto encontrado.")
                else:
                    st.warning("Nenhum dado coletado.")
            else:
                st.error("Erro ao coletar dados. Verifique os logs acima.")
        else:
            st.warning("Por favor, digite um produto para pesquisar.")