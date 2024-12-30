import streamlit as st
import pandas as pd
import plotly.express as px
from data_loader import carregar_dados

# Carregar dados
dados = carregar_dados()

# Significado dos indicadores selecionados
significado_indicadores = {
    "TAP": "Taxa de Permanência",
    "TCA": "Taxa de Conclusão Acumulada",
    "TDA": "Taxa de Desistência Acumulada",
    "TCAN": "Taxa de Conclusão Anual",
    "TADA": "Taxa de Desistência Anual", 
}

# Adicionar imagem no topo do sidebar
st.sidebar.image("./assets/inep.png", use_container_width =False)

# Filtros na barra lateral
st.sidebar.title("Filtros")
anos_selecionados = st.sidebar.slider("Selecione o Intervalo de Anos", 2014, 2023, (2014, 2023))
indicador_selecionado = st.sidebar.selectbox(
    "Escolha um Indicador de Trajetória",
    ["TAP", "TCA", "TDA", "TCAN", "TADA"],
)

caracteristica_selecionada = st.sidebar.selectbox(
    "Escolha uma Característica para Análise",
    options=[
        "Categoria Universidade",
        "Grau Acadêmico", 
        "Modalidade de Ensino",
        "Região"
    ],
    index=0
)

# Filtros adicionais com dependência entre si
unidades_federativas_selecionadas = st.sidebar.multiselect(
    "Filtre por Estado",
    options=dados["Unidade Federativa"].unique(),
    default=[]
)

# Filtrar dados com base nas unidades federativas selecionadas
dados_filtrados_uf = dados[dados["Unidade Federativa"].isin(unidades_federativas_selecionadas)] if unidades_federativas_selecionadas else dados

universidades_selecionadas = st.sidebar.multiselect(
    "Filtre por Universidade",
    options=dados_filtrados_uf["Nome da Universidade"].unique(),
    default=[]
)

# Filtrar dados com base nas universidades selecionadas
dados_filtrados_uni = dados_filtrados_uf[dados_filtrados_uf["Nome da Universidade"].isin(universidades_selecionadas)] if universidades_selecionadas else dados_filtrados_uf

cursos_selecionados = st.sidebar.multiselect(
    "Filtre por Curso",
    options=dados_filtrados_uni["Nome do Curso"].unique(),
    default=[]
)

# Filtrar dados com base nas seleções do usuário
dados_filtrados = dados[
    (dados["NU_ANO_REFERENCIA"].between(anos_selecionados[0], anos_selecionados[1])) &
    (dados[indicador_selecionado].notnull())
]

if unidades_federativas_selecionadas:
    dados_filtrados = dados_filtrados[dados_filtrados["Unidade Federativa"].isin(unidades_federativas_selecionadas)]

if universidades_selecionadas:
    dados_filtrados = dados_filtrados[dados_filtrados["Nome da Universidade"].isin(universidades_selecionadas)]

if cursos_selecionados:
    dados_filtrados = dados_filtrados[dados_filtrados["Nome do Curso"].isin(cursos_selecionados)]

# Agrupar dados por características selecionadas e ano
dados_agrupados = dados_filtrados.groupby(
        ["NU_ANO_REFERENCIA", caracteristica_selecionada])[indicador_selecionado].mean().reset_index()

# Plotagem
st.title("INEP - Indicadores de Fluxo da Educação Superior no Brasil")
st.write("Este aplicativo mostra os indicadores de acompanhamento da jornada acadêmica de 10 anos dos estudantes brasileiros que ingressaram no ensino superior em 2014.")
st.subheader(f"{significado_indicadores[indicador_selecionado]} - {indicador_selecionado}")


fig = px.line(
    dados_agrupados,
    x="NU_ANO_REFERENCIA",
    y=indicador_selecionado,
    color=caracteristica_selecionada,
    title=f"Evolução da média ao longo dos anos",
    labels={"NU_ANO_REFERENCIA": "Ano de Referência", indicador_selecionado: indicador_selecionado}
)

st.plotly_chart(fig)

# Links adicionais
with open("./data/Dicionário_acompanhamento_trajetória.docx", "rb") as file:
    st.sidebar.download_button(
        label="Download Dicionário de Dados",
        data=file,
        file_name="Dicionário_acompanhamento_trajetória.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        use_container_width=True
    )

st.sidebar.markdown("[Fonte e Metodologia - INEP](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais/indicadores-de-fluxo-da-educacao-superior)")
st.sidebar.write("Feito com ❤️ usando Streamlit")

# Remover "Deploy" e os três pontinhos
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
