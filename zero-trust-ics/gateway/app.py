import sys
import os
sys.path.append(os.path.abspath("../shared"))

from flask import Flask, request, jsonify, render_template
from db import init_db, is_node_authorized, log_access_attempt, get_private_key, DB_PATH
from pqc_sim import decrypt_and_verify
import sqlite3
from pathlib import Path

app = Flask(__name__)
init_db()

@app.route('/connect', methods=['POST'])
def connect_node():
    data = request.get_json()
    node_id = data.get("node_id")
    session_key = data.get("session_key")
    cipher = data.get("cipher")
    client_ip = request.remote_addr or "unknown"

    if not all([node_id, session_key, cipher]):
        log_access_attempt(node_id or "unknown", client_ip, "Denied: Incomplete data")
        return jsonify({"status": "Bad Request"}), 400

    # Fetch private key
    private_key = get_private_key(node_id)
    if private_key and decrypt_and_verify(cipher, private_key, session_key):
        log_access_attempt(node_id, client_ip, "Access Granted")
        return jsonify({"status": "Access Granted ✅", "node_id": node_id}), 200

    log_access_attempt(node_id or "unknown", client_ip, "Access Denied ❌")
    return jsonify({"status": "Access Denied ❌", "node_id": node_id}), 403

@app.route('/')
def dashboard():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT node_id, ip_address, result, timestamp FROM access_logs ORDER BY id DESC LIMIT 50")
    logs = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM access_logs WHERE result LIKE 'Access Granted%'")
    granted = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM access_logs WHERE result LIKE 'Access Denied%'")
    denied = cursor.fetchone()[0]

    conn.close()

    return render_template("dashboard.html", logs=logs, granted=granted, denied=denied)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)
    app.run(host="986.0.1.2", port=5000)