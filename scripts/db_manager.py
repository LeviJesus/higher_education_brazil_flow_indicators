import sqlite3
from pathlib import Path

class DatabaseManager:
    def __init__(self, db_path="data/database.db"):
        self.db_path = Path(db_path)
        self.connection = None

    def connect(self):
        """Connect to the SQLite database."""
        self.connection = sqlite3.connect(self.db_path)
        return self.connection

    def create_table(self, table_name, schema):
        """Create a table if it does not exist."""
        try:
            with self.connection:
                self.connection.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({schema})")
                print(f"Table '{table_name}' is ready.")
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            print("Database connection closed.")
