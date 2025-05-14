import pandas as pd
import requests
import json
import os

def scrape_peps_denmark_api():
    url = "https://www.finanstilsynet.dk/Media/638422919937140820/PEP_listen.xlsx"
    local_filename = "pep_dinamarca.xlsx"

    print("Descargando archivo Excel...")

    # Descargar el archivo
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error al descargar el archivo: {response.status_code}")
        return

    with open(local_filename, "wb") as f:
        f.write(response.content)

    print("Archivo descargado exitosamente.")

    # Leer el archivo con pandas
    df = pd.read_excel(local_filename)

    # Opcional: imprimir las primeras filas para entender las columnas
    print("Primeras filas del archivo:")
    print(df.head())

    # Limpieza básica
    df = df.fillna("")  # Rellenar valores nulos con cadena vacía

    # Convertir a lista de diccionarios
    pep_data = df.to_dict(orient="records")

    # Guardar el JSON
    output_path = os.path.join("data", "peps_dinamarca.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(pep_data, f, ensure_ascii=False, indent=4)

    print(f"Archivo guardado en: {output_path}")

if __name__ == "__main__":
    scrape_peps_denmark_api()
