from SPARQLWrapper import SPARQLWrapper, JSON
import json
import os

def wikidata_query_service_api(limit=10000):
    all_peps = []
    offset = 0

    while True:
        print(f"Consultando OFFSET {offset}...")

        sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
        sparql.setReturnFormat(JSON)
        sparql.setQuery(f"""
        SELECT DISTINCT ?person ?personLabel ?positionLabel ?countryLabel WHERE {{
          ?person wdt:P39 ?position.
          ?person wdt:P27 ?country.
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }}
        LIMIT {limit}
        OFFSET {offset}
        """)

        try:
            results = sparql.query().convert()
        except Exception as e:
            print(f"Error al consultar OFFSET {offset}: {e}")
            break

        bindings = results["results"]["bindings"]
        if not bindings:
            break

        for result in bindings:
            all_peps.append({
                "nombre": result["personLabel"]["value"],
                "cargo": result["positionLabel"]["value"],
                "pais": result["countryLabel"]["value"],
                "wikidata_url": result["person"]["value"]
            })

        offset += limit

    # Guardar resultados
    os.makedirs("data", exist_ok=True)
    with open("data/peps_wikidata_q_s.json", "w", encoding="utf-8") as f:
        json.dump(all_peps, f, ensure_ascii=False, indent=2)

    print("Archivo guardado con éxito con", len(all_peps), "entradas.")
