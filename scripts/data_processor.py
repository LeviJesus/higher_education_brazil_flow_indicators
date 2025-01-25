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
        """Load a large Excel file in chunks, save data to SQLite, and write processed data to CSV."""
        file_path = self.raw_data_path / excel_file
        engine = create_engine(f"sqlite:///{self.db_path}")
        processed_file_path = self.processed_data_path / f"{table_name}.csv"

        try:
            print(f"Loading data from {file_path} into table '{table_name}' in the database...")

            # Clear existing table data
            with engine.connect() as connection:
                connection.execute(text(f"DELETE FROM {table_name}"))
                print(f"Table '{table_name}' cleared before inserting new data.")

            # Convert Excel to CSV
            df = pd.read_excel(file_path, skiprows=8, header=0, sheet_name=sheet_name, engine='openpyxl')
            df.to_csv(processed_file_path, index=False)

            # Initialize an empty DataFrame to collect all chunks
            all_data = pd.DataFrame()

            # Read CSV in chunks
            for chunk in pd.read_csv(processed_file_path, chunksize=self.chunk_size):
                # Clean chunk (e.g., remove spaces from columns)
                chunk.columns = [col.strip() for col in chunk.columns]

                # Write chunk to the database
                chunk.to_sql(table_name, con=engine, if_exists='append', index=False)
                print(f"Processed a chunk with {len(chunk)} rows.")

                # Add chunk to the all_data DataFrame
                all_data = pd.concat([all_data, chunk], ignore_index=True)

            print(f"Data successfully loaded into table '{table_name}' in the database.")

        except Exception as e:
            print(f"Error loading data into the database: {e}")
            raise
