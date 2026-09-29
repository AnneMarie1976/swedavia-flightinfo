import requests
import json
from datetime import datetime
from destinationer import ladda_city_country_db, analysera_destinationer
from rich.console import Console
from rich.table import Table

console = Console()

SWEDAVIA_BASE_URL = "https://api.swedavia.se/flightinfo/v2"
API_KEY = "DIN_API_NYCKEL_HÄR"

FLYGPLATSER = {
    "1": ("Stockholm Arlanda", "ARN"),
    "2": ("Göteborg Landvetter", "GOT"),
    "3": ("Bromma Stockholm", "BMA"),
    "4": ("Malmö Airport", "MMX"),
    "5": ("Luleå Airport", "LLA"),
    "6": ("Umeå Airport", "UME"),
    "7": ("Visby Airport", "VBY"),
    "8": ("Åre Östersund Airport", "OSD"),
    "9": ("Ronneby Airport", "RNB"),
    "10": ("Kiruna Airport", "KRN")
}

IDAG = datetime.now().strftime("%Y-%m-%d")

# Mock-data med realistiska statusar för demonstration
MOCK_FLYG = [
    {
        "flightId": "SK1415",
        "departureArrival": "A",
        "locationAndDate": {"flightLeg": {"targetAirportName": "London", "scheduledTimeUTC": f"{IDAG}T10:30:00Z"}},
        "airlineOperator": {"name": "SAS"},
        "time": f"{IDAG} 10:30",
        "status": "ON_TIME"
    },
    {
        "flightId": "LH2418",
        "departureArrival": "A",
        "locationAndDate": {"flightLeg": {"targetAirportName": "Frankfurt", "scheduledTimeUTC": f"{IDAG}T11:15:00Z"}},
        "airlineOperator": {"name": "Lufthansa"},
        "time": f"{IDAG} 11:15",
        "status": "DELAYED"
    },
    {
        "flightId": "DY4001",
        "departureArrival": "D",
        "locationAndDate": {"flightLeg": {"targetAirportName": "Bucharest", "scheduledTimeUTC": f"{IDAG}T12:00:00Z"}},
        "airlineOperator": {"name": "Norwegian"},
        "time": f"{IDAG} 12:00",
        "status": "CANCELLED"
    }
]

def hämta_api_headers():
    return {
        "Accept": "application/json",
        "Ocp-Apim-Subscription-Key": API_KEY
    }

def hämta_status_sträng(status_kod):
    """Returnerar färgkodad statussträng baserad på flygets status."""
    status_kod = str(status_kod).upper()
    if status_kod in ["ON_TIME", "SCHEDULED", "LANDED", "OK"]:
        return "[bold green]🟢 I tid[/bold green]"
    elif status_kod in ["DELAYED", "LATE"]:
        return "[bold yellow]🟡 Försenat[/bold yellow]"
    elif status_kod in ["CANCELLED", "INSTÄLLT"]:
        return "[bold red]🔴 Inställt[/bold red]"
    else:
        return f"[white]⚪ {status_kod}[/white]"

def hämta_flygdata(flygplats_kod, typ="arrivals", datum=None, odata_fråga=""):
    """Hämtar flygdata med valfritt datum och OData-query parameters."""
    url = f"{SWEDAVIA_BASE_URL}/{typ}/{flygplats_kod}"
    
    if datum:
        url += f"/{datum}"

    if odata_fråga:
        url += f"?{odata_fråga}"

    try:
        response = requests.get(url, headers=hämta_api_headers(), timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            console.print(f"[yellow]ℹ️ (Status {response.status_code}: Använder offline demodata för {flygplats_kod})[/yellow]")
            return {"flights": MOCK_FLYG}
    except Exception:
        console.print("[yellow]ℹ️ (Nätverksfel – Använder offline demodata)[/yellow]")
        return {"flights": MOCK_FLYG}

def visa_flyg_tabell(flyg_data, rubrik="Flyginformation"):
    """Skriver ut flygdata i en snygg färgstark tabell med Rich inklusive Status."""
    table = Table(title=rubrik, show_header=True, header_style="bold magenta")
    table.add_column("Flight ID", style="cyan", justify="center")
    table.add_column("Flygbolag", style="green")
    table.add_column("Destination / Ursprung", style="yellow")
    table.add_column("Datum & Tid (UTC)", style="bold white", justify="center")
    table.add_column("Status", justify="center")

    city_db = ladda_city_country_db()

    for flyg in flyg_data.get("flights", []):
        flight_id = flyg.get("flightId", "N/A")
        bolag = flyg.get("airlineOperator", {}).get("name", "Okänt")
        
        loc_date = flyg.get("locationAndDate", {}).get("flightLeg", {})
        stad = loc_date.get("targetAirportName", "Okänd")
        land = city_db.get(stad, "Okänt land")
        
        tid = loc_date.get("scheduledTimeUTC", flyg.get("time", "N/A"))
        if "T" in tid:
            tid = tid.replace("T", " ").replace("Z", "")

        # Hantera status från API eller mock-data
        raw_status = flyg.get("status") or loc_date.get("status", "ON_TIME")
        formatted_status = hämta_status_sträng(raw_status)

        table.add_row(flight_id, bolag, f"{stad} ({land})", tid, formatted_status)

    console.print(table)

def kontrollera_api_status():
    console.print("\n[bold blue]🔍 Kontrollerar API-status...[/bold blue]")
    res = hämta_flygdata("ARN", "arrivals")
    if res and res.get("flights") != MOCK_FLYG:
        console.print("[bold green]✅ API:et är ONLINE och svarar med live-data![/bold green]")
    else:
        console.print("[bold yellow]⚠️ Demoläget är aktivt (offline-svar)[/bold yellow]")

def visa_huvudmeny():
    console.print("\n[bold cyan]==========================================[/bold cyan]")
    console.print("[bold cyan]✈️  SWEDAVIA FLIGHTINFO V2 TERMINALAPP  ✈️[/bold cyan]")
    console.print("[bold cyan]==========================================[/bold cyan]")
    print("1. Visa ankomster (Arrivals)")
    print("2. Visa avgångar (Departures)")
    print("3. Sök efter ett specifikt flyg")
    print("4. Kör Date/Time OData-fråga (Filtrera på datum/tid)")
    print("5. Kontrollera API-status")
    print("6. Kör automatisk demonstration")
    print("0. Avsluta")
    console.print("[bold cyan]------------------------------------------[/bold cyan]")

def välj_flygplats():
    print("\nVälj flygplats:")
    for nr, (namn, kod) in FLYGPLATSER.items():
        print(f"{nr}. {namn} ({kod})")
    
    val = input("Mata in nummer (1-10) [Standard: 1 - Arlanda]: ").strip()
    if val in FLYGPLATSER:
        return FLYGPLATSER[val][1]
    return "ARN"

def välj_datum():
    svar = input(f"Ange datum (YYYY-MM-DD) [Tryck Enter för idag: {IDAG}]: ").strip()
    if svar:
        return svar
    return IDAG

def kör_demo():
    console.print("\n[bold green]🤖 --- STARTAR AUTOMATISK DEMONSTRATION ---[/bold green]")
    console.print(f"1. Hämtar ankomster för Arlanda (ARN) för datum {IDAG}...")
    data = hämta_flygdata("ARN", "arrivals", datum=IDAG)
    
    visa_flyg_tabell(data, f"Demonstration: Ankomster Arlanda ({IDAG})")
    
    city_db = ladda_city_country_db()
    resultat = analysera_destinationer(data.get("flights", []), city_db)
    console.print(f"\n[bold green]2. Analyserade unika destinationer:[/bold green] {len(resultat)} städer identifierade i JSON-databasen.")
    console.print("[bold green]✅ Demonstration klar![/bold green]\n")

def main():
    while True:
        visa_huvudmeny()
        val = input("Välj ett alternativ (0-6): ").strip()

        if val == "1":
            kod = välj_flygplats()
            datum = välj_datum()
            data = hämta_flygdata(kod, "arrivals", datum=datum)
            visa_flyg_tabell(data, f"Ankomster - {kod} ({datum})")
        
        elif val == "2":
            kod = välj_flygplats()
            datum = välj_datum()
            data = hämta_flygdata(kod, "departures", datum=datum)
            visa_flyg_tabell(data, f"Avgångar - {kod} ({datum})")

        elif val == "3":
            kod = välj_flygplats()
            sök_nr = input("Mata in flightnummer (t.ex. SK1415): ").strip().upper()
            data = hämta_flygdata(kod, "arrivals")
            filtrerade = [f for f in data.get("flights", []) if f.get("flightId") == sök_nr]
            visa_flyg_tabell({"flights": filtrerade}, f"Sökresultat för {sök_nr}")
        
        elif val == "4":
            kod = välj_flygplats()
            console.print(f"[dim]Exempel på Date/Time OData-filter:[/dim]")
            console.print(f"[dim] - $filter=flightLeg/scheduledTimeUTC ge {IDAG}T00:00:00Z[/dim]")
            odata = input("Mata in OData query parameter: ").strip()
            data = hämta_flygdata(kod, "arrivals", odata_fråga=odata)
            visa_flyg_tabell(data, f"OData Date/Time Resultat - {kod}")

        elif val == "5":
            kontrollera_api_status()

        elif val == "6":
            kör_demo()

        elif val == "0":
            console.print("\n[bold red]Tack för idag! Avslutar applikationen.[/bold red]")
            break
        else:
            console.print("[bold red]❌ Ogiltigt val, försök igen.[/bold red]")

if __name__ == "__main__":
    main()