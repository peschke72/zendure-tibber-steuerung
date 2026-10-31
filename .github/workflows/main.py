import os
import json
import requests

def run():
    tibber_token = os.environ.get("TIBBER_TOKEN")
    
    price_val = 24.50  # Fallback-Wert, falls die API nicht erreichbar ist
    status_text = "Verbunden"

    if not tibber_token:
        print("Hinweis: TIBBER_TOKEN nicht gefunden, verwende Fallback-Werte.")
        status_text = "Token fehlt"
    else:
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
                  }
                }
              }
            }
          }
        }
        """
        try:
            response = requests.post(url, json={'query': query}, headers=headers)
            print(f"API Status Code: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                homes = result.get('data', {}).get('viewer', {}).get('homes', [])
                if homes:
                    current_price = homes[0]['currentSubscription']['priceInfo']['current']['total']
                    price_val = round(current_price * 100, 2)
                    status_text = "Aktiv (Tibber Live)"
                    print(Preis erfolgreich abgerufen: {price_val} Ct)
        except Exception as e:
            print(f"Fehler bei der Abfrage: {e}")
            status_text = "API-Fehler"

    # In jedem Fall die data.json schreiben, damit die Webseite Daten hat
    web_data = {
        "price": price_val,
        "power": 0,
        "status": status_text
    }
    
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(web_data, f)
    print("data.json erfolgreich geschrieben.")

if __name__ == "__main__":
    run()
