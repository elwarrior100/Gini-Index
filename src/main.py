from src.census_processor import CensusProcessor
from src.scraper import WebScrapper


def main():
    url = "https://ftp.ibge.gov.br/Censos/Censo_Demografico_1991/Indice_de_Gini/"
    scraper = WebScrapper(url)
    scraper.scrape()
    folder_path = 'data'  
    db_name = 'census.db'
    processor = CensusProcessor(folder_path, db_name)
    processor.process_files()


if __name__ == '__main__':
    main()
    
