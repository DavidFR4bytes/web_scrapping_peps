import requests
import json
import time
import os

def scrape_peps_armenia_api():
    base_url = "https://data.hetq.am/api/v2/en/front/filters"
    offset = 0
    step = 20
    year = 2019
    all_data = []

    print("Iniciando scraping de PEPs de Armenia desde API...")

    while True:
        params = {
            "filters[year]": year,
            "filters[officialtype]": "",
            "filters[category]": "money",
            "order": "DESC",
            "offset": offset
        }

        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            print(f"Error en la petición con offset {offset}: {response.status_code}")
            break

        data = response.json()
        if not data:  # Si la respuesta viene vacía, hemos llegado al final
            print("No hay más datos que extraer.")
            break

        print(f"Obtenidos {len(data)} registros con offset {offset}")
        all_data.extend(data)

        offset += step
        time.sleep(0.5)

    # Asegurar que el directorio 'data' exista
    os.makedirs("data", exist_ok=True)

    # Guardar los datos en el archivo dentro de la carpeta 'data'
    output_file = os.path.join("data", "peps_armenia_api.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)

    print(f"\nScraping completado. Se guardaron {len(all_data)} registros en {output_file}.")

if __name__ == "__main__":
    scrape_peps_armenia_api()
