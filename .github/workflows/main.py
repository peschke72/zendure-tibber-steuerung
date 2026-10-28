import os
import requests

def run():
    tibber_token = os.environ.get("TIBBER_TOKEN")
    
    if not tibber_token:
        print("Fehler: TIBBER_TOKEN ist nicht gesetzt!")
        return

    print("Starte Tibber-Preisabfrage...")

    # Tibber GraphQL API Abfrage für den aktuellen Preis
    url = "https://api.tibber.com/v1-beta/gql"
    headers = {
        "Authorization": f"Bearer {tibber_token}",
        "Content-Type": "application/json"
    }
    
    # GraphQL Query für den aktuellen Strompreis
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
            # Preis aus der Antwort extrahieren
            current_price = data['data']['viewer']['homes'][0]['currentSubscription']['priceInfo']['current']['total']
            print(f"Aktueller Tibber-Strompreis: {current_price * 100:.2f} Cent / kWh")
            
            # Hier bauen wir im nächsten Schritt die Logik für deinen Zendure-Speicher ein!
        else:
            print(f"Fehler bei der API-Abfrage: Statuscode {response.status_code}")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

if __name__ == "__main__":
    run()
