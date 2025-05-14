import requests
import json
import os
from bs4 import BeautifulSoup, SoupStrainer
import time


def scrape_peps_argentina_api():
    # URL del sitio web a scrapear
    URL = "https://www.hcdn.gob.ar/diputados/"

    # Iniciar una sesión para reutilizar la conexión HTTP
    session = requests.Session()

    # Hacer la petición HTTP
    start_time = time.time()
    response = session.get(URL)
    end_time = time.time()
    print("Iniciando scraping...")
    if response.status_code == 200:
        # Filtrar solo la tabla
        only_table = SoupStrainer("table")
        soup = BeautifulSoup(response.text, "html.parser", parse_only=only_table)

        # Encontrar la tabla por su ID
        table = soup.find("table", {"id": "tablaDiputados"})

        # Lista para almacenar los datos
        diputados_data = []

        if table:
            # Extraer filas de la tabla
            rows = table.find("tbody").find_all("tr")

            for row in rows:
                columns = row.find_all("td")

                a_tag = columns[1].find("a")
                if a_tag and a_tag.get("href"):
                    perfil_url = "https://www.hcdn.gob.ar" + a_tag["href"]
                else:
                    print("No se encontró el enlace del perfil en una fila, se omite.")
                    continue

                diputado = {
                    "foto": columns[0].find("img")["src"] if columns[0].find("img") else "No disponible",
                    "nombre": columns[1].text.strip(),
                    "perfil_url": perfil_url,
                    "distrito": columns[2].text.strip(),
                    "mandato": columns[3].text.strip(),
                    "inicio_mandato": columns[4].text.strip(),
                    "fin_mandato": columns[5].text.strip(),
                    "bloque": columns[6].text.strip(),
                    "fecha_nacimiento": "No disponible"
                }

                perfil_response = session.get(perfil_url)
                if perfil_response.status_code == 200:
                    perfil_soup = BeautifulSoup(perfil_response.text, "html.parser")
                    paragraph = perfil_soup.find("p", {"class": "encabezadoFecha"})
                    if paragraph:
                        diputado["fecha_nacimiento"] = paragraph.text.strip().replace("Fecha de Nac.: ", "")

                diputados_data.append(diputado)

            # Guardar en un archivo JSON
            # Guardar en un archivo JSON
            output_path = os.path.join("data", "peps_argentina.json")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            try:
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(diputados_data, f, ensure_ascii=False, indent=4)
                print(f"Datos guardados exitosamente en {output_path}")
            except Exception as e:
                print("Error al guardar el archivo:", e)

            print(f"Datos guardados en {output_path}")


        else:
            print("No se encontró la tabla de diputados.")

    else:
        print("Error al obtener la página. Código:", response.status_code)

    # Cerrar la sesión cuando se haya terminado
    session.close()

    print("Tiempo de ejecución: {:.2f} minutos".format((end_time - start_time) / 60))


if __name__ == "__main__":
    scrape_peps_argentina_api()