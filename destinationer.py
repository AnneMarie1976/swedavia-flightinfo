import json
import os

def ladda_city_country_db(filnamn="city_country.json"):
    """Läs in offline-databasen med städer och länder från samma mapp som skriptet."""
    # Hämtar mappen där denna fil (destinationer.py) ligger
    mapp_sökväg = os.path.dirname(os.path.abspath(__file__))
    full_sökväg = os.path.join(mapp_sökväg, filnamn)

    try:
        with open(full_sökväg, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Varning: Filen {filnamn} hittades inte på {full_sökväg}. Använder tom databas.")
        return {}

def analysera_destinationer(flyg_lista, city_country_db, sök_filter=None):
    """
    Tar emot flygdata från API:et och sammanställer destinationer.
    Kan filtreras på land eller stadsnamn.
    """
    statistik = {}

    for flyg in flyg_lista:
        # Hämta stadsnamn från flyginformationen
        stad = flyg.get("locationAndDate", {}).get("flightLeg", {}).get("targetAirportName", "Okänd")
        
        # Slå upp land i vår offline JSON-databas
        land = city_country_db.get(stad, "Okänt land")

        # Filtrering om användaren har sökt på land eller stad
        if sök_filter:
            sök_filter_low = sök_filter.lower()
            if sök_filter_low not in stad.lower() and sök_filter_low not in land.lower():
                continue

        # Räkna antalet flygningar per destination
        if stad not in statistik:
            statistik[stad] = {
                "land": land,
                "antal_flyg": 1
            }
        else:
            statistik[stad]["antal_flyg"] += 1

    return statistik

if __name__ == "__main__":
    db = ladda_city_country_db()
    unika_länder = set(db.values())
    print(f"Databas laddad: {len(db)} städer och {len(unika_länder)} unika länder.")