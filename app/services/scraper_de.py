import requests
import json
import os

def scrape_peps_alemania_api():
    url_json = "https://www.abgeordnetenwatch.de/api/v2/candidacies-mandates?type=mandate"

    print("Descargando archivo JSON...")
    response = requests.get(url_json)
    data = response.json()

    data = data["data"]

    os.makedirs("data", exist_ok=True)
    with open("data/peps_alemania.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print("Datos guardados exitosamente en data/peps_alemania.json")