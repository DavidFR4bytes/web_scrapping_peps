import requests
import os
import csv
import json
import io
from bs4 import BeautifulSoup


def scrape_peps_france_mayors_api():
    csv_url = "https://www.data.gouv.fr/fr/datasets/r/2876a346-d50c-4911-934e-19ee07b0e503"
    print("Descargando archivo CSV...")

    response = requests.get(csv_url)
    if response.status_code != 200:
        print(f"Error al descargar el archivo: {response.status_code}")
        return

    csv_reader = csv.DictReader(io.StringIO(response.content.decode("utf-8")), delimiter=';')
    pep_data = []

    for row in csv_reader:
        pep = {
            "codigo_departamento": row.get("Code du département", ""),
            "etiqueta_departamento": row.get("Libellé du département", ""),
            "codigo_colectividad": row.get("Code de la collectivité à statut particulier", ""),
            "etiqueta_comunidad": row.get("Libellé de la collectivité à statut particulier", ""),
            "codigo_municipio": row.get("Code de la commune", ""),
            "nombre_municipio": row.get("Libellé de la commune", ""),
            "nombre_funcionario_electo": row.get("Nom de l'élu", ""),
            "apellido_funcionario_electo": row.get("Prénom de l'élu", ""),
            "codigo_sexo": row.get("Code sexe", ""),
            "fecha_nacimiento": row.get("Date de naissance", ""),
            "codigo_socioprofesional": row.get("Code de la catégorie socio-professionnelle", ""),
            "etiqueta_categoria_socioprofesional": row.get("Libellé de la catégorie socio-professionnelle", ""),
            "fecha_inicio_mandato": row.get("Date de début du mandat", ""),
            "fecha_inicio_funcion": row.get("Date de début de la fonction", "")
        }
        pep_data.append(pep)

    os.makedirs("data", exist_ok=True)
    with open("data/peps_francia1.json", "w", encoding="utf-8") as f:
        json.dump(pep_data, f, ensure_ascii=False, indent=4)

    print("Scraping de PEPs de Francia 1 completado.")



def scrape_peps_france_senators_api():
    csv_url = "https://data.senat.fr/data/senateurs/ODSEN_GENERAL.csv"

    print("Descargando archivo CSV...")

    response = requests.get(csv_url)
    if response.status_code != 200:
        print(f"Error al descargar el archivo: {response.status_code}")
        return

    # Decodificar con ISO-8859-1 para manejar caracteres franceses
    raw_lines = response.content.decode("ISO-8859-1").splitlines()

    # Omitir las primeras 18 líneas
    data_lines = raw_lines[18:]

    # Usar coma como delimitador
    csv_reader = csv.DictReader(data_lines, delimiter=',')

    pep_data = []

    for row in csv_reader:
        pep = {
            "matricula": row.get("Matricule", "").strip(),
            "calidad": row.get("Qualité", "").strip(),
            "nombre_comun": row.get("Nom usuel", "").strip(),
            "nombre_habitual": row.get("Prénom usuel", "").strip(),
            "estado": row.get("État", "").strip(),
            "fecha_nacimiento": row.get("Date naissance", "").strip(),
            "fecha_deceso": row.get("Date de décès", "").strip(),
            "grupo_politico": row.get("Groupe politique", "").strip(),
            "tipo_adhesion_grupo": row.get("Type d'app au grp politique", "").strip(),
            "comision_permanente": row.get("Commission permanente", "").strip(),
            "circunscripcion": row.get("Circonscription", "").strip(),
            "funcion_bureau_senado": row.get("Fonction au Bureau du Sénat", "").strip(),
            "correo_electronico": row.get("Courrier électronique", "").strip(),
            "pcs_insee": row.get("PCS INSEE", "").strip(),
            "categoria_profesional": row.get("Catégorie professionnelle", "").strip(),
            "descripcion_profesion": row.get("Description de la profession", "").strip()
        }
        pep_data.append(pep)

    os.makedirs("data", exist_ok=True)
    with open("data/peps_francia_senadores.json", "w", encoding="utf-8") as f:
        json.dump(pep_data, f, ensure_ascii=False, indent=4)

    print("Scraping de PEPs de senadores de Francia completado.")


def scrape_national_assembly_france_api():

    base_url = "https://www2.assemblee-nationale.fr"
    list_url = base_url + "/deputes/liste/tableau"

    response = requests.get(list_url, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, "html.parser")
    rows = soup.select("table tbody tr")

    peps = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) != 3:
            continue

        # Nombre y URL
        a_tag = cols[0].find("a")
        nombre = a_tag.get_text(strip=True) if a_tag else ""
        url_ficha = base_url + a_tag["href"] if a_tag and a_tag.has_attr("href") else ""

        # Departamento y número de circunscripción
        departamento = cols[1].get_text(strip=True)
        circunscripcion = cols[2].get_text(strip=True)

        peps.append({
            "nombre": nombre,
            "departamento": departamento,
            "circunscripcion": circunscripcion,
            "url_biografia": url_ficha,
            "pais": "Francia",
            "fuente": list_url
        })

    os.makedirs("data", exist_ok=True)
    with open("data/peps_national_assembly_france.json", "w", encoding="utf-8") as f:
        json.dump(peps, f, ensure_ascii=False, indent=4)

    print(f"Se extrajeron {len(peps)} PEPs de Francia.")


