import os
import json
import requests

def run():
    tibber_token = os.environ.get("TIBBER_TOKEN")
    zendure_email = os.environ.get("ZENDURE_EMAIL")
    zendure_password = os.environ.get("ZENDURE_PASSWORD")
    
    if not tibber_token:
        print("Fehler: TIBBER_TOKEN ist nicht gesetzt!")
        return

    print("Starte Tibber-Datenabfrage...")

    url = "https://api.tibber.com/v1-beta/gql"
    headers = {
        "Authorization": f"Bearer {tibber_token}",
        "Content-Type": "application/json"
    }
    
    # GraphQL Query für Preis und Live-Verbrauch
    query = """
    {
      viewer {
        homes {
          currentSubscription {
            priceInfo {
              current {
                total
                startsAt
              }
            }
          }
          liveMeasurement {
            power
            timestamp
          }
        }
      }
    }
    """

    try:
        response = requests.post(url, json={'query': query}, headers=headers)
        if response.status_code == 200:
            data = response.json()
            home = data['data']['viewer']['homes'][0]
            
            # Strompreis auslesen
            current_price = home['currentSubscription']['priceInfo']['current']['total']
            preis_cent = current_price * 100
            
            # Live-Verbrauch auslesen (falls verfügbar)
            live_data = home.get('liveMeasurement')
            power = live_data['power'] if live_data else 0
            
            print(f"Aktueller Strompreis: {preis_cent:.2f} Cent / kWh | Verbrauch: {power} W")
            
            # JSON-Daten für die Weboberfläche schreiben
            web_data = {
                "price": round(preis_cent, 2),
                "power": power,
                "status": "Aktiv (Verbunden)"
            }
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(web_data, f)
            print("data.json erfolgreich aktualisiert.")

            # Steuerungslogik
            preis_grenze = 25.0
            if preis_cent <= preis_grenze:
                print(f"Preis ({preis_cent:.2f} Ct) ist unter {preis_grenze} Ct. Ladevorgang prüfen...")
            else:
                print(f"Preis ({preis_cent:.2f} Ct) ist zu hoch.")
                
        else:
            print(f"Fehler bei der API-Abfrage: Statuscode {response.status_code}")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

if __name__ == "__main__":
    run()
