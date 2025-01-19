import streamlit as st
import subprocess

seletor =  st.checkbox('Script seletor de cidade? (apenas na 1ª vez)')
produto = st.text_input('text input', placeholder='leite integral, uva, ovo...')
if st.button('Pesquisar IG'):
    with st.spinner('pesquisando'):
        if seletor:
             os = subprocess.run(["python",
                                  "testing/scrapFile.py", produto, "True",
                                  "True"],
                                 capture_output=True)
             st.write(os)
        else:
            os = subprocess.run(["python",
                                 "testing/scrapFile.py", produto, "False"],
                                capture_output=True)
            st.write(os)
        screenshot_path = "/tmp/screenshot.png"
        st.image(screenshot_path, caption="Screenshot da página")



zencheck = st.checkbox('ja tem o zen?')
if st.button('instalar zendriver'):
    with st.spinner('instalando zendriver'):
        zencheck = True
        zen = subprocess.run(['pip', 'install', 'zendriver'], capture_output=True)
        st.write(zen)

