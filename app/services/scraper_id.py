import requests
import pandas as pd
import os
import json
from io import BytesIO

def scrape_peps_indonesia_excel():
    url = "https://data.opensanctions.org/contrib/id_regional_2018/source.xlsx"

    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error al descargar el archivo: {response.status_code}")
        return

    # Leer ambas hojas
    xls = pd.ExcelFile(BytesIO(response.content))
    sheets = {
        "gubernur": xls.parse("Pemilihan Gubernur", header=3),
        "bupati_walikota": xls.parse("Pemilihan Bupati atau Walikota", header=3)
    }

    all_data = []

    # Procesar Pemilihan Gubernur
    for _, row in sheets["gubernur"].iterrows():
        data = {
            "no": row.get("No."),
            "kode_provinsi": row.get("Kode Provinsi"),
            "provinsi": row.get("Provinsi"),
            "nama_paslon": row.get("Nama Paslon"),
            "parpol_pendukung": row.get("Parpol Pendukung"),
            "perolehan_suara": row.get("Perolehan Suara"),
            "total_suara": row.get("Total Suara"),
            "presentase": row.get("Presentase"),
            "nivel": "Gubernur"
        }
        all_data.append(data)

    # Procesar Pemilihan Bupati atau Walikota
    for _, row in sheets["bupati_walikota"].iterrows():
        data = {
            "no": row.get("No."),
            "kode_provinsi": row.get("Kode Provinsi"),
            "provinsi": row.get("Provinsi"),
            "kode_kabupaten": row.get("Kode Kabupaten/Kota"),
            "kabupaten_kota": row.get("Kabupaten/Kota"),
            "nama_paslon": row.get("Nama Paslon"),
            "parpol_pendukung": row.get("Parpol Pendukung"),
            "perolehan_suara": row.get("Perolehan Suara"),
            "total_suara": row.get("Total Suara"),
            "presentase": row.get("Presentase"),
            "nivel": "Bupati/Walikota"
        }
        all_data.append(data)

    # Guardar en JSON
    os.makedirs("data", exist_ok=True)
    with open("data/peps_indonesia.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)

    print("Datos guardados correctamente en data/peps_indonesia.json")

