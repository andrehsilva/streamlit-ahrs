import streamlit as st
import pandas as pd

@st.cache

def load_data():
    columns = {
    'ocorrencia_latitude' : 'latitude',
    'ocorrencia_longitude' : 'longitude',
    'ocorrencia_dia' : 'dia',
    'ocorrencia_classificacao' : 'classificacao',
    'ocorrencia_tipo' : 'tipo',
    'ocorrencia_tipo_categoria' : 'tipo_categoria',
    'ocorrencia_tipo_icao' : 'tipo_icao',
    'ocorrencia_aerodromo' : 'aerodromo',
    'ocorrencia_cidade' : 'cidade',
    'investigacao_status' : 'status',
    'divulgacao_relatorio_numero' : 'relatorio_numero',
    'total_aeronaves_envolvidas' : 'aeronaves_envolvidas'
    }



    DATA_URL = "https://raw.githubusercontent.com/carlosfab/curso_data_science_na_pratica/master/modulo_02/ocorrencias_aviacao.csv"

    data = pd.read_csv(DATA_URL, index_col='codigo_ocorrencia')
    data = data.rename(columns=columns)
    data.dia = data.dia + " " + data.ocorrencia_horario
    data.dia = pd.to_datetime(data.dia)
    data = data[list(columns.values())]

    return data

#carregar os dados

df = load_data()
labels = df.classificacao.unique().tolist()


#SIDEBAR

st.sidebar.subheader("Parâmetros")
info_sidebar = st.sidebar.empty()


st.sidebar.subheader("Ano")
year_to_filter= st.sidebar.slider('Escolha o ano desejado', 2008, 2018, 2017)

st.sidebar.subheader("Tabela")
tabela = st.sidebar.empty()


label_to_filter = st.sidebar.multiselect(
    label="Escolha a classificação da ocorrência",
    options=labels,
    default=["INCIDENTE" , "ACIDENTE"]
)

st.sidebar.markdown("""
A base de dados de ocorrências aeronáuticas e gerenciada pela CENIPA
""")

filtered_df = df[(df.dia.dt.year == year_to_filter) & (df.classificacao.isin(label_to_filter))]

info_sidebar.info("{} Ocorrências selecionadas". format(filtered_df.shape[0]))

# MAIN
st.sidebar.title("CENIPA - Acidentes Aeronáuticos")

st.markdown(f"""
Estão sendo classificadas as ocorrências como **{", ".join(label_to_filter)}** para o ano de ** {year_to_filter}**
""")

if tabela.checkbox("Mostar tabela de dados"):
    st.write(filtered_df)


st.subheader("Mapa de ocorrências")
st.map(filtered_df)

