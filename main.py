import json

print("Skript wird ausgeführt...")

web_data = {
    "price": 24.50,
    "power": 150,
    "status": "Läuft stabil"
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(web_data, f)

print("data.json erfolgreich geschrieben.")
