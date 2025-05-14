import requests
import json
import os
import urllib3



def scrape_peps_south_africa_municipal_leaders_api():
    url = "https://municipaldata.treasury.gov.za/api/cubes/officials/facts"

    response = requests.get(url)

    if response.status_code == 200:
        peps = response.json()
        peps = peps['data']

    else:
        print(f"Error al obtener los datos. Código de estado: {response.status_code}")
        return

    os.makedirs("data", exist_ok=True)
    with open("data/peps_south_africa_municipal_leaders.json", "w", encoding="utf-8") as f:
        json.dump(peps, f, ensure_ascii=False, indent=4)

    print(f"{len(peps)} PEPs guardadas en data/peps_south_africa_municipal_leaders.json")



def scraper_peps_south_africa_provincial_legislators_api():
    url = "https://pa.org.za/media_root/popolo_json/pombola.json"

    response = requests.get(url)

    if response.status_code == 200:
        peps = response.json()

    else:
        print(f"Error al obtener los datos. Código de estado: {response.status_code}")
        return

    os.makedirs("data", exist_ok=True)
    with open("data/peps_south_africa_provincial_legislators.json", "w", encoding="utf-8") as f:
        json.dump(peps, f, ensure_ascii=False, indent=4)

    print("PEPs guardadas en data/peps_south_africa_provincial_legislators.json")