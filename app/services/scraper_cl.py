from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import os
import time

# Cargos considerados como PEPs
PEP_CARGOS = {
    "ALACALDE", "ALCALDE", "ALCALDE  TERMINO DE PERIODO", "ALCALDE I.MUNICIPALIDAD DE CHANCO",
    "ALCALDE(A)", "ALCALDE 2024-2028", "EX ALCALDE 2021-2024", "ALCALDESA",
    "CONCEJAL", "CONCEJAL 2024-2028", "CONCEJAL (A)", "CONCEJAL (A) NO VIGENTE",
    "CONCEJAL DEJA CARGO", "CONCEJAL I-MUNICIPALIDAD DE CHANCO", "CONCEJAL SALIENTE",
    "CONCEJAL VITACURA", "CONCEJAL(A)", "CONCEJAL/A", "CONCEJALA", "CONCEJALES",
    "DIRECTIVO JEFE DE DEPARTAMENTO", "EMBAJADOR", "EMBAJADOR PRIMERA CATEGORÍA EXTERIOR",
    "EMBAJADORA", "GOBERNADOR ", "GOBERNADOR REGIONAL", "GOBERNADORA REGIONAL", "JUEZ",
    "JEFE GABINETE", "JEFE(A) DE GABINETE MINISTRO(A)", "JEFE DEPARTAMENTO DE BIENESTAR",
    "JEFE SECCION AUDITORIA PROYECTOS DE INVERSION", "SENADOR(A)", "SEREMI", "MINISTRA",
    "MINISTRA(O)", "MINISTRO", "MINISTRO CONSEJERO", "MINISTRO CONSEJERO O CÓNSUL GENERAL PRIMERA CLASE, SEGUNDA CATEGORÍA EXTERIOR",
    "MINISTRO DE AGRICULTURA", "MINISTRO DE ECONOMÍA FOMENTO Y TURISMO", "MINISTRO DE FE",
    "MINISTRO DE RELACIONES EXTERIORES", "MINISTRO DEL TRIBUNAL CALIFICADOR DE ELECCIONES",
    "MINISTRO SUPLENTE", "MINISTRO TITULAR", "MINISTRO(A)", "MINISTRO(A) DESARROLLO SOCIAL",
    "MINISTRO/A", "PRESIDENTE COMPIN", "TESORERO", "TESORERO GENERAL",
    "TESORERO GENERAL DE LA REPUBLICA", "TESORERO/A GENERAL DE LA REPUBLICA",
    "VICEPRESIDENTA/E EJECUTIVA/O", "VICEPRESIDENTE", "VICEPRESIDENTE EJECUTIVO",
    "SEREMI REGIÓN ARAUCANÍA", "SEREMI REGION ARICA Y PARINACOTA", "SEREMI REGIÓN ATACAMA",
    "SEREMI REGIÓN DE ANTOFAGASTA", "SEREMI REGIÓN DE ARICA Y PARINACOTA", "SEREMI REGIÓN DE AYSÉN",
    "SEREMI REGIÓN DE BIOBIO", "SEREMI REGIÓN DE COQUIMBO", "SEREMI REGIÓN DE LOS LAGOS",
    "SEREMI REGIÓN DE LOS RÍOS", "SEREMI REGIÓN DE MAGALLANES", "SEREMI REGIÓN DE ÑUBLE",
    "SEREMI REGION DE TARAPACA", "SEREMI REGIÓN DE VALPARAÍSO", "SEREMI REGIÓN DEL LIBERTADOR BERNARDO O¨HIGGINS",
    "SEREMI REGIÓN DEL MAULE", "SEREMI REGIÓN METROPOLITANA",
    "TERCER SECRETARIO O CÓNSUL DE SEGUNDA CLASE, SEPTIMA CATEGORIA EXTERIOR",
    "TERCER SECRETARIO O CÓNSUL DE SEGUNDA CLASE, SEXTA CATEGORÍA EXTERIOR",
    "TERCER SECRETARIO O CÓNSUL DE TERCERA CLASE, SEXTA CATEGORÍA EXTERIOR",
    "TERCERA SECRETARIA O CÓNSUL DE TERCERA CLASE, SEXTA CATEGORÍA EXTERIOR",
    "TERCER SECRETARIO O CÓNSUL SEGUNDA CLASE, SÉPTIMA CATEGORÍA EXTERIOR",
    "PRIMER SECRETARIO O CÓNSUL DE PRIMERA CLASE, CUARTA CATEGORÍA EXTERIOR",
    "PRIMERA SECRETARIA O CÓNSUL DE PRIMERA CLASE, CUARTA CATEGORÍA EXTERIOR",
    "CONSEJERO O CÓNSUL GENERAL SEGUNDA CLASE, TERCERA CATEGORÍA EXTERIOR",
    "SEGUNDO SECRETARIO O CÓNSUL DE SEGUNDA CLASE, QUINTA CATEGORÍA EXTERIOR",
    "SEGUNDA SECRETARIA O CÓNSUL DE SEGUNDA CLASE, QUINTA CATEGORÍA EXTERIOR"
}

def scrape_peps_chile():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.infoprobidad.cl/Home/Listado")

    wait = WebDriverWait(driver, 20)
    peps = []
    current_page = 1

    while True:
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.k-grid-content table tbody tr")))

            soup = BeautifulSoup(driver.page_source, "html.parser")
            rows = soup.select("div.k-grid-content table tbody tr")

            for row in rows:
                cols = row.find_all("td")
                if len(cols) < 7:
                    continue

                cargo = cols[5].get_text(strip=True).upper()
                if cargo not in PEP_CARGOS:
                    continue  # Filtramos directamente

                declaracion_link = cols[1].find("a")
                declaracion_url = "https://www.infoprobidad.cl" + declaracion_link["href"] if declaracion_link else ""

                peps.append({
                    "fecha_declaracion": cols[0].get_text(strip=True),
                    "tipo_declaracion": cols[1].get_text(strip=True),
                    "nombres": cols[2].get_text(strip=True),
                    "apellido_paterno": cols[3].get_text(strip=True),
                    "apellido_materno": cols[4].get_text(strip=True),
                    "cargo": cargo,
                    "entidad": cols[6].get_text(strip=True),
                    "link": declaracion_url
                })

            print(f"Página {current_page} procesada. PEPs acumulados: {len(peps)}")

            # Botón de siguiente página
            next_button = driver.find_element(By.CSS_SELECTOR, "a.k-link.k-pager-nav[title='Go to the next page']")
            if "k-state-disabled" in next_button.get_attribute("class"):
                break

            next_button.click()
            current_page += 1

        except Exception as e:
            print(f"Fin del scraping en página {current_page}: {str(e)}")
            break

    driver.quit()

    os.makedirs("data", exist_ok=True)
    with open("data/peps_chile_filtradas.json", "w", encoding="utf-8") as f:
        json.dump(peps, f, ensure_ascii=False, indent=4)

    print(f"Finalizado. Total PEPs extraídas: {len(peps)}")

if __name__ == "__main__":
    scrape_peps_chile()
