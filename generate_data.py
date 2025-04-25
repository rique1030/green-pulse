from config import *
from datetime import datetime, timedelta
import random
import os
import csv

def generate_appliance_data(appliance_name: str, mean: float, std: float, n: int):
    data = []
    timestamp = START_DATE
    for _ in range(TOTAL_ENTRIES):
        is_anomaly = random.random() < ANOMALY_RATE
        if is_anomaly:
            anomaly_factor = 0
            if random.random() < 0.5:
                anomaly_factor = random.uniform(2,3)
            else:
                anomaly_factor = random.uniform(0.1,0.5)
            power = round(mean * anomaly_factor, 2)
        else:
            power = round(random.gauss(mean, std), 2)
            power = max(0.01, power)
        data.append([timestamp.strftime("%Y-%m-%d %H:%M:%S"), appliance_name, power, int(is_anomaly)])
        timestamp += timedelta(minutes=INTERVAL)
    return data


for appliance, settings in APPLIANCES.items():
    data = generate_appliance_data(appliance, settings["mean"], settings["std"], TOTAL_ENTRIES)
    file_path = os.path.join(DATA_PATH, f"{appliance}.csv")
    with open(file_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "appliance", "power", "is_anomaly"])
        writer.writerows(data)

DATA_PATH
