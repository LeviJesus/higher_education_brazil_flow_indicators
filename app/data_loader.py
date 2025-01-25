import pandas as pd
import sqlite3

def load_data():
    # Connect to the database
    conn = sqlite3.connect('./data/database.db')
    
    # Load data
    query = "SELECT * FROM student_trajectory_2014_2023"
    data = pd.read_sql_query(query, conn)
    
    # Close the connection
    conn.close()

    # Map categories for better understanding
    university_category_map = {
        1: "Federal Public",
        2: "State Public",
        3: "Municipal Public",
        4: "Private For-Profit",
        5: "Private Non-Profit",
        7: "Special"
    }

    course_category_map = {
        1: "Bachelor",
        2: "Licentiate",
        3: "Technological",
    }

    modality_category_map = {
        1: "In-Person",
        2: "Distance Learning"
    }

    region_category_map = {
        1: "North",
        2: "Northeast",
        3: "Southeast",
        4: "South",
        5: "Central-West"
    }

    state_map = {
        11: "Rondônia",
        12: "Acre",
        13: "Amazonas",
        14: "Roraima",
        15: "Pará",
        16: "Amapá",
        17: "Tocantins",
        21: "Maranhão",
        22: "Piauí",
        23: "Ceará",
        24: "Rio Grande do Norte",
        25: "Paraíba",
        26: "Pernambuco",
        27: "Alagoas",
        28: "Sergipe",
        29: "Bahia",
        31: "Minas Gerais",
        32: "Espírito Santo",
        33: "Rio de Janeiro",
        35: "São Paulo",
        41: "Paraná",
        42: "Santa Catarina",
        43: "Rio Grande do Sul",
        50: "Mato Grosso do Sul",
        51: "Mato Grosso",
        52: "Goiás",
        53: "Federal District"
    }

    data["TP_CATEGORIA_ADMINISTRATIVA"] = data["TP_CATEGORIA_ADMINISTRATIVA"].map(university_category_map)
    data["TP_GRAU_ACADEMICO"] = data["TP_GRAU_ACADEMICO"].map(course_category_map)
    data["TP_MODALIDADE_ENSINO"] = data["TP_MODALIDADE_ENSINO"].map(modality_category_map)
    data["CO_REGIAO"] = data["CO_REGIAO"].map(region_category_map)
    data["CO_UF"] = data["CO_UF"].map(state_map)
    
    data.rename(columns={
        "NO_IES": "University Name",
        "TP_CATEGORIA_ADMINISTRATIVA": "University Category",
        "NO_CURSO": "Course Name",
        "CO_REGIAO": "Region",
        "CO_UF": "State",
        "TP_GRAU_ACADEMICO": "Academic Degree",
        "TP_MODALIDADE_ENSINO": "Teaching Modality",
        "QT_PERMANENCIA": "Permanence Quantity",
        "QT_CONCLUINTE": "Graduate Quantity",
        "QT_DESISTENCIA": "Dropout Quantity",
        "QT_FALECIDO": "Deceased Quantity"
    }, inplace=True)

    return data
