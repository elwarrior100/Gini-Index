import os
import requests
from bs4 import BeautifulSoup

class WebScrapper:
    
    def __init__(self,url):
        self.url=url
    
    def fetch_html(self):
        """Fetch data of the given URL in the initialization of WebScrapper class"""
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error in fetching process {self.url}: {e}")
            return None
        
    def parse_html(self, html):

        """Used to parse the HTML content for easier finding of the ZIP file link"""
        soup = BeautifulSoup(html, 'html.parser')

        #Return the hyperlinks on the page that end with '.zip'
        zip_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.zip')]

        return{"zip_links": zip_links}
    
    def download_zip(self,zip_url,download_folder="data"):
        """Download the ZIP file and save it to the specified folder."""
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

        file_name = zip_url.split("/")[-1]
        download_path = os.path.join(download_folder, file_name)

        try:
            print(f"Downloading {file_name} from {zip_url}...")
            response = requests.get(zip_url)
            response.raise_for_status()

            with open(download_path, 'wb') as file:
                file.write(response.content)

            print(f"Downloaded and saved to {download_path}.")
        except requests.RequestException as e:
            print(f"Error downloading {zip_url}: {e}")

    def scrape(self):
        html = self.fetch_html()
        
        if html:
            data = self.parse_html(html)
            zip_links = data["zip_links"]
        
            print(f"Found {len(zip_links)} ZIP file(s):")
            for link in zip_links:
                if not link.startswith("http"):
                    link = self.url + link
                print(f"Downloading {link}...")
                self.download_zip(link)
        else:
            print("Failed to retrieve or parse HTML.")



