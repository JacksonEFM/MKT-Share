import pandas as pd
import streamlit as st
import ocd_data
import nome_solicitante
import tipo_de_produto
import tipo_de_certificado
import plotly.express as px
import ocd

st.set_page_config(page_title="MKT Share", layout="wide")

# Menu de navegação aprimorado
st.sidebar.title("Menu")
opcao = st.sidebar.radio("Selecione uma opção",
                         ["TIPO DE CERTIFICADO", "NOME DO SOLICITANTE", "TIPO DE PRODUTO", "OCD X NOME COMERCIAL","Certificados - OCD"])

if opcao == "TIPO DE CERTIFICADO":
    tipo_de_certificado.main()
elif opcao == "NOME DO SOLICITANTE":
    nome_solicitante.main()
elif opcao == "TIPO DE PRODUTO":
    tipo_de_produto.main()
elif opcao == "OCD X NOME COMERCIAL":
    ocd_data.main()
elif opcao == "Certificados - OCD":
    ocd.main()