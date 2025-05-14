import requests
import json
import os


def scrape_peps_mexico_diputados_api():
    url = "https://micrositios.diputados.gob.mx:4001/graphql"

    query = """
    {
      allDiputados(Legislacion: "") {
        Nombre
        PrimerApellido
        SegundoApellido
        NombreCompleto
        Estado
        Partido
        Distrito
        Legislacion
        CabeceraMunicipal
        Suplente
        Correo
        Telefono
        TipoEleccion
        Licencia
      }
    }
    """

    payload = json.dumps({"query": query})
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        raw_peps = response.json().get("data", {}).get("allDiputados", [])
        peps = []

        for pep in raw_peps:
            peps.append({
                "name": pep.get("Nombre", ""),
                "first_surname": pep.get("PrimerApellido", ""),
                "second_surname": pep.get("SegundoApellido", ""),
                "full_name": pep.get("NombreCompleto", ""),
                "state": pep.get("Estado", ""),
                "party": pep.get("Partido", ""),
                "district": pep.get("Distrito", ""),
                "legislation": pep.get("Legislacion", ""),
                "municipality": pep.get("CabeceraMunicipal", ""),
                "substitute": pep.get("Suplente", ""),
                "email": pep.get("Correo", ""),
                "phone": pep.get("Telefono", ""),
                "election_type": pep.get("TipoEleccion", ""),
                "license": pep.get("Licencia", "")
            })
    else:
        print(f"Error al obtener los datos. Código de estado: {response.status_code}")
        return

    os.makedirs("data", exist_ok=True)
    with open("data/peps_mexico_diputados.json", "w", encoding="utf-8") as f:
        json.dump(peps, f, ensure_ascii=False, indent=4)

    print(f"{len(peps)} PEPs guardadas en data/peps_mexico_diputados.json")

def scrape_peps_mexico_senadores_api():
    url = "https://www.senado.gob.mx/66/datosAbiertos/senadoresDatosAb_66.json"

    response = requests.get(url)

    if response.status_code == 200:
        peps = response.json()
    else:
        print(f"Error al obtener los datos. Código de estado: {response.status_code}")
        return

    os.makedirs("data", exist_ok=True)
    with open("data/peps_mexico_senadores.json", "w", encoding="utf-8") as f:
        json.dump(peps, f, ensure_ascii=False, indent=4)

    print(f"{len(peps)} PEPs guardadas en data/peps_mexico_senadores.json")