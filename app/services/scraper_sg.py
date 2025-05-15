import json
import os

import aiohttp
import asyncio
import ssl
from bs4 import BeautifulSoup

# URL base
BASE_URL = "https://www.sgdi.gov.sg"

# Crear un contexto SSL que no verifica (solo para pruebas)
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


# Paso 1: Obtener todos los links de organizaciones
async def get_organization_links(session):
    org_links = []
    url = f"{BASE_URL}/statutory-boards"
    async with session.get(url, ssl=ssl_context) as resp:
        html = await resp.text()
        soup = BeautifulSoup(html, "html.parser")
        ministries_list = soup.find("ul", class_="ministries")
        if ministries_list:
            for li in ministries_list.find_all("li"):
                a = li.find("a")
                if a and a["href"]:
                    org_links.append(a["href"])
    return org_links

# Paso 2: Extraer miembros de cada organización
async def extract_members(session, url):
    members = []
    async with session.get(url, ssl=ssl_context) as resp:
        html = await resp.text()
        soup = BeautifulSoup(html, "html.parser")
        lis = soup.find_all("li", id=True)
        for li in lis:
            name = li.find("div", class_="name")
            rank = li.find("div", class_="rank")
            detail = li.find("div", class_="detail")
            tel = li.find("div", class_="tel info-contact")
            email = li.find("div", class_="email info-contact")

            member_data = {
                "name": name.get_text(strip=True) if name else "",
                "rank": rank.get_text(strip=True) if rank else "",
                "detail": detail.get_text(separator="\n", strip=True) if detail else "",
                "phone": tel.find("div").get_text(strip=True) if tel and tel.find("div") else "",
                "email": email.find("span", style=True).get_text(strip=True) if email and email.find("span", style=True) else "",
                "source_url": url
            }
            members.append(member_data)
    return members

# Paso 3: Proceso principal
# Quita asyncio.run()
async def scrape_peps_singapore():
    async with aiohttp.ClientSession() as session:
        org_links = await get_organization_links(session)
        print(f"Total organizaciones encontradas: {len(org_links)}")

        # Ejecutar scraping de miembros en paralelo
        tasks = [extract_members(session, link) for link in org_links]
        results = await asyncio.gather(*tasks)

        # Unificar resultados
        all_members = [member for sublist in results for member in sublist]

        # Guardar en JSON
        os.makedirs("data", exist_ok=True)
        with open("data/peps_singapore.json", "w", encoding="utf-8") as f:
            json.dump(all_members, f, ensure_ascii=False, indent=4)
