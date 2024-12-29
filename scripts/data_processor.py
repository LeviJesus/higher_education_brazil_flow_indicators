import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path

class DataProcessor:
    def __init__(self, raw_data_path="data/raw", db_path="data/database.db", processed_data_path="data/processed", chunk_size=5000):
        self.raw_data_path = Path(raw_data_path)
        self.db_path = Path(db_path)
        self.processed_data_path = Path(processed_data_path)
        self.chunk_size = chunk_size

    def load_and_save_to_db(self, excel_file, sheet_name, table_name):
        """Carregar um grande arquivo Excel em partes, salvar dados no SQLite e escrever dados processados em CSV."""
        file_path = self.raw_data_path / excel_file
        engine = create_engine(f"sqlite:///{self.db_path}")
        processed_file_path = self.processed_data_path / f"{table_name}.csv"

        try:
            print(f"Carregando dados de {file_path} na tabela '{table_name}' no banco de dados...")

            # Clear existing table data
            with engine.connect() as connection:
                connection.execute(text(f"DELETE FROM {table_name}"))
                print(f"Tabela '{table_name}' limpa antes de inserir novos dados.")

            # Converter Excel para CSV
            df = pd.read_excel(file_path, skiprows=8, header=0, sheet_name=sheet_name, engine='openpyxl')
            df.to_csv(processed_file_path, index=False)

            # Inicializar um DataFrame vazio para coletar todas as partes
            all_data = pd.DataFrame()

            # Ler CSV em partes
            for chunk in pd.read_csv(processed_file_path, chunksize=self.chunk_size):
                # Limpar parte (por exemplo, remover espaços das colunas)
                chunk.columns = [col.strip() for col in chunk.columns]

                # Escrever parte no banco de dados
                chunk.to_sql(table_name, con=engine, if_exists='append', index=False)
                print(f"Processada uma parte com {len(chunk)} linhas.")

                # Adicionar parte ao DataFrame all_data
                all_data = pd.concat([all_data, chunk], ignore_index=True)

            print(f"Dados carregados com sucesso na tabela '{table_name}' no banco de dados.")

        except Exception as e:
            print(f"Erro ao carregar dados no banco de dados: {e}")
            raise
