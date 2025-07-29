import sys
import os
sys.path.append(os.path.abspath("../shared"))

from flask import Flask, request, jsonify
from db import init_db, is_node_authorized, log_access_attempt, get_private_key
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

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)