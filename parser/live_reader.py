import serial
import time
import pandas as pd
import re
from datetime import datetime

def start_live_uart(port="COM3", baudrate=9600, duration=10):
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
    except serial.SerialException as e:
        print(f"Error opening serial port {port}: {e}")
        return None

    ser = serial.Serial(port, baudrate, timeout=1)
    start_time = time.time()
    logs = []
    last_time = None

    while time.time() - start_time < duration:
        line = ser.readline().decode(errors='ignore').strip()
        match = re.match(r'(\d{2}:\d{2}:\d{2}).*(RX|TX).*?: (.+)', line)
        if match:
            time_str, direction, message = match.groups()
            time_obj = datetime.strptime(time_str, "%H:%M:%S")
            delay = (time_obj - last_time).total_seconds() if last_time else 0
            last_time = time_obj
            logs.append({
                "Time": time_str,
                "Direction": direction,
                "Message": message.strip(),
                "Delay": delay
            })
    
    ser.close()
    return pd.DataFrame(logs)
