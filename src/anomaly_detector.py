import pandas as pd
from pathlib import Path
from analytics import load_cleaned_data

def detect_traffic_anomalies(df: pd.DataFrame, z_threshold: float = 1.5) -> pd.DataFrame:
    data = df.copy()
    mean_traffic = data["foot_traffic"].mean()
    std_traffic = data["foot_traffic"].std(ddof=0) or 1.0
    data["traffic_zscore"] = ((data["foot_traffic"] - mean_traffic) / std_traffic).round(2)
    data["is_spike"] = data["traffic_zscore"].abs() >= z_threshold
    return data.sort_values("traffic_zscore", ascending=False)

def save_anomaly_report(anomaly_df: pd.DataFrame, output_path: str = "reports/traffic_anomalies.csv") -> Path:
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    anomaly_df.to_csv(out, index=False)
    return out

if __name__ == "__main__":
    cleaned = load_cleaned_data()
    anomalies = detect_traffic_anomalies(cleaned)
    out_file = save_anomaly_report(anomalies)
    print("Saved traffic anomaly report to:", out_file)
    print(anomalies[["store_id", "zone", "hour", "foot_traffic", "traffic_zscore", "is_spike"]])
