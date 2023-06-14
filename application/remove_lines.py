import fileinput
import re
from datetime import datetime, timedelta

def remove_lines(file_path, threshold_minutes):
    threshold_time = datetime.now() - timedelta(minutes=threshold_minutes)
    
    with fileinput.FileInput(file_path, inplace=True) as file:
        for line in file:
            timestamp_str = line.split(',')[0].strip()
            timestamp = datetime.strptime(timestamp_str, "%m/%d-%H:%M:%S.%f")

            if timestamp >= threshold_time:
                print(line, end='')