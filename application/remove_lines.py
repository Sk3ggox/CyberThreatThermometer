import fileinput
import re
from datetime import datetime, timedelta

def remove_lines(file_path, threshold_minutes):
    threshold_time = datetime.now() - timedelta(minutes=threshold_minutes)
    pattern = r'(\d{2}\/\d{1,2}-\d{2}:\d{2}:\d{2}\.\d{6}).*'
    
    with open(file_path, "r") as file, open(file_path, "w") as file_write:
        for line in file:
            timestamp = datetime.strptime(str(datetime.now().year) + "/" + re.match(pattern, line).group(1), "%Y/%m/%d-%H:%M:%S.%f").isoformat()
            if timestamp > threshold_time.isoformat():
                file_write.write(line)