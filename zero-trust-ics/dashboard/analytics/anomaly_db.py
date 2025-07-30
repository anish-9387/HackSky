import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "logs" / "anomalies.db"

def store_anomalies(df: pd.DataFrame):
    if df.empty:
        return

    conn = sqlite3.connect(DB_PATH)
    df[["timestamp", "sensor1", "sensor2"]].to_sql("anomaly_log", conn, if_exists="append", index=False)
    conn.close()