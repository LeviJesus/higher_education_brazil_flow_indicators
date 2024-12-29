import sqlite3
from pathlib import Path

class DatabaseManager:
    def __init__(self, db_path="data/database.db"):
        self.db_path = Path(db_path)
        self.connection = None

    def connect(self):
        """Conectar ao banco de dados SQLite."""
        self.connection = sqlite3.connect(self.db_path)
        return self.connection

    def create_table(self, table_name, schema):
        """Criar uma tabela se ela não existir."""
        try:
            with self.connection:
                self.connection.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({schema})")
                print(f"Tabela '{table_name}' está pronta.")
        except sqlite3.Error as e:
            print(f"Erro ao criar tabela: {e}")

    def close(self):
        """Fechar a conexão com o banco de dados."""
        if self.connection:
            self.connection.close()
            print("Conexão com o banco de dados fechada.")
