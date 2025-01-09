import streamlit as st
import pandas as pd
import json
import subprocess

def find_lowest_price(product):
    #Call the data scraping script
    subprocess.call(['python', 'coletarDados.py', product])

    #load JSON file with scraped data
    with open('product_data.json') as json_file:
        data = json.load(json_file)

    #convert JSON to DataFrame
    df = pd.DataFrame(data)

    #replace ',' with '.' and remove "R$" from values
    df["Preco"] = df["Preco"].replace({'R\$': '', ',': '.'}, regex=True).astype(float)

    #return the row having minimum value of "Preço"
    return df.loc[df["Preco"].idxmin()]

def main():
    st.title('Market price comparison')
    product_name = st.text_input("Enter the product name:", "Type Here ...")

    if st.button('Find Lowest Price'):
        result = find_lowest_price(product_name)
        st.write(f"The market '{result['Mercado']}' has the lowest price for this product: R$  {result['Preco']}")
        st.image(result['Img'], width=200,caption=result['Titulo'])

if __name__ == "__main__":
    main()