import requests
from bs4 import BeautifulSoup
import json
import os
import urllib.parse

def scrape_peps_estonia_api():
    base_url = "https://www.riigikogu.ee"
    members_url = f"{base_url}/en/parliament-of-estonia/composition/members-riigikogu/"
    response = requests.get(members_url)
    if response.status_code != 200:
        print(f"Error al acceder a la página: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    members = []

    # Buscar todos los elementos que contienen información de los miembros
    member_items = soup.find_all("li", class_="item")

    for item in member_items:
        member = {}

        # Extraer el nombre y el enlace al perfil
        name_tag = item.find("h3")
        if name_tag and name_tag.a:
            member["nombre"] = name_tag.a.get_text(strip=True)
            member["perfil_url"] = name_tag.a["href"]
        else:
            member["nombre"] = None
            member["perfil_url"] = None

        # Extraer la URL de la foto
        photo_tag = item.find("p", class_="photo")
        if photo_tag and photo_tag.a and photo_tag.a.img:
            img_src = photo_tag.a.img.get("data-original") or photo_tag.a.img.get("src")
            member["foto"] = urllib.parse.urljoin(base_url, img_src)
        else:
            member["foto"] = None

        # Extraer la información adicional (partido, correo, comités)
        content_div = item.find("div", class_="content")
        if content_div:
            info_items = content_div.find_all("li")
            for info in info_items:
                text = info.get_text(strip=True)
                # Identificar el correo electrónico
                if "@" in text:
                    member["correo"] = text
                # Identificar el partido político
                elif "Parliamentary Group" in text or "Non-affiliated members" in text:
                    member["partido"] = text
                # Identificar los comités
                elif "Committee" in text:
                    member.setdefault("comites", []).append(text)

        members.append(member)

    # Guardar los datos en un archivo JSON
    output_path = os.path.join("data", "peps_estonia.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(members, f, ensure_ascii=False, indent=4)

    print(f"Datos guardados en: {output_path}")

if __name__ == "__main__":
    scrape_peps_estonia_api()
