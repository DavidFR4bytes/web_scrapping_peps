import requests
import json
import os
import time
from bs4 import BeautifulSoup

def scrape_peps_cuba_api():
    url = "https://proyectoinventario.org/x-legislatura-la-asamblea-nacional-poder-popular-parlamento-cuba-2023-2028/"
    session = requests.Session()

    print("Iniciando scraping de PEPs de Cuba...")
    start_time = time.time()
    response = session.get(url)
    end_time = time.time()

    if response.status_code != 200:
        print(f"Error al acceder a la página: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.select("tr[id^='table_107_row_']")

    pep_data = []

    for row in rows:
        columns = row.find_all("td")
        if len(columns) < 8:
            continue  # Asegurarse de que la fila tiene suficientes columnas

        foto_tag = columns[1].find("img")
        foto_url = foto_tag["src"] if foto_tag else None

        pep = {
            "nombre": columns[2].get_text(strip=True),
            "ocupacion": columns[3].get_text(strip=True),
            "edad": columns[4].get_text(strip=True),
            "votos_validos": columns[5].get_text(strip=True),
            "provincia": columns[12].get_text(strip=True),
            "municipio": columns[13].get_text(strip=True),
            "foto": foto_url
        }

        pep_data.append(pep)

    # Guardar los datos en un archivo JSON
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "peps_cuba.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(pep_data, f, ensure_ascii=False, indent=4)

    print(f"Datos de {len(pep_data)} PEPs de Cuba guardados en {output_path}")
    print("Tiempo de ejecución: {:.2f} segundos".format(end_time - start_time))

if __name__ == "__main__":
    scrape_peps_cuba_api()
