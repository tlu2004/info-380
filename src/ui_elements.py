import requests
from alerts import get_static_alert
from datetime import datetime
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer
from fetch_data import fetch_911_calls

def get_location():
    try:
        res = requests.get("http://ip-api.com/json").json()
        return f"{res['city']}, {res['regionName']}, {res['country']}"
    except:
        return "Location Unavailable"

def get_weather():
    return "🌤️ 65°F, Clear Skies"

def get_battery_status():
    try:
        import psutil
        battery = psutil.sensors_battery()
        return f"🔋 {battery.percent}% {'(Charging)' if battery.power_plugged else ''}"
    except:
        return "Battery 100%"

class InfoOverlay:
    def __init__(self, parent):
        self.labels = []
        y_positions = [20, 60, 100, 140]
        for i in range(4):
            label = QLabel(parent)
            label.setGeometry(650, y_positions[i], 240, 30)
            label.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 100); padding: 5px;")
            label.setFont(QFont("Arial", 10))
            self.labels.append(label)

        self.update_all()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_all)
        self.timer.start(10000)

    def update_all(self):
        self.labels[0].setText(f"📍 {get_location()}")
        self.labels[1].setText(f"{get_weather()}")
        self.labels[2].setText(f"{get_battery_status()}")
        self.labels[3].setText(f"🕒 {datetime.now().strftime('%I:%M:%S %p')}")

class AlertsOverlay:
    def __init__(self, parent):
        self.alert_label = QLabel(parent)
        self.alert_label.setGeometry(650, 420, 240, 60)
        self.alert_label.setStyleSheet(
            "color: black; background-color: lightgrey; border: 1px solid black; padding: 5px;"
        )
        self.alert_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.alert_label.setWordWrap(True)
        self.alert_label.raise_()

        self.update_alert()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_alert)
        self.timer.start(30000)

    def update_alert(self):
        try:
            # Get approximate lat/lon from IP
            res = requests.get("http://ip-api.com/json").json()
            lat, lon = float(res["lat"]), float(res["lon"])

            # Fetch 911 data
            df = fetch_911_calls(limit=1, lat=lat, lon=lon)

            if not df.empty:
                row = df.iloc[0]
                time = row["datetime"].strftime("%I:%M %p")
                address = row["address"]
                description = row["description"]
                alert_text = f"🚨 {description}\n📍 {address}\n🕒 {time}"
            else:
                alert_text = "✅ No recent nearby 911 incidents"

        except Exception as e:
            alert_text = "⚠️ Failed to load alert data"

        self.alert_label.setText(alert_text)