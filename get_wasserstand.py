import os
import requests
from datetime import datetime
import csv
from pathlib import Path

# --- CONFIGURATION ---
URL = "https://www.hochwasserportal.nrw.de/data/internet/stations/104/2728759000100/S/week.json"
THRESHOLD = 75.0  # Set your limit in cm
NTFY_TOPIC = os.getenv("NTFY_TOPIC") # Pulls from GitHub Secrets

headers = {
    "Accept": "application/json",
    "User-Agent": "agger-bot/1.0",
    "Referer": "https://www.hochwasserportal.nrw.de/webpublic/",
}

# Paths
base_path = Path(__file__).parent
csv_path = base_path / "agger_wasserstand.csv"
flag_path = base_path / ".alert_sent"

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

# 2. THRESHOLD & SPAM LOGIC
if current_val > THRESHOLD:
    if not flag_path.exists():
        send_ntfy_alert(current_val)
        flag_path.touch() # Create the "lock" file
    else:
        print("Still above threshold, but alert already sent.")
else:
    if flag_path.exists():
        print("Water level back to normal. Resetting alert flag.")
        flag_path.unlink() # Delete the flag so we can alert again next time

# 3. SAVE TO CSV
datum = dt.strftime("%d.%m.%Y")
zeit = dt.strftime("%H:%M")
fieldnames = ["Datum", "Zeit", "Wert", "Einheit", "Station", "Zeit der Abfrage"]

row = {
    "Datum": datum,
    "Zeit": zeit,
    "Wert": current_val,
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

print(f"Logged: {row}")