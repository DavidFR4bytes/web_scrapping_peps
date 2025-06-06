import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_peps_lithuania_api():
    url = "https://www.lrs.lt/sip/portal.show?p_r=35299&p_k=2"  # Página que contiene las PEPs
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    peps = []

    members = soup.find_all("div", class_="list-member")
    for member in members:
        name_tag = member.find("a", class_="smn-name link")
        surname_tag = name_tag.find("span", class_="smn-pavarde") if name_tag else None
        group_tag = member.find("a", class_="smn-frakcija link")

        if name_tag and surname_tag and group_tag:
            # Extraer nombre y apellido
            full_name = name_tag.get_text(separator=" ", strip=True)
            surname = surname_tag.get_text(strip=True)
            name = full_name.replace(surname, "").strip()

            # Enlace al perfil
            profile_url = name_tag.get("href")
            if profile_url and not profile_url.startswith("http"):
                profile_url = "https://www.lrs.lt" + profile_url

            peps.append({
                "name": name,
                "surname": surname,
                "parliamentary_group": group_tag.get_text(strip=True),
                "profile_url": profile_url
            })

    # Guardar en archivo JSON
    os.makedirs("data", exist_ok=True)
    with open("data/peps_lithuania.json", "w", encoding="utf-8") as f:
        json.dump(peps, f, ensure_ascii=False, indent=4)

    print(f"{len(peps)} PEPs extraídas y guardadas en data/peps_lithuania.json")

def get_declaration(id_num):
    guest_id = 9179496
    url = f"https://pinreg.vtek.lt/external/deklaracijos/{id_num:06d}/perziura/viesa"
    headers = {
        "Accept": "application/json",
        "Referer": f"https://pinreg.vtek.lt/app/pid-perziura/{id_num:06d}",
    }
    params = {
        "v": f"c{guest_id}"
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.json()

# Prueba con un ID de ejemplo
data = get_declaration(301730)
print(data)
