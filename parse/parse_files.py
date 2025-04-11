import selenium
import selenium.webdriver
import selenium.webdriver.firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import selenium.webdriver.firefox.service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from pathlib import Path
from json import load
from utils.downloader import download_image


class Parser:
    def __init__(self):
        self.firefox_options = Options()
        self.firefox_options.add_argument("--headless")
        self.driver = selenium.webdriver.Firefox(
            service=selenium.webdriver.firefox.service.Service(GeckoDriverManager().install()),
            options=self.firefox_options
        )
        self.image_dir = Path("media/product_images")
        self.image_dir.mkdir(parents=True, exist_ok=True)

    def __del__(self):
        self.driver.quit()

    def parse_product(self, article: str):
        try:
            url = f"https://st1.by/catalog/?q={article}"
            self.driver.get(url)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "product-details"))
            )
            product_name = self.driver.find_element(By.CLASS_NAME, "product-name").text
            image_url = self.driver.find_element(By.CLASS_NAME, "product-image").get_attribute("src")
            image_path = self.image_dir / f"{article}.jpg"
            success = download_image(image_url, image_path)
            if not success:
                raise Exception(f"Не удалось скачать изображение для артикула {article}")

            return {
                "article": article,
                "name": product_name,
                "image_path": str(image_path)
            }
        except Exception as e:
            return None

    def parser_data(self, json_path="article.json"):
        try:
            with open(file=json_path, mode="r", encoding="utf-8") as json_file:
                articles_data = load(json_file)
            articles = [data["article"] for data in articles_data.values() if "article" in data]
            if len(articles) != 100:
                raise ValueError(f"Ожидалось 100 артикулов, но найдено {len(articles)}")
            results = []
            for article in articles:
                result = self.parse_product(article)
                if result:
                    results.append(result)
            return results
        except Exception as e:
            return []