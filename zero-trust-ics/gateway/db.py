import sqlite3
from pathlib import Path

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