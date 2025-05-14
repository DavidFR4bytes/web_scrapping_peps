import requests
import os
import json
import csv
import io
from bs4 import BeautifulSoup


api_key = "pZd398hNyauFtpgVzIjyaBLHkzUmQIZ7ZpHH05RF"


def scrape_peps_usa_plum_api():
    csv_url = "https://escs.opm.gov/escs-net/api/pbpub/download-data"
    print("Descargando archivo CSV...")

    response = requests.get(csv_url)
    if response.status_code != 200:
        print(f"Error al descargar el archivo: {response.status_code}")
        return

    csv_reader = csv.DictReader(io.StringIO(response.content.decode("utf-8")), delimiter=',')
    pep_data = []

    for row in csv_reader:
        pep = {
            "agency_name": row.get("AgencyName", ""),
            "organization_name": row.get("OrganizationName", ""),
            "position_title": row.get("PositionTitle", ""),
            "position_status": row.get("PositionStatus", ""),
            "appointment_type_description": row.get("AppointmentTypeDescription", ""),
            "expiration_date": row.get("ExpirationDate", ""),
            "level_grade_pay": row.get("LevelGradePay", ""),
            "location": row.get("Location", ""),
            "incumbent_first_name": row.get("IncumbentFirstName", ""),
            "incumbent_last_name": row.get("IncumbentLastName", ""),
            "payment_plan_description": row.get("PaymentPlanDescription", ""),
            "tenure": row.get("Tenure", ""),
        }
        pep_data.append(pep)

    os.makedirs("data", exist_ok=True)
    with open("data/peps_usa_plum.json", "w", encoding="utf-8") as f:
        json.dump(pep_data, f, ensure_ascii=False, indent=4)

    print("Scraping de PEPs de USA Plum completado.")


def scrape_peps_usa_cia_world_liders_api():
    url_json = "https://www.cia.gov/resources/world-leaders/page-data/sq/d/3338022342.json"
    print("Descargando archivo JSON...")

    response = requests.get(url_json)
    if response.status_code != 200:
        print(f"Error al descargar el archivo: {response.status_code}")
        return

    data = response.json()
    data = data["data"]

    os.makedirs("data", exist_ok=True)
    with open("data/peps_usa_cia_world_liders.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print("Scraping de PEPs de USA CIA World Leaders completado.")


def scrape_peps_usa_members_congress_api():
    url_json = f"https://api.congress.gov/v3/member?api_key={api_key}"
    print("Descargando archivo JSON...")

    response = requests.get(url_json)
    if response.status_code != 200:
        print(f"Error al descargar el archivo: {response.status_code}")
        return

    data = response.json()
    data = data["members"]

    os.makedirs("data", exist_ok=True)
    with open("data/peps_usa_members_congress.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print("Scraping de PEPs de USA Members Congress completado.")


def scrape_peps_us_navy_leadership_api():
    url = "https://www.navy.mil/Leadership/"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code != 200:
        print(f"Error al acceder a la página: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, "html.parser")
    peps = []

    # Buscar todos los bloques de miembros (divs que contienen la clase 'row' con estructura conocida)
    for row in soup.find_all("div", class_="row"):
        name_tag = row.find("h1")
        position_tag = row.find("h3")
        bio_tag = row.find("p", class_="bio-sum")
        img_tag = row.find("img")
        bio_link_tag = row.find("a", href=True)

        if name_tag and position_tag and bio_tag:
            nombre = name_tag.get_text(strip=True)
            cargo = position_tag.get_text(strip=True)
            biografia_resumen = bio_tag.get_text(strip=True) if bio_tag else ""
            imagen = img_tag["src"] if img_tag and "src" in img_tag.attrs else ""
            url_biografia = "https://www.navy.mil" + bio_link_tag["href"] if bio_link_tag["href"].startswith("/") else bio_link_tag["href"]

            peps.append({
                "nombre": nombre,
                "cargo": cargo,
                "biografia_resumen": biografia_resumen,
                "imagen": imagen,
                "url_biografia": url_biografia
            })

    # Guardar en archivo JSON
    os.makedirs("data", exist_ok=True)
    with open("data/peps_us_navy.json", "w", encoding="utf-8") as f:
        json.dump(peps, f, ensure_ascii=False, indent=4)

    print(f"Se extrajeron {len(peps)} PEPs de la Marina de EE.UU. y se guardaron en 'data/peps_us_navy.json'.")


def scrape_peps_us_state_department_api():
    initial_url = "https://www.state.gov/biographies-list/"
    base_url = "https://www.state.gov/biographies-list/page/{}/"
    page = 0
    peps = []

    while True:
        print(f"Scrapeando página {page}...")
        url = base_url.format(page)

        if page == 0:
            url = initial_url
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
        if response.status_code != 200:
            print(f"Error al acceder a la página {page}: {response.status_code}")
            break

        soup = BeautifulSoup(response.content, "html.parser")
        items = soup.select("li.collection-result--biography")

        # Si no hay elementos, hemos llegado al final
        if not items:
            print("No se encontraron más resultados.")
            break

        for item in items:
            nombre_tag = item.select_one(".biography-collection__link span")
            cargo_tags = item.select(".biography-collection__description")
            imagen_tag = item.find("img")
            link_tag = item.find("a", class_="biography-collection__link")

            nombre = nombre_tag.get_text(strip=True) if nombre_tag else ""
            cargo = cargo_tags[0].get_text(strip=True) if len(cargo_tags) > 0 else ""
            oficina = cargo_tags[1].get_text(strip=True) if len(cargo_tags) > 1 else ""
            imagen = imagen_tag["src"] if imagen_tag else ""
            url_biografia = link_tag["href"] if link_tag else ""

            peps.append({
                "nombre": nombre,
                "cargo": cargo,
                "oficina": oficina,
                "imagen": imagen,
                "url_biografia": url_biografia
            })

        page += 1

    # Guardar en JSON
    os.makedirs("data", exist_ok=True)
    with open("data/peps_usa_state_department.json", "w", encoding="utf-8") as f:
        json.dump(peps, f, ensure_ascii=False, indent=4)

    print(f"Se extrajeron {len(peps)} registros de funcionarios del Departamento de Estado de EE. UU.")
