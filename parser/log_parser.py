import pandas as pd
import re
from datetime import datetime

def parse_log_file(file_path):
    """
    Parse UART log file into structured DataFrame
    Extracts timestamp, direction (RX/TX), message and delay
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data = []
    last_time = None

    for line in lines:
        match = re.match(r'(\d{2}:\d{2}:\d{2}).*(RX|TX).*?: (.+)', line)
        if match:
            time_str, direction, message = match.groups()
            time_obj = datetime.strptime(time_str, "%H:%M:%S")

            delay = (time_obj - last_time).total_seconds() if last_time else 0
            last_time = time_obj

            data.append({
                "Time": time_str,
                "Direction": direction,
                "Message": message.strip(),
                "Delay": delay
            })

    return pd.DataFrame(data)