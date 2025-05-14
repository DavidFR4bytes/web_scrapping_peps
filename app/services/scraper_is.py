from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import os
import time

def scrape_peps_iceland_api():
    url = "https://www.althingi.is/altext/cv/en/"

    options = Options()
    # NO headless para evitar bloqueos
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("start-maximized")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(7)  # Aumenta si la página tarda en cargar

    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, "html.parser")

    peps = []
    rows = soup.find_all("tr")

    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 2:
            name_tag = cols[0].find("a")
            name = name_tag.text.strip() if name_tag else cols[0].text.strip()
            party = cols[1].text.strip()

            peps.append({
                "nombre": name,
                "partido": party
            })

    os.makedirs("data", exist_ok=True)
    with open("data/peps_islandia.json", "w", encoding="utf-8") as f:
        json.dump(peps, f, ensure_ascii=False, indent=4)


