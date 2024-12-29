import os
import requests
import zipfile

class DataDownloader:
    def __init__(self, url, download_path="data/raw", extract_path="data/raw"):
        self.url = url
        self.download_path = os.path.join(download_path, "dataset.zip")
        self.extract_path = extract_path

    def download(self):
        """Baixar o conjunto de dados da URL fornecida."""
        os.makedirs(os.path.dirname(self.download_path), exist_ok=True)
        try:
            response = requests.get(self.url, stream=True)
            response.raise_for_status()
            with open(self.download_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"Arquivo baixado para {self.download_path}")
        except requests.RequestException as e:
            print(f"Falha ao baixar: {e}")
            raise

    def extract(self):
        """Extrair o arquivo ZIP baixado."""
        os.makedirs(self.extract_path, exist_ok=True)
        try:
            with zipfile.ZipFile(self.download_path, 'r') as zip_ref:
                zip_ref.extractall(self.extract_path)
            print(f"Arquivos extraídos para {self.extract_path}")
        except zipfile.BadZipFile as e:
            print(f"Falha na extração: {e}")
            raise
