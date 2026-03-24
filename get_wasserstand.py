import os
import requests
from datetime import datetime, timedelta
import csv
from pathlib import Path
import json

# --- CONFIGURATION ---
URL = "https://www.hochwasserportal.nrw.de/data/internet/stations/104/2728759000100/S/week.json"
THRESHOLD = 150.0  # limit in cm
NTFY_TOPIC = os.getenv("NTFY_TOPIC") # Pulls from GitHub Secrets

headers = {
    "Accept": "application/json",
    "User-Agent": "agger-bot/1.0",
    "Referer": "https://www.hochwasserportal.nrw.de/webpublic/",
}

# Paths
base_path = Path(__file__).parent
csv_path = base_path / "agger_wasserstand.csv"

def send_ntfy_alert(val):
    if not NTFY_TOPIC:
        print("No NTFY_TOPIC found. Skipping notification.")
        return
    
    try:
        requests.post(
            f"https://ntfy.sh/{NTFY_TOPIC}",
            data=f"⚠️ Agger Alarm! Wasserstand: {val} cm".encode("utf-8"),
            headers={
                "Title": "Hochwasser Warnung",
                "Priority": "high",
                "Tags": "warning,ocean"
            }
        )
        print("Notification sent!")
    except Exception as e:
        print(f"Failed to send notification: {e}")

# 1. FETCH DATA
r = requests.get(URL, headers=headers, timeout=30)
r.raise_for_status()
payload = r.json()

obj = payload[0]
station_name = obj["station_name"]
unit = obj.get("ts_unitsymbol", "cm")

# latest datapoint
last_ts, last_val = obj["data"][-1]
current_val = float(last_val)
dt = datetime.fromisoformat(last_ts)

# 2. THRESHOLD CHECK
if current_val > THRESHOLD:
    send_ntfy_alert(current_val)
    print(f"ALARM! {current_val} cm ist über {THRESHOLD} cm.")
else:
    print(f"Normalstand: {current_val} cm.")

# 3. SAVE TO CSV
german_time = datetime.now() + timedelta(hours=1)  # Convert to German time (UTC+1)
current_date = dt.strftime("%d.%m.%Y")
current_time = dt.strftime("%H:%M")
fieldnames = ["Datum", "Zeit", "Wert", "Einheit", "Station", "Zeit der Abfrage"]

current_val_german = f"{current_val:.1f}".replace(".", ",")

row = {
    "Datum": current_date,
    "Zeit": current_time,
    "Wert": current_val_german,
    "Einheit": unit,
    "Station": station_name,
    "Zeit der Abfrage": german_time.strftime("%d.%m.%Y %H:%M:%S") + " (UTC+1)",
}

file_exists = csv_path.exists()
with csv_path.open("a", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
    if not file_exists:
        writer.writeheader()
    writer.writerow(row)

print(f"Logged: {row}")

def update_wasserstand_dashboard():
    """Liest die Wasserstandsdaten aus der CSV-Datei und aktualisiert das Dashboard."""
    csv_path = base_path / "agger_wasserstand.csv"
    dashboard_data = []

    if not csv_path.exists():
        print("CSV-Datei nicht gefunden. Dashboard wird nicht aktualisiert.")
        return
    
    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        rows = list(reader)

        for row in rows[-150:]: #
            try:
                wert = float(row["Wert"].replace(",", "."))
                dashboard_data.append({
                    "label": f"{row['Datum']} {row['Zeit']}",
                    "pegel": wert
                })
            except ValueError:
                continue

    json_path = base_path / "dashboard_data.json"
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(dashboard_data, f, ensure_ascii=False, indent=2)
    print(f"Dashboard aktualisiert mit {len(dashboard_data)} Einträgen.")

if __name__ == "__main__":
    update_wasserstand_dashboard()