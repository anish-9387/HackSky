from flask import Flask, request, jsonify
from db import init_db, is_node_authorized
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

    if not all([node_id, session_key, cipher]):
        return jsonify({"status": "Bad Request"}), 400

    # Get node's private key from DB
    db_path = Path(__file__).parent / "../logs/access_log.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT secret_key FROM nodes WHERE node_id = ?", (node_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        private_key = row[0]
        if decrypt_and_verify(cipher, private_key, session_key):
            return jsonify({"status": "Access Granted ✅", "node_id": node_id}), 200

    return jsonify({"status": "Access Denied ❌", "node_id": node_id}), 403

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)