import streamlit as st
import pandas as pd
import plotly.express as px
from data_loader import load_data

# Load data
data = load_data()

# Meaning of selected indicators
indicator_meanings = {
    "TAP": "Retention Rate",
    "TCA": "Cumulative Completion Rate",
    "TDA": "Cumulative Dropout Rate",
    "TCAN": "Annual Completion Rate",
    "TADA": "Annual Dropout Rate", 
}

# Add image at the top of the sidebar
st.sidebar.image("./assets/inep.png", use_container_width=False)

# Filters in the sidebar
st.sidebar.title("Filters")
selected_years = st.sidebar.slider("Select Year Range", 2014, 2023, (2014, 2023))
selected_indicator = st.sidebar.selectbox(
    "Choose a Trajectory Indicator",
    ["TAP", "TCA", "TDA", "TCAN", "TADA"],
)

selected_characteristic = st.sidebar.selectbox(
    "Choose a Characteristic for Analysis",
    options=[
        "University Category",
        "Academic Degree", 
        "Teaching Modality",
        "Region"
    ],
    index=0
)

# Additional filters with dependency
selected_states = st.sidebar.multiselect(
    "Filter by State",
    options=data["State"].unique(),
    default=[]
)

# Filter data based on selected states
filtered_data_state = data[data["State"].isin(selected_states)] if selected_states else data

selected_universities = st.sidebar.multiselect(
    "Filter by University",
    options=filtered_data_state["University Name"].unique(),
    default=[]
)

# Filter data based on selected universities
filtered_data_uni = filtered_data_state[filtered_data_state["University Name"].isin(selected_universities)] if selected_universities else filtered_data_state

selected_courses = st.sidebar.multiselect(
    "Filter by Course",
    options=filtered_data_uni["Course Name"].unique(),
    default=[]
)

# Filter data based on user selections
filtered_data = data[
    (data["NU_ANO_REFERENCIA"].between(selected_years[0], selected_years[1])) &
    (data[selected_indicator].notnull())
]

if selected_states:
    filtered_data = filtered_data[filtered_data["State"].isin(selected_states)]

if selected_universities:
    filtered_data = filtered_data[filtered_data["University Name"].isin(selected_universities)]

if selected_courses:
    filtered_data = filtered_data[filtered_data["Course Name"].isin(selected_courses)]

# Group data by selected characteristics and year
grouped_data = filtered_data.groupby(
        ["NU_ANO_REFERENCIA", selected_characteristic])[selected_indicator].mean().reset_index()

# Plotting
st.title("INEP - Higher Education Flow Indicators in Brazil")
st.write("This application shows the indicators of the 10-year academic journey of Brazilian students who entered higher education in 2014.")
st.subheader(f"{indicator_meanings[selected_indicator]} - {selected_indicator}")

fig = px.line(
    grouped_data,
    x="NU_ANO_REFERENCIA",
    y=selected_indicator,
    color=selected_characteristic,
    title=f"Average Evolution Over the Years",
    labels={"NU_ANO_REFERENCIA": "Reference Year", selected_indicator: selected_indicator}
)

st.plotly_chart(fig)

# Additional links
with open("./data/Data_Dictionary.docx", "rb") as file:
    st.sidebar.download_button(
        label="Download Data Dictionary",
        data=file,
        file_name="Data_Dictionary.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        use_container_width=True
    )

st.sidebar.markdown("[Source and Methodology - INEP](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais/indicadores-de-fluxo-da-educacao-superior)")
st.sidebar.write("Made with 🦾 using Streamlit")

# Remove "Deploy" and the three dots
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
