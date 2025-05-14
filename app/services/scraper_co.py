import requests
import os
import csv
import json
import io

def scrape_peps_colombia_api():
    csv_url = "https://peps.directoriolegislativo.org/datasets/peps.csv"

    print("Descargando archivo CSV...")

    response = requests.get(csv_url)
    if response.status_code != 200:
        print(f"Error al descargar el archivo: {response.status_code}")
        return

    csv_reader = csv.DictReader(io.StringIO(response.text), delimiter=',')
    pep_data = []

    for row in csv_reader:
        pep = {
            "ID / CC": row["ID / CC"],
            "primer nombre": row["Primer Nombre"],
            "segundo nombre": row["Segundo Nombre"],
            "primer apellido": row["Primer Apellido"],
            "segundo apellido": row["Segundo Apellido"],
            "ID / ENTIDAD": row["ID / Entidad"],
            "nombre entidad": row["Entidad"],
            "departamento": row["Departamento"],
            "municipio": row["Municipio"],
        }
        pep_data.append(pep)

    os.makedirs("data", exist_ok=True)
    with open("data/peps_colombia.json", "w", encoding="utf-8") as f:
        json.dump(pep_data, f, ensure_ascii=False, indent=4)

    print("Scraping de PEPs de Colombia completado.")

if __name__ == "__main__":
    scrape_peps_colombia_api()