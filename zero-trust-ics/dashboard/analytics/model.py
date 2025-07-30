from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import pandas as pd

def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Normalize sensor values
    scaler = StandardScaler()
    X = scaler.fit_transform(df[["sensor1", "sensor2"]])

    # Train Isolation Forest
    model = IsolationForest(contamination=0.01, random_state=42)
    df["anomaly"] = model.fit_predict(X)

    return df