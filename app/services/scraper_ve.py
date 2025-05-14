import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_peps_venezuela():
    base_url = "https://www.asambleanacional.gob.ve/diputados?page={}"
    page = 1
    peps = []
    nombres_anteriores = set()

    while True:
        print(f"Scrapeando página {page}...")
        url = base_url.format(page)

        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
        if response.status_code != 200:
            print(f"Error al acceder a la página {page}: {response.status_code}")
            break

        soup = BeautifulSoup(response.content, "html.parser")
        items = soup.select("div.uk-padding-small")

        if not items:
            print("No se encontraron más resultados.")
            break

        nuevos = 0

        for item in items:
            nombre_tag = item.select_one("div.text-diputado-slider b a")
            partido_tag = item.select_one("div.text-diputado-slider small:nth-of-type(1) b")
            estado_tag = item.select_one("div.text-diputado-slider small:nth-of-type(2)")
            imagen_tag = item.select_one("div.uk-background-cover")

            nombre = nombre_tag.get_text(strip=True) if nombre_tag else ""
            if nombre in nombres_anteriores:
                continue

            partido = partido_tag.get_text(strip=True) if partido_tag else ""
            estado = estado_tag.get_text(strip=True).replace("Estado:", "").strip() if estado_tag else ""
            url_biografia = nombre_tag["href"] if nombre_tag else ""

            imagen = ""
            if imagen_tag:
                imagen_style = imagen_tag.get("style", "")
                if "background-image:" in imagen_style:
                    imagen = imagen_style.split("url(")[-1].split(")")[0].strip()

            peps.append({
                "nombre": nombre,
                "partido": partido,
                "estado": estado,
                "imagen": imagen,
                "url_biografia": url_biografia
            })

            nombres_anteriores.add(nombre)
            nuevos += 1

        if nuevos == 0:
            print("No se encontraron nuevos diputados. Fin del scraping.")
            break

        page += 1

    os.makedirs("data", exist_ok=True)
    with open("data/peps_venezuela.json", "w", encoding="utf-8") as f:
        json.dump(peps, f, ensure_ascii=False, indent=4)

    print(f"Se extrajeron {len(peps)} registros de diputados de Venezuela.")

if __name__ == "__main__":
    scrape_peps_venezuela()
