import requests
from bs4 import BeautifulSoup
import os
import time
import json

# Enlaces directos a cada año
links_iniciales = [
    ("2024", "http://62.176.124.194/index.php?option=com_content&view=article&layout=edit&id=233&Itemid=103"),
    ("2023", "http://62.176.124.194/index.php?option=com_content&view=article&layout=edit&id=204&Itemid=103"),
    ("2022", "http://62.176.124.194/index.php?option=com_content&view=article&layout=edit&id=175&Itemid=103"),
    ("2021", "http://62.176.124.194/index.php?option=com_content&view=article&layout=edit&id=146&Itemid=103"),
    ("2020", "http://62.176.124.194/index.php?option=com_content&view=article&layout=edit&id=115&Itemid=103"),
    ("2019", "http://62.176.124.194/index.php?option=com_content&view=article&layout=edit&id=31&Itemid=103"),
    ("2018", "http://62.176.124.194/index.php?option=com_content&view=article&layout=edit&id=44&Itemid=103"),
    ("2017", "http://62.176.124.194/index.php?option=com_content&view=article&layout=edit&id=80&Itemid=103")
]

# Función para extraer los enlaces por letra del alfabeto en cada página anual
def extraer_links_letras(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        links = [
            a.get("href")
            for a in soup.find_all("a", href=True)
            if "images/declaracii" in a.get("href") and a.get("href").endswith(".pdf")
        ]
        return ["http://62.176.124.194" + link for link in links]
    except Exception as e:
        print(f"Error extrayendo links PDF: {e}")
        return []

# Función para extraer los datos de cada tabla de personas con enlaces PDF
def extraer_datos_tabla(url, anio):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        tabla = soup.find("table")
        if not tabla:
            return []

        filas = tabla.find_all("tr")[1:]
        datos = []

        for fila in filas:
            celdas = fila.find_all("td")
            if len(celdas) >= 2:
                link_tag = celdas[0].find("a")
                if link_tag:
                    nombre = link_tag.text.strip()
                    url_pdf = "http://62.176.124.194" + link_tag.get("href")
                    nro_entrada = celdas[1].text.strip()
                    datos.append({
                        "nombre": nombre,
                        "url_pdf": url_pdf,
                        "nro_entrada": nro_entrada,
                        "año": anio
                    })
        return datos
    except Exception as e:
        print(f"Error extrayendo datos de {url}: {e}")
        return []

def extraer_todos_los_datos():
    todos_los_datos = []

    for año, link_anual in links_iniciales:
        print(f"Procesando año ({año}): {link_anual}")
        datos = extraer_datos_tabla(link_anual, año)
        todos_los_datos.extend(datos)
        time.sleep(1)

    os.makedirs("data", exist_ok=True)
    with open("data/peps_bulgaria.json", "w", encoding="utf-8") as f:
        json.dump(todos_los_datos, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    extraer_todos_los_datos()



