import requests
from pathlib import Path

def download_image(url: str, save_path: Path):
    try:
        response = requests.get(url, stream=True)
        if response.status_code != 200:
            return False
        with open(save_path, mode="wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        return True
    except Exception as e:
        return f"Что-то не так {e}"