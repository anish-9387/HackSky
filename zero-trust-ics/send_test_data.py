import requests
import random
import time

url = "http://127.0.0.1:5000/sensor-data"

for _ in range(10):  # Send 10 data points
    payload = {
        "sensor1": round(random.uniform(70, 90), 2),
        "sensor2": round(random.uniform(60, 85), 2)
    }

    res = requests.post(url, json=payload)
    print("Sent:", payload, "| Response:", res.status_code)
    time.sleep(1)  # 1 second gap