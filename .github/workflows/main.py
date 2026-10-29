import os
import requests

def run():
    tibber_token = os.environ.get("TIBBER_TOKEN")
    zendure_email = os.environ.get("ZENDURE_EMAIL")
    zendure_password = os.environ.get("ZENDURE_PASSWORD")
    
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
                print(f"Preis ({preis_cent:.2f} Ct) ist unter {preis_grenze} Ct. Aktiviere Zendure Ladevorgang...")
                
                # Hier greifen wir auf deine Zendure-Zugangsdaten zu
                if zendure_email and zendure_password:
                    print("Zendure-Zugangsdaten vorhanden. Verbindung wird aufgebaut...")
                    # Anbindung an die Zendure Cloud API zum Starten des Ladens
                else:
                    print("Hinweis: Zendure E-Mail oder Passwort sind noch nicht als Secrets hinterlegt.")
            else:
                print(f"Preis ({preis_cent:.2f} Ct) ist zu hoch. Keine Lade-Aktion erforderlich.")
                
        else:
            print(f"Fehler bei der API-Abfrage: Statuscode {response.status_code}")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

if __name__ == "__main__":
    run()
