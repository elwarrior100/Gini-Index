import sqlite3
import logging

class CensusData:
    def __init__(self, state, gini_index):
        self.state = state
        self.gini_index = gini_index

class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.create_table()
    
    def create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS census_data (
                    id INTEGER PRIMARY KEY,
                    state TEXT,
                    gini_index REAL
                )
            """)
    
    def insert_data(self, census_data_list):
        with self.conn:
            for census_data in census_data_list:
                try:
                    self.conn.execute("""
                        INSERT INTO census_data (state, gini_index) VALUES (?, ?)
                    """, (census_data.state, census_data.gini_index))
                    logging.info(f"Inserted: {census_data.state}, Gini Index: {census_data.gini_index}")
                except Exception as e:
                    logging.error(f"Error inserting {census_data.state}: {e}") 

    def query_data(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM census_data")
        return cursor.fetchall()
    
    def close(self):
        if self.conn:
            self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()