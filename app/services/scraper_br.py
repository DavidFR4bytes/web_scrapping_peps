import requests
import zipfile
import io
import os
import csv
import json

def normalize_field(value):
    """Convierte 'Não informada' a None, si no, retorna el valor limpio."""
    value = value.strip()
    return None if value.lower() in ["não informada", "nao informada", ""] else value

def scrape_peps_brazil_api():
    zip_url = "https://portaldatransparencia.gov.br/download-de-dados/pep/202502"
    print("Descargando archivo ZIP...")

    response = requests.get(zip_url)
    if response.status_code != 200:
        print(f"Error al descargar el archivo: {response.status_code}")
        return

    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
        csv_filename = next((name for name in zip_file.namelist() if name.endswith(".csv")), None)

        if not csv_filename:
            print("No se encontró ningún archivo CSV dentro del ZIP.")
            return

        print(f"Extrayendo y procesando archivo CSV: {csv_filename}")
        with zip_file.open(csv_filename) as csv_file_obj:
            csv_reader = csv.DictReader(io.TextIOWrapper(csv_file_obj, encoding='latin1'), delimiter=';')
            pep_data = []

            for row in csv_reader:
                pep = {
                    "cpf": normalize_field(row.get("CPF")),
                    "full_name": normalize_field(row.get("Nome_PEP")),
                    "role_code": normalize_field(row.get("Sigla_Função")),
                    "role_description": normalize_field(row.get("Descrição_Função")),
                    "role_level": normalize_field(row.get("Nível_Função")),
                    "organization": normalize_field(row.get("Nome_Órgão")),
                    "start_date": normalize_field(row.get("Data_Início_Exercício")),
                    "end_date": normalize_field(row.get("Data_Fim_Exercício")),
                    "grace_period_end": normalize_field(row.get("Data_Fim_Carência"))
                }
                pep_data.append(pep)

    os.makedirs("data", exist_ok=True)
    with open("data/peps_brasil.json", "w", encoding="utf-8") as f:
        json.dump(pep_data, f, ensure_ascii=False, indent=4)

    print(f"Datos de {len(pep_data)} personas PEP de Brasil guardados en data/peps_brasil.json")

if __name__ == "__main__":
    scrape_peps_brazil_api()
