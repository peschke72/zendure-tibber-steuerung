import os
import json
import urllib.request
import urllib.error
import sys

def run():
    try:
        tibber_token = os.environ.get("TIBBER_TOKEN")
        
        price_val = 43.78  
        power_val = 0      # Startwert
        status_text = "Aktiv (Tibber)"

        if not tibber_token:
            print("TIBBER_TOKEN nicht gefunden, verwende Fallback.")
        else:
            print("Starte Tibber-Abfrage...")
            url = "https://api.tibber.com/v1-beta/gql"
            headers = {
                "Authorization": f"Bearer {tibber_token}",
                "Content-Type": "application/json"
            }
            
            # Abfrage für Preis und den letzten Verbrauchswert
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
                            # Preis auslesen
                            price_info = homes[0].get('currentSubscription', {}).get('priceInfo', {}).get('current', {})
                            if price_info and price_info.get('total') is not None:
                                price_val = round(price_info['total'] * 100, 2)
                            
                            # Letzten Verbrauch auslesen (in kWh, umgerechnet in Watt oder als Basis)
                            consumption_nodes = homes[0].get('consumption', {}).get('nodes', [])
                            if consumption_nodes and consumption_nodes[0].get('consumption') is not None:
                                kwh = consumption_nodes[0]['consumption']
                                # Da HOURLY-Verbrauch in kWh pro Stunde vorliegt, entspricht das dem Durchschnitt in kW -> in Watt umrechnen
                                power_val = int(kwh * 1000)
                                status_text = "Aktiv (Tibber)"
                            
                            print(f"Abruf erfolgreich: {price_val} Ct, ~{power_val} W")
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
        web_data = {"price": 43.78, "power": 0, "status": "Fallback"}
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(web_data, f)

    sys.exit(0)

if __name__ == "__main__":
    run()
