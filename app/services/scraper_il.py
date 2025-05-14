import requests
from bs4 import BeautifulSoup
import json
import os


def scrape_peps_israel_api():
    url_json = "https://knesset.gov.il/WebSiteApi/knessetapi/MKs/GetMksDropdown?languageKey=en"

    print("Descargando archivo JSON...")
    response = requests.get(url_json)
    data = response.json()

    os.makedirs("data", exist_ok=True)
    with open("data/peps_israel.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print("Datos guardados exitosamente en data/peps_israel.json")