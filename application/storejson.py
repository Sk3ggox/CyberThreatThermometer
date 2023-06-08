import json

try:
    with open("alerts_db.json", "r") as db_file:
        database = json.load(db_file)
except FileNotFoundError:
    database = []
except json.decoder.JSONDecodeError:
    database = []

with open("snort_response.json", "r") as file:
    json_data = json.load(file)

    for analyses in json_data["analyses"]:
        for alert in analyses["alerts"]:
            useful_info = {
                "timestamp": alert["timestamp"],
                "sid": alert["sid"],
                "priority": alert["priority"],
                "message": alert["message"],
                "source": alert["source"],
                "destination": alert["destination"],
                "protocol": alert["protocol"],
                "classtype": alert["classtype"],
            }

            database.append(useful_info)

with open("alerts_db.json", "w") as db_file:
    json.dump(database, db_file, indent=1)
