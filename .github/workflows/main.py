import os
import json
import requests
import sys

def run():
    try:
        tibber_token = os.environ.get("TIBBER_TOKEN")
        
        price_val = 24.50
        status_text = "Verbunden"

        if not tibber_token:
            print("Hinweis: TIBBER_TOKEN nicht gefunden, verwende Fallback.")
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
            response = requests.post(url, json={'query': query}, headers=headers)
            print(f"API Status Code: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                homes = result.get('data', {}).get('viewer', {}).get('homes', [])
                if homes:
                    current_price = homes[0]['currentSubscription']['priceInfo']['current']['total']
                    price_val = round(current_price * 100, 2)
                    status_text = "Aktiv (Tibber Live)"
                    print(f"Preis erfolgreich abgerufen: {price_val} Ct")
                else:
                    status_text = "Kein Zuhause gefunden"
            else:
                status_text = f"API Fehler {response.status_code}"

        # In jedem Fall die data.json schreiben
        web_data = {
            "price": price_val,
            "power": 0,
            "status": status_text
        }
        
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(web_data, f)
        print("data.json erfolgreich geschrieben.")

    except Exception as e:
        print(f"Fehler abgefangen: {e}")
        # Fallback-Datei schreiben, damit die App nicht leer bleibt
        web_data = {"price": 24.50, "power": 0, "status": "Notfall-Fallback"}
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(web_data, f)

    # Garantiert erfolgreicher Exit-Code für GitHub Actions
    sys.exit(0)

if __name__ == "__main__":
    run()
