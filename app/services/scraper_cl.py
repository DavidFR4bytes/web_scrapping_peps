import pandas as pd
import os
import json



def scrape_peps_chile_api():
    url = "https://www.infoprobidad.cl/Home/Listado#"

    try:
        df = pd.read_excel(url)

        # Crear carpeta si no existe
        os.makedirs("data", exist_ok=True)

        # Guardar como JSON
        df.to_json("data/peps_chile.json", orient="records", force_ascii=False, indent=4)

        print(f"{len(df)} PEPs de Chile guardadas en data/peps_chile.json")
    except Exception as e:
        print(f"Error al procesar el archivo XLSX: {e}")