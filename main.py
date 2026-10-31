import os
import json
import urllib.request
import urllib.error
import sys

def run():
    try:
        tibber_token = os.environ.get("TIBBER_TOKEN")
        
        price_val = 43.78  
        power_val = 200    # Stabiler Standardwert für den Verbrauch
        status_text = "Aktiv (Stabil)"

        if not tibber_token:
            print("TIBBER_TOKEN nicht gefunden, verwende Fallback.")
        else:
            print("Starte sichere Tibber-Abfrage...")
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
                            price_info = homes[0].get('currentSubscription', {}).get('priceInfo', {}).get('current', {})
                            if price_info and 'total' in price_info:
                                price_val = round(price_info['total'] * 100, 2)
                                status_text = "Aktiv (Tibber Live)"
                                print(f"Preis erfolgreich abgerufen: {price_val} Ct")
            except Exception as api_err:
                print(f"Tibber API Hinweis: {api_err}")

        web_data = {
            "price": price_val,
            "power": power_val,
            "status": status_text
        }
        
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(web_data, f)
        print("data.json erfolgreich gespeichert.")

    except Exception as e:
        print(f"Fehler abgefangen: {e}")
        web_data = {"price": 43.78, "power": 200, "status": "Notfall-Fallback"}
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(web_data, f)

    sys.exit(0)

if __name__ == "__main__":
    run()
