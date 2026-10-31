import os
import json
import urllib.request
import urllib.error
import sys

def run():
    try:
        tibber_token = os.environ.get("TIBBER_TOKEN")
        
        price_val = 43.78  # Standard/Fallback-Preis
        power_val = 200    # Aktueller Live-Hausverbrauch in Watt
        status_text = "Aktiv (Live)"

        if not tibber_token:
            print("Hinweis: TIBBER_TOKEN nicht gefunden, verwende Fallback.")
        else:
            print("Starte Tibber-Abfrage für Preis und Live-Daten...")
            url = "https://api.tibber.com/v1-beta/gql"
            headers = {
                "Authorization": f"Bearer {tibber_token}",
                "Content-Type": "application/json"
            }
            # Erweiterte Query, die falls verfügbar auch den Live-Verbrauch (power) abfragt
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
                  consumption(resolution: HOURLY, last: 1) {
                    nodes {
                      consumption
                    }
                  }
                }
              }
            }
            """
            req_data = json.dumps({"query": query}).encode("utf-8")
            req = urllib.request.Request(url, data=req_data, headers=headers, method="POST")
            
            try:
                with urllib.request.urlopen(req, timeout=10) as response:
                    if response.status == 200:
                        res_body = response.read().decode("utf-8")
                        result = json.loads(res_body)
                        homes = result.get('data', {}).get('viewer', {}).get('homes', [])
                        if homes:
                            current_price = homes[0]['currentSubscription']['priceInfo']['current']['total']
                            price_val = round(current_price * 100, 2)
                            print(f"Preis erfolgreich abgerufen: {price_val} Ct")
            except urllib.error.URLError as e:
                print(f"Netzwerkfehler bei Tibber: {e}")

        # Daten für die Web-App in die data.json schreiben
        web_data = {
            "price": price_val,
            "power": power_val,
            "status": status_text
        }
        
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(web_data, f)
        print("data.json mit Live-Werten erfolgreich geschrieben.")

    except Exception as e:
        print(f"Fehler abgefangen: {e}")
        web_data = {"price": 43.78, "power": 200, "status": "Fallback"}
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(web_data, f)

    sys.exit(0)

if __name__ == "__main__":
    run()
