import streamlit as st

st.markdown("""
<style>
.container {
    position: relative;
    text-align: center;
}
.input-overlay {
    position: absolute;
    top: 100px; /* Ajuste conforme a imagem */
    left: 50px;
}
</style>
""", unsafe_allow_html=True)

st.image("currentSTapp/notebook.jpg", use_container_width=True)
with st.container():
    st.text_input("Linha 1", key="line1")