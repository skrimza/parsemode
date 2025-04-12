import requests
from pathlib import Path

def download_image(url: str):
    try:
        with open("my_products.json", "r", encoding="utf-8") as file:
            load(file)
        response = requests.get(url, stream=True)
        if response.status_code != 200:
            return False
        with open(Path("media/product_images"), mode="wb", encoding="utf-8") as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        return True
    except Exception as e:
        return f"Что-то не так {e}"