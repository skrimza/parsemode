import requests
from json import load, dump
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from filereader.reader import FrameJson
# from utils import download_image


class Parser:
    
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        }

    def parse_product(self):
        list_art = list(*FrameJson().read_json().values())
        all_product_info = {}
        try:
            for article in list_art:
                url = f"https://st1.by/"
                data_files = requests.get(
                    url=f"{url}catalog/",
                    headers=self.headers,
                    params={
                        "q": str(article),
                        "how": "r"
                    },
                    timeout=5
                )
                if data_files.status_code == 200:
                    selected_product = BeautifulSoup(data_files.text, "html.parser")
                    link_product = selected_product.find_all('a', class_="thumb")
                    if not link_product:
                        continue
                    all_product_info[article] = None
                    product_url = urljoin(url, link_product[0]["href"])
                    product_page = requests.get(
                        product_url, 
                        headers=self.headers,
                        timeout=5
                    )
                    if product_page.status_code == 200:
                        all_information = {
                            "list_images": [],
                            "price": None,
                            "local_images": []
                        }
                        about_product = BeautifulSoup(product_page.text, "html.parser")
                        product_price = about_product.find("span", class_="price_value")
                        if not product_price:
                            all_information["price"] = None
                        else:
                            all_information["price"] = product_price.text.strip()
                        all_images = about_product.find_all(
                            "img", 
                            class_="detail-gallery-big__picture"
                        )
                        for i, img in enumerate(all_images):
                            if "data-src" in img.attrs and img["data-src"]:
                                image_url = urljoin(url, img["data-src"])
                            elif "src" in img.attrs and img["src"] and not img["src"].startswith("data:image"):
                                image_url = urljoin(url, img["src"])
                            all_information["list_images"].append(image_url)
                    else:
                        pass
                    all_product_info[article] = all_information
                else:
                    pass
                # with open("my_products.json", "w", encoding="utf-8") as my_file:
                #     dump(
                #         obj=all_product_info,
                #         fp=my_file,
                #         ensure_ascii=False,
                #         indent=4
                #     )
        except Exception as e:
            return f"false {e}"
