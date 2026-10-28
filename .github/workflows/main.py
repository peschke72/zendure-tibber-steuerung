import os
import requests

def run():
    # Tibber API Token aus den GitHub Secrets auslesen
    tibber_token = os.environ.get("TIBBER_TOKEN")
    
    if not tibber_token:
        print("Fehler: TIBBER_TOKEN ist nicht gesetzt!")
        return

    print("Starte Tibber-Preisabfrage...")
    
    # Hier binden wir gleich die Abfrage für die aktuellen Preise ein
    # (Das Skript wird Schritt für Schritt erweitert)

if __name__ == "__main__":
    run()
