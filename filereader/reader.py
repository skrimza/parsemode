import pandas as pd
from json import dump, load

class WorkFrame:
    
    def __init__(self, excel_path="article.xlsx"):
        self.excel_path = excel_path
        self.frame = pd.read_excel(
            io=self.excel_path,
            header=0
        )

class FrameJson(WorkFrame):
    
    def from_excel(self, json_path="article.json"):
        try:
            with open(file=json_path, mode="w", encoding="utf-8") as json_file:
                data = self.frame.to_dict()
                for articles in data.values():
                    new_dict = {"articles": list(articles.values())}
                    dump(
                        obj=new_dict,
                        fp=json_file,
                        ensure_ascii=False,
                        indent=4
                    )
            return True
        except Exception as e:
            raise

    def read_json(self, json_path="article.json"):
        try:
            with open(file=json_path, mode="r", encoding="utf-8") as json_file:
                data = load(json_file)
            return data
        except Exception as e:
            raise

