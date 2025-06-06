import requests
import json
import os

SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"

QUERY = """
SELECT DISTINCT ?item ?label WHERE {
  ?item wdt:P31 wd:Q5.
  FILTER NOT EXISTS { ?item wdt:P570 ?dateOfDeath. }

  {
    ?item wdt:P106 wd:Q82955.
  } UNION {
    ?item wdt:P106 wd:Q8125919.
  }

  ?item wdt:P27 wd:Q148.  # Ciudadanía china

  OPTIONAL { ?item rdfs:label ?label. FILTER (lang(?label) = "en") }
}

"""

def fetch_peps_china():
    headers = {
        "Accept": "application/sparql-results+json"
    }
    response = requests.get(SPARQL_ENDPOINT, params={"query": QUERY}, headers=headers)

    if response.status_code != 200:
        raise Exception(f"SPARQL query failed: {response.status_code} - {response.text}")

    data = response.json()
    peps = []

    for result in data["results"]["bindings"]:
        item_url = result["item"]["value"]
        name = result.get("label", {}).get("value")

        if name is not None and name != "Unknown":
            peps.append({
                "name": name,
                "wikidata_url": item_url,
                "source": "Wikidata",
                "country": "China"
            })
    os.makedirs("data", exist_ok=True)
    with open("data/peps_china.json", "w", encoding="utf-8") as f:
        json.dump(peps, f, ensure_ascii=False, indent=4)

    print(f"Guardado {len(peps)} registros en data/peps_china.json")

if __name__ == "__main__":
    fetch_peps_china()
