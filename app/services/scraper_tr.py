import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import json
import os

async def scrape_peps_turkey():
    url = "https://www.tbmm.gov.tr/milletvekili/AllList"
    peps = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, timeout=60000)
        await page.wait_for_load_state("networkidle")  # esperar a que cargue el contenido JS

        html = await page.content()
        await browser.close()

        soup = BeautifulSoup(html, "html.parser")

        for ul in soup.find_all("ul", class_="tbmm-list-ul"):
            current_province = None

            for li in ul.find_all("li", class_="list-group-item"):
                if "tbmm-list-item-active" in li.get("class", []):
                    current_province = li.get_text(strip=True)
                    continue

                name_tag = li.find("a")
                party_tag = li.find("div", class_="col-md-4")

                name = name_tag.get_text(strip=True) if name_tag else ""
                link = "https://www.tbmm.gov.tr" + name_tag["href"] if name_tag and name_tag.has_attr("href") else ""
                party = party_tag.get_text(strip=True) if party_tag else ""

                peps.append({
                    "nombre": name,
                    "partido": party,
                    "provincia": current_province,
                    "url_biografia": link
                })

    os.makedirs("data", exist_ok=True)
    with open("data/peps_turkey.json", "w", encoding="utf-8") as f:
        json.dump(peps, f, ensure_ascii=False, indent=4)

    print(f"{len(peps)} PEPs de Turquía guardadas en data/peps_turkey.json")

# Ejecutar el script asíncrono
asyncio.run(scrape_peps_turkey())
