from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import os

def scrape_peps_slovakia():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.nrsr.sk/web/Default.aspx?sid=vnf%2fzoznam&ViewType=2")

    wait = WebDriverWait(driver, 20)

    # Selección del combobox
    combobox = wait.until(EC.presence_of_element_located((By.ID, "_sectionLayoutContainer_ctl01_ViewsList")))
    combobox.find_element(By.XPATH, ".//option[@value='1']").click()

    # Click en el botón "Zobraziť"
    button = driver.find_element(By.ID, "_sectionLayoutContainer_ctl01_ShowSelectedView")
    button.click()

    # Esperar a que el contenedor aparezca
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.container_16")))

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    # Extraer datos
    peps = []
    for link in soup.select("div.container_16 a"):
        if 'href' in link.attrs:
            name = link.text.strip()
            partial_url = link['href'].strip()
            full_url = "https://www.nrsr.sk/web/" + partial_url
            if not full_url.startswith("https://www.nrsr.sk/web/Default.aspx?sid=vnf/oznamenie&UserId="):
                continue
            peps.append({
                "name": name,
                "url": full_url
            })

    # Guardar en JSON
    os.makedirs("data", exist_ok=True)
    with open("data/peps_slovakia.json", "w", encoding="utf-8") as f:
        json.dump(peps, f, ensure_ascii=False, indent=2)

    print(f"{len(peps)} PEPs extraídas y guardadas en peps_slovakia.json")

if __name__ == "__main__":
    scrape_peps_slovakia()
