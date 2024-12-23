import pandas as pd
import streamlit as st
import upload
import plotly.express as px


# Função para carregar o arquivo Excel
def load_data(file_path):
    return pd.read_excel(file_path)


# Função de classificação do tipo de certificação
def classify_certification(data_certificado, data_validade):
    if pd.isnull(data_certificado) or pd.isnull(data_validade):
        return "Dados insuficientes"

    delta = (data_validade - data_certificado).days
    if 710 <= delta <= 750:  # Aproximadamente 2 anos em dias, com margem de 10 dias
        return "Certificação inicial"
    else:
        return "Troca de OCD"


# Função de classificação de OCD
def classify_certificado(certificado):
    certificado_str = str(certificado)

    if certificado_str.isdigit() and 1 <= int(certificado_str) <= 150000:
        return "IBRACE"
    elif len(certificado_str) == 8 and certificado_str[3] == "-" and certificado_str[6] == "-":
        return "ACERT"
    elif "OCD" in certificado_str and "ABCP" not in certificado_str:
        return "BRICS"
    elif "ABCP" in certificado_str:
        return "ABCP"
    elif "MODERNA" in certificado_str:
        return "MODERNA"
    elif "ICC" in certificado_str:
        return "ICC"
    elif "TÜV" in certificado_str:
        return "TUV"
    elif "TEL" in certificado_str:
        return "ACTA"
    elif "BRA" in certificado_str:
        return "BR APPROVAL"
    elif "BRC" in certificado_str:
        return "BRACERT"
    elif "CCPE" in certificado_str:
        return "CCPE"
    elif "CPQD" in certificado_str:
        return "CPQD"
    elif "CTCP" in certificado_str:
        return "CTCP"
    elif "DEKRA" in certificado_str:
        return "DEKRA"
    elif "ELD" in certificado_str:
        return "ELDORADO"
    elif "IBR" in certificado_str:
        return "IBR TECH"
    elif "TELECOM" in certificado_str:
        return "INTERTEK"
    elif "LPM" in certificado_str:
        return "LPM"
    elif "MT" in certificado_str:
        return "MASTER"
    elif "NCC" in certificado_str:
        return "NCC"
    elif "OCP" in certificado_str:
        return "OCPTELLI"
    elif "PCN" in certificado_str:
        return "PCN"
    elif "QC" in certificado_str:
        return "QCCERT"
    elif "7C" in certificado_str:
        return "SEVEN COMPLIANCE"
    elif "UL-BR" in certificado_str:
        return "UL"
    elif "Versys" in certificado_str:
        return "VERSYS"
    elif len(certificado_str) == 8 and certificado_str.startswith("100"):
        return "TECPAR CERT"
    else:
        return "OUTROS"


# Título da aplicação
def main():
    st.title("Análise por Tipo de Certificado")

    # Upload do arquivo
   # uploaded_file = upload.upload()
    uploaded_file = st.file_uploader("Escolha um arquivo Excel", type=["xlsx", "xls"])
    if uploaded_file:
        # Carregar os dados
        data = upload.load_data(uploaded_file)

        # Remover duplicatas baseadas na coluna 'Certificado de Conformidade Técnica'
        #data = data.drop_duplicates(subset=["Certificado de Conformidade Técnica"])

        # Verificar se as colunas necessárias existem
        if "Data do Certificado de Conformidade Técnica" in data.columns and "Data de Validade do Certificado" in data.columns:
            # Garantir que as colunas de datas estão no formato correto
            data["Data do Certificado de Conformidade Técnica"] = pd.to_datetime(
                data["Data do Certificado de Conformidade Técnica"], errors='coerce')
            data["Data de Validade do Certificado"] = pd.to_datetime(data["Data de Validade do Certificado"],
                                                                     errors='coerce')

            # Remover linhas com datas inválidas
            data = data.dropna(
                subset=["Data do Certificado de Conformidade Técnica", "Data de Validade do Certificado"])

            # Aplicar a função de classificação
            data["OCD Classificação"] = data["Certificado de Conformidade Técnica"].apply(classify_certificado)

            # Classificar tipo de certificação
            data["Tipo de Certificação"] = data.apply(
                lambda row: classify_certification(row["Data do Certificado de Conformidade Técnica"],
                                                   row["Data de Validade do Certificado"]), axis=1
            )

            # Seleção de intervalo de datas na barra lateral
            st.sidebar.header("Seleção de Datas")
            min_date = data["Data do Certificado de Conformidade Técnica"].min()
            max_date = data["Data do Certificado de Conformidade Técnica"].max()

            date_range = st.sidebar.date_input(
                "Selecione o intervalo de datas:", [min_date, max_date], min_value=min_date, max_value=max_date
            )

            if len(date_range) == 2:
                start_date, end_date = date_range
                data = data[(data["Data do Certificado de Conformidade Técnica"] >= pd.Timestamp(start_date)) &
                            (data["Data do Certificado de Conformidade Técnica"] <= pd.Timestamp(end_date))]

            # Dropdown para seleção de OCD
            ocd_selecionado = st.sidebar.selectbox(
                "Selecione a classificação OCD:", ["Todos"] + data["OCD Classificação"].unique().tolist()
            )

            if ocd_selecionado != "Todos":
                data = data[data["OCD Classificação"] == ocd_selecionado]

            # Dropdown para seleção de tipo de certificação
            tipo_certificacao = st.sidebar.selectbox(
                "Selecione o tipo de certificação:", ["Todos", "Certificação inicial", "Troca de OCD"]
            )

            if tipo_certificacao != "Todos":
                data = data[data["Tipo de Certificação"] == tipo_certificacao]

            if ocd_selecionado == "Todos":
                # Gráfico de pizza para classificação de OCD
                st.subheader("Distribuição de Classificação de OCD")
                ocd_counts = data["OCD Classificação"].value_counts().reset_index()
                ocd_counts.columns = ["OCD Classificação", "Count"]
                fig_ocd = px.pie(ocd_counts, values="Count", names="OCD Classificação",
                                 title="Distribuição de Classificação de OCD")
                st.plotly_chart(fig_ocd)

           # if tipo_certificacao == "Todos":
            # Gráfico de barras para tipos de certificação
            st.subheader("Distribuição de Tipos de Certificação")
            tipo_certificacao_counts = data["Tipo de Certificação"].value_counts().reset_index()
            tipo_certificacao_counts.columns = ["Tipo de Certificação", "Count"]
            fig_tipo = px.bar(tipo_certificacao_counts, x="Tipo de Certificação", y="Count",
                              title="Distribuição de Tipos de Certificação")
            st.plotly_chart(fig_tipo)

            # st.dataframe(data)

        else:
            st.error(
                "As colunas necessárias ('Data do Certificado de Conformidade Técnica', 'Data de Validade do Certificado') não foram encontradas no arquivo."
            )
    else:
        st.info("Aguardando o upload do arquivo Excel.")


if __name__ == "__main__":
    main()
