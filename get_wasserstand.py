import requests
from datetime import datetime
import csv
from pathlib import Path

URL = "https://www.hochwasserportal.nrw.de/data/internet/stations/104/2728759000100/S/week.json"
headers = {
    "Accept": "application/json",
    "User-Agent": "agger-bot/1.0",
    "Referer": "https://www.hochwasserportal.nrw.de/webpublic/",
}

r = requests.get(URL, headers=headers, timeout=30)
r.raise_for_status()
payload = r.json()

obj = payload[0]
station_name = obj["station_name"]
unit = obj.get("ts_unitsymbol", "cm")

# latest datapoint
last_ts, last_val = obj["data"][-1]
dt = datetime.fromisoformat(last_ts)  # timezone-aware

datum = dt.strftime("%d.%m.%Y")
zeit = dt.strftime("%H:%M")

# CSV next to this script
csv_path = Path(__file__).with_name("agger_wasserstand.csv")

# German column titles
fieldnames = ["Datum", "Zeit", "Wert", "Einheit", "Station", "Zeit der Abfrage"]

row = {
    "Datum": datum,
    "Zeit": zeit,
    "Wert": last_val,
    "Einheit": unit,
    "Station": station_name,
    "Zeit der Abfrage": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
}

file_exists = csv_path.exists()
with csv_path.open("a", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
    if not file_exists:
        writer.writeheader()
    writer.writerow(row)

print(f"Gespeichert in {csv_path}: {row}")