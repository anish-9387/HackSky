import os
import pandas as pd
from model import detect_anomalies
from anomaly_db import store_anomalies
import streamlit as st

st.set_page_config(layout="wide")
st.title("🔍 ICS Predictive Maintenance Dashboard")

DATA_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'logs', 'sensor_data.csv'))

st.write("Looking for sensor data at:", DATA_FILE)

# ✅ Read and check CSV
try:
    df = pd.read_csv(DATA_FILE)
    if {"timestamp", "sensor1", "sensor2"}.issubset(df.columns):
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        anomaly_df = detect_anomalies(df)
        store_anomalies(anomaly_df[anomaly_df["anomaly"] == -1])

        st.subheader("📈 Sensor Trends")
        st.line_chart(anomaly_df.set_index("timestamp")[["sensor1", "sensor2"]])

        st.subheader("🔴 Anomalies Detected")
        st.scatter_chart(anomaly_df[anomaly_df["anomaly"] == -1].set_index("timestamp")[["sensor1"]])
    else:
        st.warning("Missing sensor data columns.")
        st.write("Columns found:", df.columns.tolist())
except Exception as e:
    st.error(f"❌ Failed to load data: {str(e)}")