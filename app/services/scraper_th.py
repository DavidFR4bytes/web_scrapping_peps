import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import json

async def get_page_html(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(url, timeout=60000)
        await page.wait_for_load_state('networkidle')
        html = await page.content()
        await browser.close()
        return html

def extract_peps(html):
    soup = BeautifulSoup(html, 'html.parser')
    peps = []

    containers = soup.select("div.elementor-widget-container")
    for div in containers:
        text = div.get_text(separator=" ", strip=True)
        if text and len(text) > 5:
            peps.append({
                "nombre": text
            })

    return peps

async def scrape_peps_thailandia_api():
    url = "https://www.soc.go.th/?page_id=182"
    html = await get_page_html(url)
    pep_data = extract_peps(html)

    with open("peps_tailandia.json", "w", encoding="utf-8") as f:
        json.dump(pep_data, f, ensure_ascii=False, indent=2)

    print(f"Se extrajeron {len(pep_data)} registros y se guardaron en 'peps_tailandia.json'")

# Ejecutar el script
if __name__ == "__main__":
    asyncio.run(scrape_peps_thailandia_api())
