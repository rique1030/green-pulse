from datetime import datetime, timedelta
import os

DAYS = 7
ENTRIES_PER_DAY = 1000 # 15-min intervalsa
INTERVAL = 1440 / ENTRIES_PER_DAY
TOTAL_ENTRIES = DAYS * ENTRIES_PER_DAY
ANOMALY_RATE = 0.05 # 5%
START_DATE = datetime(2025, 4, 1, 0, 0, 0)
DATA_PATH = "./synthetic_data/"

os.makedirs(DATA_PATH, exist_ok=True)

APPLIANCES = {
    "FR001": {
        "name": "fridge",
        "mean": 0.15, 
        "std": 0.02
    },
    "AC001": {
        "name": "air conditioner",
        "mean": 1.2, 
        "std": 0.3
    },
    "WM001": {
        "name": "washing machine",
        "mean": 0.5, 
        "std": 0.1
    },
    "RC001": {
        "name": "rice cooker",
        "mean": 0.4, 
        "std": 0.05
    },
    "TV001": {
        "name": "television",
        "mean": 0.1, 
        "std": 0.02
    }
}



