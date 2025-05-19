from fastapi import FastAPI

from app.services.scraper_cn import fetch_peps_china
from services.scraper_sg import scrape_peps_singapore
from services.scraper_ar import scrape_peps_argentina_api
from services.scraper_am import scrape_peps_armenia_api
from services.scraper_at import scrape_peps_austria_api
from services.scraper_br import scrape_peps_brazil_api
from services.scraper_ky import scrape_peps_cayman_api, scrape_cayman_officials
from services.scraper_co import scrape_peps_colombia_api
from services.scraper_hr import scrape_peps_croatia_api
from services.scraper_cu import scrape_peps_cuba_api
from services.scraper_dk import scrape_peps_denmark_api
from services.scraper_ee import scrape_peps_estonia_api
from services.scraper_eu import scrape_peps_european_union_api
from services.scraper_fr_mayors import scrape_peps_france_mayors_api
from services.scraper_fr_mayors import scrape_peps_france_senators_api, scrape_national_assembly_france_api
from services.scraper_de import scrape_peps_alemania_api
from services.scraper_hk import scrape_peps_hong_kong_principal_officials_api
from services.scraper_hk import scrape_peps_hong_kong_council_members_api
from services.scraper_is import scrape_peps_iceland_api
from services.scraper_il import scrape_peps_israel_api
from services.scraper_lv import scrape_peps_latvia_api
from services.scraper_lt import scrape_peps_lithuania_api
from services.scraper_mx import scrape_peps_mexico_diputados_api, scrape_peps_mexico_senadores_api
from services.scraper_me import scrape_peps_montenegro_api
from services.scraper_ng import scrape_peps_nigeria_api, scrape_peps_nigeria_dot
#from services.scraper_cl import
from services.scraper_ro import scrape_peps_romania_api
from services.scraper_si import scrape_peps_slovenia_api
from services.scraper_za import scrape_peps_south_africa_municipal_leaders_api, scraper_peps_south_africa_provincial_legislators_api
from services.scraper_th import scrape_peps_thailandia_api
from services.scraper_us import scrape_peps_usa_plum_api, scrape_peps_usa_cia_world_liders_api, scrape_peps_usa_members_congress_api, scrape_peps_us_navy_leadership_api, scrape_peps_us_state_department_api
from services.scraper_uy import scrape_peps_uruguay_api
from services.scraper_ve import scrape_peps_venezuela
from services.scraper_nl import scrape_peps_netherlands
from services.scraper_wikidata_query_service import wikidata_query_service_api
from services.scraper_id import scrape_peps_indonesia_excel

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/scrape/{country_code}")
async def search(country_code: str):

    country_code = country_code.upper()
    # codigos_paises = obtener_codigo_pais()
    #
    # if country_code not in codigos_paises:
    #     return {"message": "Country not supported"}

    if country_code == "AR":
        try:
            scrape_peps_argentina_api()
            return {"message": "Success"}
        except Exception as e:
            print(e)

    if country_code == "AM":
        try:
            scrape_peps_armenia_api()
            return {"message": "Success"}
        except Exception as e:
            print(e)

    if country_code == "AT":
        try:
            scrape_peps_austria_api()
            return {"message": "Success"}
        except Exception as e:
            print(e)

    if country_code == "BR":
        try:
            scrape_peps_brazil_api()
            return {"message": "Success"}
        except Exception as e:
            print(e)

    if country_code == "KY":
        try:
            scrape_peps_cayman_api()
            return {"message": "Success"}
        except Exception as e:
            print(e)

    if country_code == "KY_OF":
        try:
            scrape_cayman_officials()
            return {"message": "Success"}
        except Exception as e:
            print(e)

    if country_code == "CO":
        try:
            scrape_peps_colombia_api()
            return {"message": "Success"}
        except Exception as e:
            print(e)

    if country_code == "HR":
        try:
            scrape_peps_croatia_api()
            return {"message": "Success"}
        except Exception as e:
            print(e)

    if country_code == "CU":
        try:
            scrape_peps_cuba_api()
            return {"message": "Success"}
        except Exception as e:
            print(e)

    if country_code == "CN":
        try:
            fetch_peps_china()
            return {"message": "Success"}
        except Exception as e:
            print(e)

    if country_code == "DK":
        try:
            scrape_peps_denmark_api()
            return {"message": "Success"}
        except Exception as e:
            print(e)

    if country_code == "EE":
        try:
            scrape_peps_estonia_api()
            return {"message": "Success"}
        except Exception as e:
            print(e)


    if country_code == "EU":
        try:
            scrape_peps_european_union_api()
            return {"message": "Success"}
        except Exception as e:
            print(e)

    if country_code == "FR1":
        try:
            scrape_peps_france_mayors_api()
            return {"message": "Success"}
        except Exception as e:
            print("error")
            print(e)

    if country_code == "FR2":
        try:
            scrape_peps_france_senators_api()
            return {"message": "Success"}
        except Exception as e:
            print("error")
            print(e)

    if country_code == "FR3":
        try:
            scrape_national_assembly_france_api()
            return {"message": "Success"}
        except Exception as e:
            print("error")
            print(e)

    if country_code == "DE":
        try:
            scrape_peps_alemania_api()
            return {"message": "Success"}
        except Exception as e:
            print(e)

    if country_code == "HK1":
        try:
            scrape_peps_hong_kong_principal_officials_api()
            return {"message": "Success"}
        except Exception as e:
            print(e)

    if country_code == "HK2":
        try:
            scrape_peps_hong_kong_council_members_api()
            return {"message": "Success"}
        except Exception as e:
            print(e)

    if country_code == "ID":
        try:
            scrape_peps_indonesia_excel()
            return {"message": "Success"}
        except Exception as e:
            print(e)

    if country_code == "IS":
        try:
            scrape_peps_iceland_api()
            return {"message": "Success"}
        except Exception as e:
            print(e)

    if country_code == "IL":
        try:
            scrape_peps_israel_api()
            return {"message": "Success"}
        except Exception as e:
            print(e)

    if country_code == "LV":
        try:
            scrape_peps_latvia_api()
            return {"message": "Success"}
        except Exception as e:
            print(e)

    if country_code == "LT":
        try:
            scrape_peps_lithuania_api()
            return {"message": "Success"}
        except Exception as e:
            print(e)

    if country_code == "MX_DP":
        try:
            scrape_peps_mexico_diputados_api()
            return {"message": "Success"}
        except Exception as e:
            print(e)

    if country_code == "MX_SN":
        try:
            scrape_peps_mexico_senadores_api()
            return {"message": "Success"}
        except Exception as e:
            print(e)

    if country_code == "ME":
        try:
            scrape_peps_montenegro_api()
            return {"message": "Success"}
        except Exception as e:
            print(e)

    if country_code == "NG":
        try:
            scrape_peps_nigeria_api()
            return {"message": "Success"}
        except Exception as e:
            print(e)

    if country_code == "NL":
        try:
            scrape_peps_netherlands()
            return {"message": "Success"}
        except Exception as e:
            print(e)


    if country_code == "NG_DOT":
        try:
            scrape_peps_nigeria_dot()
            return {"message": "Success"}
        except Exception as e:
            print(e)

    """if country_code == "CL":
        try:
            scrape_peps_chile_api()
            return {"message": "Success"}
        except Exception as e:
            print(e)"""

    if country_code == "RO":
        try:
            scrape_peps_romania_api()
            return {"message": "Success"}
        except Exception as e:
            print(e)

    if country_code == "SI":
        try:
            scrape_peps_slovenia_api()
            return {"message": "Success"}
        except Exception as e:
            print(e)

    if country_code == "ZA_ML":
        try:
            scrape_peps_south_africa_municipal_leaders_api()
            return {"message": "Success"}
        except Exception as e:
            print(e)

    if country_code == "ZA_PL":
        try:
            scraper_peps_south_africa_provincial_legislators_api()
            return {"message": "Success"}
        except Exception as e:
            print(e)

    if country_code == "TH":
        try:
            scrape_peps_thailandia_api()
            return {"message": "Success"}
        except Exception as e:
            print(e)

    if country_code == "US_PLUM":
        try:
            scrape_peps_usa_plum_api()
            return {"message": "Success"}
        except Exception as e:
            print(e)

    if country_code == "US_WL":
        try:
            scrape_peps_usa_cia_world_liders_api()
            return {"message": "Success"}
        except Exception as e:
            print(e)

    if country_code == "US_CM":
        try:
            scrape_peps_usa_members_congress_api()
            return {"message": "Success"}
        except Exception as e:
            print(e)

    if country_code == "US_NL":
        try:
            scrape_peps_us_navy_leadership_api()
            return {"message": "Success"}
        except Exception as e:
            print(e)
    if country_code == "US_ST":
            try:
                scrape_peps_us_state_department_api()
                return {"message": "Success"}
            except Exception as e:
                print(e)

    if country_code == "UY":
        try:
            scrape_peps_uruguay_api()
            return {"message": "Success"}
        except Exception as e:
            print(e)

    if country_code == "VE":
        try:
            scrape_peps_venezuela()
            return {"message": "Success"}
        except Exception as e:
            print(e)

    if country_code == "WQS":
        try:
            wikidata_query_service_api()
            return {"message": "Success"}
        except Exception as e:
            print(e)

    if country_code == "SG":
        try:
            await scrape_peps_singapore()
            return {"message": "Success"}
        except Exception as e:
            print(e)
            return {"message": "Error", "detail": str(e)}

    return {"message": "Country not supported"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)