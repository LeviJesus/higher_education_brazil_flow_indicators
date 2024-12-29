# %%
from scripts.data_downloader import DataDownloader
from scripts.data_processor import DataProcessor
from scripts.db_manager import DatabaseManager

def initialize_database():
    """Configurar o banco de dados SQLite e criar a tabela necessária."""
    db_manager = DatabaseManager()
    conn = db_manager.connect()

    # Definição do esquema para a tabela
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

    # Criar a tabela
    db_manager.create_table("student_trajectory_2014_2023", schema)

    # Fechar conexão
    db_manager.close()

def main():
    # Passo 1: Baixar e Extrair
    downloader = DataDownloader(
        url="http://download.inep.gov.br/informacoes_estatisticas/indicadores_educacionais/indicadores_fluxo_es_2014-2023.zip")
    downloader.download()
    downloader.extract()

    # Passo 2: Inicializar Banco de Dados e Processar Dados
    print("Inicializando banco de dados...")
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
