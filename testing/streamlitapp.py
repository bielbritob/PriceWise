import streamlit as st
import subprocess

seletor =  st.checkbox('Script seletor de cidade? (apenas na 1ª vez)')
produto = st.text_input('text input', placeholder='leite integral, uva, ovo...')

if st.button('Pesquisar IG') and seletor:
    with st.spinner('pesquisando'):
         os1 = subprocess.run(["python",
                              "testing/scrapFile.py", produto, "True"],
                             capture_output=True)
         st.write(os1)



zencheck = st.checkbox('ja tem o zen?')
if st.button('instalar zendriver'):
    with st.spinner('instalando zendriver'):
        zencheck = True
        zen = subprocess.run(['pip', 'install', 'zendriver'], capture_output=True)
        st.write(zen)

