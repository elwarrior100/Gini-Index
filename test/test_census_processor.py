import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import sqlite3
import tempfile
from src.census_processor import CensusProcessor
from src.database_manager import DatabaseManager, CensusData
from src.scraper import WebScrapper

class TestCensusProcessor(unittest.TestCase):
    def setUp(self):

        self.test_dir = tempfile.TemporaryDirectory()
        self.test_db = os.path.join(self.test_dir.name, 'test_census.db')
        self.processor = CensusProcessor(folder_path='dummy_path', db_name='dummy_db')

    def tearDown(self):
        self.test_dir.cleanup()

    @patch('os.listdir', return_value=['test.zip'])
    @patch('zipfile.ZipFile')
    @patch('pandas.read_excel')
    def test_process_files(self, mock_read_excel, mock_zipfile, mock_listdir):

        mock_zip = mock_zipfile.return_value.__enter__.return_value
        mock_zip.namelist.return_value = ['test.XLS']

        mock_df = MagicMock()
        mock_df.iterrows.return_value = iter([
            (0, ["Header", "Value"]),
            (1, ["Brasil", "0.35"]),
            (2, ["Acre", "zero"]),
            (3, ["...", "zero"]),
            (4, ["Resende", "0.45"]),
        ])
        mock_read_excel.return_value = mock_df

        processor = CensusProcessor(self.test_dir.name, self.test_db)
        processor.process_files()

        with sqlite3.connect(self.test_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT state, gini_index FROM census_data")
            results = cursor.fetchall()
        
        self.assertEqual(len(results), 1)
        self.assertIn(('Resende', 0.45), results)

    def test_clean_state_with_int(self):
        result = self.processor.clean_state(123)
        self.assertEqual(result, "123")

    def test_clean_state_with_string(self):
        result = self.processor.clean_state("  Viseu  ")
        self.assertEqual(result, "Viseu")

    def test_insert_data(self):
        db_manager = DatabaseManager(self.test_db)

        data_list = [CensusData('Anreade', 0.25), CensusData('Rendufe', 0.40)]
        db_manager.insert_data(data_list)
        results = db_manager.query_data()
        
        self.assertEqual(len(results), 2)
        self.assertIn(('Anreade', 0.25), [(row[1], row[2]) for row in results])
        self.assertIn(('Rendufe', 0.40), [(row[1], row[2]) for row in results])

        db_manager.close()

class TestWebScrapper(unittest.TestCase):
    @patch('requests.get')
    def test_fetch_html(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = "<html><body>Test HTML</body></html>"
        mock_get.return_value = mock_response

        scraper = WebScrapper("http://example.com")
        result = scraper.fetch_html()
        
        self.assertEqual(result, "<html><body>Test HTML</body></html>")
    
    def test_parse_html(self):
        html = """
        <html>
            <body>
                <a href="file1.zip">Download file1</a>
                <a href="file2.zip">Download file2</a>
                <a href="otherfile.txt">Other file</a>
            </body>
        </html>
        """
        scraper = WebScrapper("http://example.com")
        result = scraper.parse_html(html)
        
        self.assertEqual(result, {"zip_links": ["file1.zip", "file2.zip"]})
    
    @patch('requests.get')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.makedirs')
    def test_download_zip(self, mock_makedirs, mock_open_file, mock_get):

        mock_response = MagicMock()
        mock_response.content = b'Test Content'
        mock_get.return_value = mock_response

        scraper = WebScrapper("http://example.com/file.zip")
        scraper.download_zip("http://example.com/file.zip", download_folder="test_folder")

        mock_open_file.assert_called_once_with(os.path.join("test_folder", "file.zip"), 'wb')
        mock_open_file().write.assert_called_once_with(b'Test Content')

if __name__ == '__main__':
    unittest.main()
