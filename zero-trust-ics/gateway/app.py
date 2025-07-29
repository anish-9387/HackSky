import sys
import os
import sqlite3
from flask import Flask, request, jsonify, render_template
from pathlib import Path
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

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)