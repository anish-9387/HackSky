import sys
import os
import sqlite3
import csv
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from pathlib import Path

# Add sensor data log file path
SENSOR_LOG_FILE = os.path.join("logs", "sensor_data.csv")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db import init_db, log_access_attempt, get_private_key, fetch_logs
from pqc_sim import decrypt_and_verify

app = Flask(__name__)
init_db()

@app.route('/connect', methods=['POST'])
def connect_node():
    data = request.get_json()
    node_id = data.get("node_id")
    session_key = data.get("session_key")
    cipher = data.get("cipher")

    client_ip = request.remote_addr

    if not all([node_id, session_key, cipher]):
        return jsonify({"status": "Bad Request"}), 400

    private_key = get_private_key(node_id)
    if private_key and decrypt_and_verify(cipher, private_key, session_key):
        log_access_attempt(node_id, client_ip, "Access Granted ✅")
        return jsonify({"status": "Access Granted ✅", "node_id": node_id}), 200

    log_access_attempt(node_id, client_ip, "Access Denied ❌")
    return jsonify({"status": "Access Denied ❌", "node_id": node_id}), 403

@app.route('/')
def dashboard():
    logs = fetch_logs()
    granted = sum(1 for row in logs if row[2].startswith("Access Granted"))
    denied = sum(1 for row in logs if row[2].startswith("Access Denied"))
    return render_template('dashboard.html', logs=logs, granted=granted, denied=denied)

# ✅ NEW: Sensor data receiver
@app.route('/sensor-data', methods=['POST'])
def receive_sensor_data():
    try:
        data = request.get_json(force=True)
        sensor1 = float(data.get("sensor1"))
        sensor2 = float(data.get("sensor2"))

        if sensor1 is None or sensor2 is None:
            return jsonify({"status": "Missing sensor data"}), 400

        # ✅ Create logs/ if not exists
        log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, 'sensor_data.csv')

        # ✅ Write data
        file_exists = os.path.isfile(log_file)
        with open(log_file, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(["timestamp", "sensor1", "sensor2"])
            writer.writerow([datetime.now(), sensor1, sensor2])

        print(f"✅ Logged: sensor1={sensor1}, sensor2={sensor2}")
        return jsonify({"status": "Sensor data logged ✅"}), 200

    except Exception as e:
        import traceback
        print("❌ ERROR:", str(e))
        traceback.print_exc()
        return jsonify({"status": "Logging failed", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)