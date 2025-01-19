import streamlit as st
import subprocess

if st.button('Pesquisar IG'):
    with st.spinner('pesquisando'):
         os = subprocess.run(["python", "testing/scrapFile.py"], capture_output=True)
         st.write(os)