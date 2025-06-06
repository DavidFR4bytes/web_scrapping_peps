import requests
import json
import os
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def scrape_peps_montenegro_api():
    url = "https://obsidian.antikorupcija.me/api/ask-interni-pretraga/ank-izvjestaj-imovine/pretraga-izvjestaj-imovine-javni"

    response = requests.get(url, verify=False)

    if response.status_code == 200:
        peps = response.json()
    else:
        print(f"Error al obtener los datos. Código de estado: {response.status_code}")
        return

    os.makedirs("data", exist_ok=True)
    with open("data/peps_montenegro.json", "w", encoding="utf-8") as f:
        json.dump(peps, f, ensure_ascii=False, indent=4)

    print(f"{len(peps)} PEPs guardadas en data/peps_montenegro.json")
