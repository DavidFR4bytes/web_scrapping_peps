import requests
import json
import time
import os
from bs4 import BeautifulSoup


def scrape_peps_cayman_api():
    base_url = "https://parliament.ky/members/"
    session = requests.Session()

    start_time = time.time()
    response = session.get(base_url)
    end_time = time.time()
    print("Iniciando scraping...")

    if response.status_code != 200:
        print(f"Error al acceder a la página: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    members_data = []
    members = soup.find_all("div", class_="member-select-main")

    for member in members:
        name = member.find("h1").get_text(strip=True)
        role = member.find("p").get_text(strip=True)
        district_tag = member.find_all("p", class_="change-add-to-cart-text")
        district = district_tag[0].get_text(strip=True) if len(district_tag) > 0 else "No disponible"
        image_tag = member.find("img")
        image_url = image_tag["src"] if image_tag else None

        members_data.append({
            "nombre": name,
            "cargo": role,
            "distrito": district,
            "imagen": image_url
        })

    # Guardar como JSON en carpeta data
    os.makedirs("data", exist_ok=True)
    with open("data/peps_caiman.json", "w", encoding="utf-8") as f:
        json.dump(members_data, f, ensure_ascii=False, indent=4)

    print(f"{len(members_data)} miembros del parlamento extraídos y guardados en data/peps_caiman.json")


def scrape_cayman_officials():
    peps = []

    # Lista de URLs de páginas que contienen oficiales judiciales
    urls = [
        "https://judicial.ky/chief-justice/",
        "https://judicial.ky/president-of-the-court-of-appeal/",
        "https://judicial.ky/court-of-appeal-judges/",
        "https://judicial.ky/grand-court-judges/",
        "https://judicial.ky/chief-magistrate/",
        "https://judicial.ky/magistrates/"
    ]

    for url in urls:
        print(f"Scrapeando: {url}")
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
        if response.status_code != 200:
            print(f"Error al acceder a {url}: {response.status_code}")
            continue

        soup = BeautifulSoup(response.content, "html.parser")

        # Buscar bloques con clase 'single-team-area'
        blocks = soup.select("div.single-team-area")
        for block in blocks:
            name_tag = block.select_one("span.team-name a")
            img_tag = block.select_one("figure img")
            bio_url = name_tag["href"] if name_tag else ""

            name = name_tag.get_text(strip=True) if name_tag else ""
            image = img_tag["src"] if img_tag and img_tag.has_attr("src") else ""

            peps.append({
                "nombre": name,
                "imagen": image,
                "url_biografia": bio_url,
                "pais": "Islas Caimán",
                "fuente": url
            })

    os.makedirs("data", exist_ok=True)
    with open("data/peps_islas_caiman.json", "w", encoding="utf-8") as f:
        json.dump(peps, f, ensure_ascii=False, indent=4)

    print(f"Se extrajeron {len(peps)} oficiales judiciales de las Islas Caimán.")
