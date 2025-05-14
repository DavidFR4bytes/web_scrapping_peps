import requests
from bs4 import BeautifulSoup
import json
import os

BASE_URL = "https://www.tweedekamer.nl"
LIST_URL = BASE_URL + "/kamerleden_en_commissies/alle_kamerleden"

def scrape_peps_netherlands():
    response = requests.get(LIST_URL, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, "html.parser")
    cards = soup.select("div.u-member-card-height")

    peps = []
    for card in cards:
        # Nombre y link
        name_tag = card.select_one("h3 a")
        nombre = name_tag.get_text(strip=True) if name_tag else ""
        url_biografia = BASE_URL + name_tag["href"] if name_tag and name_tag.has_attr("href") else ""

        # Partido
        partido_tag = card.select_one("span.u-text-sm.u-text-primary")
        partido = partido_tag.get_text(strip=True) if partido_tag else ""

        # Imagen
        img_tag = card.select_one("img.m-avatar__image")
        imagen = BASE_URL + img_tag["src"] if img_tag and img_tag.has_attr("src") else ""

        # Datos adicionales
        table = card.select_one("table")
        ciudad, edad, antiguedad = "", "", ""
        if table:
            rows = table.find_all("tr")
            for row in rows:
                th = row.find("th")
                td = row.find("td")
                if th and td:
                    campo = th.get_text(strip=True).lower()
                    valor = td.get_text(strip=True)
                    if "woonplaats" in campo:
                        ciudad = valor
                    elif "leeftijd" in campo:
                        edad = valor
                    elif "anciënniteit" in campo or "ancienniteit" in campo:
                        antiguedad = valor

        peps.append({
            "nombre": nombre,
            "partido": partido,
            "ciudad": ciudad,
            "edad": edad,
            "antiguedad": antiguedad,
            "imagen": imagen,
            "url_biografia": url_biografia,
            "pais": "Países Bajos",
            "fuente": LIST_URL
        })

    os.makedirs("data", exist_ok=True)
    with open("data/peps_paises_bajos.json", "w", encoding="utf-8") as f:
        json.dump(peps, f, ensure_ascii=False, indent=4)

    print(f"Se extrajeron {len(peps)} PEPs de Países Bajos.")

if __name__ == "__main__":
    scrape_peps_netherlands()
