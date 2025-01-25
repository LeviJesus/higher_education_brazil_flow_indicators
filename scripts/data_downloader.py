import os
import requests
import zipfile

class DataDownloader:
    def __init__(self, url, download_path="data/raw", extract_path="data/raw"):
        self.url = url
        self.download_path = os.path.join(download_path, "dataset.zip")
        self.extract_path = extract_path

    def download(self):
        """Download the dataset from the provided URL."""
        os.makedirs(os.path.dirname(self.download_path), exist_ok=True)
        try:
            response = requests.get(self.url, stream=True)
            response.raise_for_status()
            with open(self.download_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"File downloaded to {self.download_path}")
        except requests.RequestException as e:
            print(f"Failed to download: {e}")
            raise

    def extract(self):
        """Extract the downloaded ZIP file."""
        os.makedirs(self.extract_path, exist_ok=True)
        try:
            with zipfile.ZipFile(self.download_path, 'r') as zip_ref:
                zip_ref.extractall(self.extract_path)
            print(f"Files extracted to {self.extract_path}")
        except zipfile.BadZipFile as e:
            print(f"Extraction failed: {e}")
            raise
