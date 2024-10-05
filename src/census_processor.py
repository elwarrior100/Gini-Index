import os
import logging
import pandas as pd
import zipfile

from src.database_manager import CensusData, DatabaseManager

class CensusProcessor:

    def __init__(self, folder_path, db_name):
        self.folder_path = folder_path
        self.db_manager = DatabaseManager(db_name)

    def process_files(self):
        for file_name in os.listdir(self.folder_path):
            file_path = os.path.join(self.folder_path, file_name)
            if file_name.endswith('.zip'):
                logging.info(f'Processing file: {file_path}')
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    extracted_files = zip_ref.namelist()
                    logging.info(f'Extracted files: {extracted_files}')
                    self.handle_extracted_files(zip_ref, extracted_files)
    
    def handle_extracted_files(self, zip_ref, extracted_files):
        for extracted_file in extracted_files:
            if extracted_file.endswith('.XLS'):
                with zip_ref.open(extracted_file) as xls_file:
                    df = pd.read_excel(xls_file, header=None)
                    logging.info(f'DataFrame from {extracted_file}:\n{df}')
                    self.extract_and_insert_data(df)

    def extract_and_insert_data(self, df):
        census_data_list = []
        
        for index, row in df.iterrows():
            if index == 0:  # Skip header
                continue
            
            state = self.clean_state(row[0])
            if state == 'Brasil':
                logging.info(f'Skipping state: {state}')
                continue

            gini_index = row[1]

            if not self.is_valid_gini_index(gini_index):
                logging.warning(f'Skipping invalid Gini index for state: {state}')
                continue

            gini_index = float(gini_index)  
            
            census_data_list.append(CensusData(state, gini_index))
            logging.info(f'Extracted: {state}, Gini Index: {gini_index}')

        logging.info(f'Parsed data count: {len(census_data_list)}')
        self.db_manager.insert_data(census_data_list)

    def clean_state(self, state):
        if isinstance(state, (float, int)):
            return str(state)
        elif isinstance(state, str):
            return state.strip()
        return state

    def is_valid_gini_index(self, gini_index):
        try:
            float(gini_index)
            return True
        except (ValueError, TypeError):
            return False

