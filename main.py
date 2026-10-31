import os
import json
import urllib.request
import urllib.error
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
                            status_text = "Aktiv (Tibber Live)"
                            print(f"Preis erfolgreich abgerufen: {price_val} Ct")
            except urllib.error.URLError as e:
                print(f"Netzwerkfehler bei Tibber: {e}")
                status_text = "API-Fehler"

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
        web_data = {"price": 24.50, "power": 0, "status": "Notfall-Fallback"}
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(web_data, f)

    sys.exit(0)

if __name__ == "__main__":
    run()
