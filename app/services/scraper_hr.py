import requests
import os
import csv
import json
import io

def scrape_peps_croatia_api():
    csv_url = "https://www.sukobinteresa.hr/export/registar_rukovodecih_drzavnih_sluzbenika_koje_imenuje_vlada_republike_hrvatske.csv?1744650475"

    print("Descargando archivo CSV...")

    response = requests.get(csv_url)
    if response.status_code != 200:
        print(f"Error al descargar el archivo: {response.status_code}")
        return

    # Encabezados personalizados para evitar duplicados
    fieldnames = [
        "nombre", "apellido",
        "cargo_1", "institucion_1", "inicio_1", "fin_1",
        "cargo_2", "institucion_2", "inicio_2", "fin_2"
    ]

    csv_reader = csv.DictReader(io.StringIO(response.text), delimiter=';', fieldnames=fieldnames)
    pep_data = []

    # Saltamos la primera fila que contiene los encabezados originales
    next(csv_reader)

    for row in csv_reader:
        pep = {
            "nombre": row["nombre"],
            "apellido": row["apellido"],
            "cargos": []
        }

        if row["cargo_1"] or row["institucion_1"]:
            pep["cargos"].append({
                "cargo": row["cargo_1"],
                "institucion": row["institucion_1"],
                "inicio": row["inicio_1"],
                "fin": row["fin_1"]
            })

        if row["cargo_2"] or row["institucion_2"]:
            pep["cargos"].append({
                "cargo": row["cargo_2"],
                "institucion": row["institucion_2"],
                "inicio": row["inicio_2"],
                "fin": row["fin_2"]
            })

        pep_data.append(pep)

    # Guardar como JSON
    output_path = os.path.join("data", "peps_croacia.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(pep_data, f, ensure_ascii=False, indent=4)

    print(f"{len(pep_data)} registros guardados en peps_croacia.json")


if __name__ == "__main__":
    scrape_peps_croatia_api()
