import pandas as pd
import sqlite3

def carregar_dados(file_path):
    # Conectar ao banco de dados
    conn = sqlite3.connect('database.db')
    
    # Carregar dados
    query = "SELECT * FROM student_trajectory_2014_2023"
    dados = pd.read_sql_query(query, conn)
    
    # Fechar a conexão
    conn.close()

    # Mapear categorias para melhor entendimento
    mapa_categoria_univ = {
        1: "Pública Federal",
        2: "Pública Estadual",
        3: "Pública Municipal",
        4: "Privada c/ Fins Lucrativos",
        5: "Privada s/ Fins Lucrativos",
        7: "Especial"
    }

    mapa_categoria_cursos = {
        1: "Bacharelado",
        2: "Licenciatura",
        3: "Tecnológico",
    }

    mapa_categoria_mod = {
        1: "Presencial",
        2: "EaD"
    }

    mapa_categoria_regiao = {
        1: "Norte",
        2: "Nordeste",
        3: "Sudeste",
        4: "Sul",
        5: "Centro-Oeste"
    }

    mapa_unidades_federativas = {
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
        53: "Distrito Federal"
    }

    dados["TP_CATEGORIA_ADMINISTRATIVA"] = dados["TP_CATEGORIA_ADMINISTRATIVA"].map(mapa_categoria_univ)
    dados["TP_GRAU_ACADEMICO"] = dados["TP_GRAU_ACADEMICO"].map(mapa_categoria_cursos)
    dados["TP_MODALIDADE_ENSINO"] = dados["TP_MODALIDADE_ENSINO"].map(mapa_categoria_mod)
    dados["CO_REGIAO"] = dados["CO_REGIAO"].map(mapa_categoria_regiao)
    dados["CO_UF"] = dados["CO_UF"].map(mapa_unidades_federativas)
    
    dados.rename(columns={
        "NO_IES": "Nome da Universidade",
        "TP_CATEGORIA_ADMINISTRATIVA": "Categoria Universidade",
        "NO_CURSO": "Nome do Curso",
        "CO_REGIAO": "Região",
        "CO_UF": "Unidade Federativa",
        "TP_GRAU_ACADEMICO": "Grau Acadêmico",
        "TP_MODALIDADE_ENSINO": "Modalidade de Ensino",
        "QT_PERMANENCIA": "Quantidade de Permanência",
        "QT_CONCLUINTE": "Quantidade de Concluintes",
        "QT_DESISTENCIA": "Quantidade de Desistências",
        "QT_FALECIDO": "Quantidade de Falecidos"
    }, inplace=True)

    return dados
