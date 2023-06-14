import fileinput
import re
from datetime import datetime, timedelta

def remove_lines(file_path, threshold_minutes):
    threshold_time = datetime.now() - timedelta(minutes=threshold_minutes)
    
    with fileinput.FileInput(file_path, inplace=True) as file:
        for line in file:
            pattern = r'(\d{2}\/\d{1,2}-\d{2}:\d{2}:\d{2}\.\d{6}).{10}(\d+).+?\]\s(.*?)\s\[\*{2}\]\s\[Classification:\s(.*?)\]\s\[Priority:\s(.*?)\]\s\{(.*?)\}\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d+)\s->\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d+)'
            matches = re.match(pattern, line)
            timestamp_str = datetime.strptime(str(datetime.now().year) + "/" + matches.group(1), "%Y/%m/%d-%H:%M:%S.%f").isoformat()
            timestamp = datetime.fromisoformat(timestamp_str)

            if timestamp >= threshold_time:
                print(line, end='')