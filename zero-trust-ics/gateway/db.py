import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent / "../logs/access_log.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            node_id TEXT UNIQUE,
            secret_key TEXT
        )
    ''')
    conn.commit()
    conn.close()

def register_node(node_id, secret_key):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO nodes (node_id, secret_key) VALUES (?, ?)", (node_id, secret_key))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Already registered
    conn.close()

def is_node_authorized(node_id, secret_key):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nodes WHERE node_id = ? AND secret_key = ?", (node_id, secret_key))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def log_access_attempt(node_id, ip_address, result):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS access_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            node_id TEXT,
            ip_address TEXT,
            result TEXT,
            timestamp TEXT
        )
    ''')
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("INSERT INTO access_logs (node_id, ip_address, result, timestamp) VALUES (?, ?, ?, ?)",
                   (node_id, ip_address, result, timestamp))
    conn.commit()
    conn.close()

def get_private_key(node_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT secret_key FROM nodes WHERE node_id = ?", (node_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None