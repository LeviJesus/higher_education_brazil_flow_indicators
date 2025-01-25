# %%
from scripts.data_downloader import DataDownloader
from scripts.data_processor import DataProcessor
from scripts.db_manager import DatabaseManager

def initialize_database():
    """Set up the SQLite database and create the necessary table."""
    db_manager = DatabaseManager()
    conn = db_manager.connect()

    # Table schema definition
    schema = """
        CO_IES INTEGER,
        NO_IES TEXT,
        TP_CATEGORIA_ADMINISTRATIVA INTEGER,
        TP_ORGANIZACAO_ACADEMICA INTEGER,
        CO_CURSO INTEGER,
        NO_CURSO TEXT,
        CO_REGIAO INTEGER,
        CO_UF INTEGER,
        CO_MUNICIPIO INTEGER,
        TP_GRAU_ACADEMICO INTEGER,
        TP_MODALIDADE_ENSINO INTEGER,
        CO_CINE_ROTULO TEXT,
        NO_CINE_ROTULO TEXT,
        CO_CINE_AREA_GERAL INTEGER,
        NO_CINE_AREA_GERAL TEXT,
        NU_ANO_INGRESSO INTEGER,
        NU_ANO_REFERENCIA INTEGER,
        NU_PRAZO_INTEGRALIZACAO INTEGER,
        NU_ANO_INTEGRALIZACAO INTEGER,
        NU_PRAZO_ACOMPANHAMENTO INTEGER,
        NU_ANO_MAXIMO_ACOMPANHAMENTO INTEGER,
        QT_INGRESSANTE INTEGER,
        QT_PERMANENCIA INTEGER,
        QT_CONCLUINTE INTEGER,
        QT_DESISTENCIA INTEGER,
        QT_FALECIDO INTEGER,
        TAP REAL,
        TCA REAL,
        TDA REAL,
        TCAN REAL,
        TADA REAL
    """

    # Create the table
    db_manager.create_table("student_trajectory_2014_2023", schema)

    # Close connection
    db_manager.close()

def main():
    # Step 1: Download and Extract
    downloader = DataDownloader(
        url="http://download.inep.gov.br/informacoes_estatisticas/indicadores_educacionais/indicadores_fluxo_es_2014-2023.zip")
    downloader.download()
    downloader.extract()

    # Step 2: Initialize Database and Process Data
    print("Initializing database...")
    initialize_database()

    processor = DataProcessor()
    processor.load_and_save_to_db(
        excel_file="indicadores_trajetoria_educacao_superior_2014_2023.xlsx",
        sheet_name="INDICADORES_TRAJETORIA", 
        table_name="student_trajectory_2014_2023"
    )

if __name__ == "__main__":
    main()

# %%
