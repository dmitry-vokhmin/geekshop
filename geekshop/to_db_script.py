import json
from pathlib import Path
import datetime as dt


def to_json(data, file_path):
    with open(file_path, "w") as f:
        json.dump(data, f)


if __name__ == '__main__':
    path = Path(__file__).parent.joinpath("mainapp/fixtures/data_to_db.json")
    data_to_db = [
        {"model": "mainapp.product",
         "pk": 1,
         "fields": {
             "name": "Стул повышенного качества",
             "image": "product_images/product-1.jpg",
             "short_desc": "Расположитесь комфортно",
             "price": 2000,
             "category_id": 1,
             "created": dt.datetime.now().isoformat(),
             "updated": dt.datetime.now().isoformat()
         }},
        {"model": "mainapp.product",
         "pk": 2,
         "fields": {
             "name": "Современная лампа",
             "image": "product_images/product-4-sm.jpg",
             "short_desc": "Комфорт превыше всего",
             "price": 1500,
             "category_id": 2,
             "created": dt.datetime.now().isoformat(),
             "updated": dt.datetime.now().isoformat()
         }},
        {"model": "mainapp.product",
         "pk": 3,
         "fields": {
             "name": "Стул повышенного качества",
             "image": "product_images/product-4.jpg",
             "short_desc": "Не оторваться",
             "price": 1500,
             "category_id": 1,
             "created": dt.datetime.now().isoformat(),
             "updated": dt.datetime.now().isoformat()
         }},
        {"model": "mainapp.product",
         "pk": 4,
         "fields": {
             "name": "Диван повышенного качества",
             "image": "product_images/product-3-sm.jpg",
             "short_desc": "Не оторваться",
             "price": 15000,
             "category_id": 1,
             "created": dt.datetime.now().isoformat(),
             "updated": dt.datetime.now().isoformat()
         }}
    ]
    to_json(data_to_db, path)
