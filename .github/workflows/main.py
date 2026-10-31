import os
import json
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

    price_val = 0.0
    status_text = "Verbunden"

    try:
        response = requests.post(url, json={'query': query}, headers=headers)
        print(f"Tibber API Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            homes = result.get('data', {}).get('viewer', {}).get('homes', [])
            if homes:
                home = homes[0]
                current_sub = home.get('currentSubscription')
                if current_sub and current_sub.get('priceInfo'):
                    current_price = current_sub['priceInfo']['current']['total']
                    price_val = round(current_price * 100, 2)
                    print(f"Aktueller Strompreis: {price_val} Cent / kWh")
                    status_text = "Aktiv (Verbunden)"
                else:
                    status_text = "Keine Preisinfo gefunden"
            else:
                status_text = "Kein Zuhause gefunden"
        else:
            status_text = f"API Fehler {response.status_code}"
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
        status_text = "Skript-Fehler"

    # JSON-Daten für die Weboberfläche schreiben
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
