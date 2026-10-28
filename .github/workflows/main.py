import os
import requests

def run():
    tibber_token = os.environ.get("TIBBER_TOKEN")
    
    if not tibber_token:
        print("Fehler: TIBBER_TOKEN ist nicht gesetzt!")
        return

    print("Starte Tibber-Preisabfrage...")

    url = "https://api.tibber.com/v1-beta/gql"
    headers = {
        "Authorization": f"Bearer {tibber_token}",
        "Content-Type": "application/json"
    }
    
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
        }
      }
    }
    """

    try:
        response = requests.post(url, json={'query': query}, headers=headers)
        if response.status_code == 200:
            data = response.json()
            current_price = data['data']['viewer']['homes'][0]['currentSubscription']['priceInfo']['current']['total']
            preis_cent = current_price * 100
            print(f"Aktueller Tibber-Strompreis: {preis_cent:.2f} Cent / kWh")
            
            preis_grenze = 25.0
            
            if preis_cent <= preis_grenze:
                print(f"Preis ({preis_cent:.2f} Ct) ist unter der Grenze von {preis_grenze} Ct. Speicher soll geladen werden.")
                # Hier binden wir im nächsten Schritt die Zendure-API-Befehle ein
            else:
                print(f"Preis ({preis_cent:.2f} Ct) ist zu hoch. Keine Lade-Aktion erforderlich.")
                
        else:
            print(f"Fehler bei der API-Abfrage: Statuscode {response.status_code}")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

if __name__ == "__main__":
    run()
