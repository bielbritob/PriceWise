import streamlit as st
import subprocess

if st.button('Pesquisar IG'):
    with st.spinner('pesquisando'):
         os = subprocess.run(["python", "testing/scrapFile.py"], capture_output=True)
         st.write(os)

if st.button('instalar zendriver'):
    with st.spinner('instalando zendriver'):
        zen = subprocess.run(['pip', 'install', 'zendriver'], capture_output=True)
        st.write(zen)

