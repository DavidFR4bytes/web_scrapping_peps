import requests
import json
import time
import os
from bs4 import BeautifulSoup

def scrape_peps_austria_api():
    URL = "https://www.meineabgeordneten.at/Abgeordnete"
    session = requests.Session()

    start_time = time.time()
    response = session.get(URL)
    end_time = time.time()
    print("Iniciando scraping...")

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        people_divs = soup.find_all("div", class_="abgeordneter row")

        pep_data = []

        for person in people_divs:
            # Imagen
            img_tag = person.find("img")
            img_url = "https://www.meineabgeordneten.at" + img_tag["src"] if img_tag else ""

            # Nombre y enlace
            a_tag = person.find("a")
            profile_url = a_tag["href"] if a_tag else ""
            full_name = a_tag.get_text(strip=True).split(",")[0] if a_tag else ""

            # Cargo
            subtitle = person.find("div", class_="untertitel")
            position = subtitle.get_text(strip=True) if subtitle else ""

            pep_data.append({
                "fullName": full_name,
                "profileURL": profile_url,
                "position": position,
                "imageURL": img_url
            })

        # Guardar los datos
        os.makedirs("data", exist_ok=True)
        with open("data/peps_austria.json", "w", encoding="utf-8") as f:
            json.dump(pep_data, f, ensure_ascii=False, indent=4)

        print(f"Scraping completado en {end_time - start_time:.2f} segundos. {len(pep_data)} personas guardadas.")
    else:
        print(f"Error al hacer la petición: {response.status_code}")

if __name__ == "__main__":
    scrape_peps_austria_api()
