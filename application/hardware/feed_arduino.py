import serial
from datetime import datetime, timedelta
import json
import time

ser = serial.Serial('COM7', 9600)

while True:
    current_time = datetime.now()
    ten_minutes_ago = current_time - timedelta(minutes=10)

    with open("application\\alerts_db.json", "r") as file:
        database = json.load(file)

    filtered_data = []
    for data in database:
        if ten_minutes_ago <= datetime.fromisoformat(data["timestamp"]):
            filtered_data.append(data)

    threat_value = 0

    for alert in filtered_data:
        if alert["priority"] == 1:
            threat_value = threat_value + 10
        elif alert["priority"] == 2:
            threat_value = threat_value + 7
        elif alert["priority"] == 3:
            threat_value = threat_value + 4
        else:
            threat_value = threat_value + 1

    ser.write(str(threat_value).encode())
    time.sleep(0.1)