import re
from datetime import datetime, timedelta
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from subprocess import Popen, DEVNULL

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"]
)

def remove_lines():
    threshold_time = datetime.now() - timedelta(minutes=4)
    print(threshold_time)
    pattern = r'(\d{2}\/\d{1,2}-\d{2}:\d{2}:\d{2}\.\d{6}).*'
    
    with open("/var/log/snort/alert", "r") as file, open("/var/log/snort/alert", "w") as file_write:
        for line in file:
            timestamp = datetime.strptime(str(datetime.now().year) + "/" + re.match(pattern, line).group(1), "%Y/%m/%d-%H:%M:%S.%f").isoformat()
            if timestamp < threshold_time.isoformat():
                file_write.write(line)

scheduler = BackgroundScheduler()
scheduler.add_job(remove_lines, 'interval', minutes=1)
scheduler.start()

@app.get("/get_alerts")
async def get_alerts():
    alert_list = []
    with open("/var/log/snort/alert", "r") as f:
        for line in f:
            pattern = r'(\d{2}\/\d{1,2}-\d{2}:\d{2}:\d{2}\.\d{6}).{10}(\d+).+?\]\s(.*?)\s\[\*{2}\]\s\[Classification:\s(.*?)\]\s\[Priority:\s(.*?)\]\s\{(.*?)\}\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d+)\s->\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d+)'
            matches = re.match(pattern, line)
            if matches:
                timestamp = datetime.strptime(str(datetime.now().year) + "/" + matches.group(1), "%Y/%m/%d-%H:%M:%S.%f").isoformat()
                rule_id = matches.group(2)
                description = matches.group(3)
                classification = matches.group(4)
                priority = matches.group(5)
                protocol = matches.group(6)
                src_addr = matches.group(7)
                src_port = matches.group(8)
                targ_addr = matches.group(9)
                targ_port = matches.group(10)
                alert_list.append({"timestamp": timestamp, "rule_id": rule_id, "description": description, "classification": classification, "priority": priority, "protocol": protocol, "src_addr": src_addr, "src_port": src_port, "targ_addr": targ_addr, "targ_port": targ_port})
            elif re.match(r'(\d{2}\/\d{1,2}-\d{2}:\d{2}:\d{2}\.\d{6}).{10}(\d+).+?\]\s(.*?)\s\[\*{2}\]\s\[Classification:\s(.*?)\]\s\[Priority:\s(.*?)\]\s\{(.*?)\}\s(.*)\s->\s(.*)', line):
                matches = re.match(r'(\d{2}\/\d{1,2}-\d{2}:\d{2}:\d{2}\.\d{6}).{10}(\d+).+?\]\s(.*?)\s\[\*{2}\]\s\[Classification:\s(.*?)\]\s\[Priority:\s(.*?)\]\s\{(.*?)\}\s(.*)\s->\s(.*)', line)
                timestamp = datetime.strptime(str(datetime.now().year) + "/" + matches.group(1), "%Y/%m/%d-%H:%M:%S.%f").isoformat()
                rule_id = matches.group(2)
                description = matches.group(3)
                classification = matches.group(4)
                priority = matches.group(5)
                protocol = matches.group(6)
                src_addr = matches.group(7)
                targ_addr = matches.group(8)
                alert_list.append({"timestamp": timestamp, "rule_id": rule_id, "description": description, "classification": classification, "priority": priority, "protocol": protocol, "src_addr": src_addr, "targ_addr": targ_addr})
            else:
                print("No match: " + line)
    return alert_list

@app.get("/get_count")
async def get_count():
    alerts = await get_alerts()
    prio_count = {
        "prio1": 0,
        "prio2": 0
    }
    for alert in alerts:
        if alert["priority"] == "1":
            prio_count["prio1"] = prio_count["prio1"] + 1
        elif alert["priority"] == "2":
            prio_count["prio2"] = prio_count["prio2"] + 1
    return prio_count

@app.get("/get_current_threat_level")
async def get_current_threat_level():
    current_time = datetime.now()
    ten_minutes_ago = current_time - timedelta(minutes=1)
    threat_value = 0
    alerts = await get_alerts()
    for alert in alerts:
        if ten_minutes_ago <= datetime.fromisoformat(alert["timestamp"]):
            if alert["priority"] == "1":
                threat_value = threat_value + 2
            elif alert["priority"] == "2":
                threat_value = threat_value + 1
    return threat_value