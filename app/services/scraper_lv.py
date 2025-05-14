import requests
from bs4 import BeautifulSoup
import json
import re
import os

def scrape_peps_latvia_api():
    url = "https://titania.saeima.lv/personal/deputati/saeima14_depweb_public.nsf/deputies?OpenView&lang=EN&count=1000"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    script_data = soup.find("div", {"id": "viewHolderText"})
    if not script_data:
        print("No se encontró el div con los datos.")
        return

    text = script_data.get_text()

    pattern = r"drawDep\(\{(.*?)\}\);"
    matches = re.findall(pattern, text, re.DOTALL)

    peps = []
    for match in matches:
        js_object = "{" + match + "}"

        # Convertir claves JS sin comillas a JSON válido (poner comillas a las claves)
        js_object_cleaned = re.sub(r"(\w+):", r'"\1":', js_object)

        try:
            pep_data = json.loads(js_object_cleaned)
            peps.append({
                "name": pep_data.get("name", ""),
                "surname": pep_data.get("sname", ""),
                "parliamentary_group": pep_data.get("lst", ""),
                "profile_url": f"https://titania.saeima.lv/personal/deputati/saeima14_depweb_public.nsf/depArchive.html?ReadForm&unid={pep_data.get('unid')}&url=./0/{pep_data.get('unid')}?OpenDocument&lang=EN"
            })
        except json.JSONDecodeError as e:
            print(f"Error al decodificar JSON: {e}")
            print("Entrada problemática:", js_object_cleaned)

    # Guardar resultados
    os.makedirs("data", exist_ok=True)
    with open("data/peps_latvia.json", "w", encoding="utf-8") as f:
        json.dump(peps, f, ensure_ascii=False, indent=4)

    print(f"{len(peps)} PEPs extraídas y guardadas en data/peps_latvia.json")
