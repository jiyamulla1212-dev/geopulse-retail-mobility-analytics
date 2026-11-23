import pandas as pd
from pathlib import Path

REQUIRED_COLUMNS = [
    "store_id",
    "zone",
    "date",
    "hour",
    "foot_traffic",
    "avg_dwell_mins",
    "transactions",
    "revenue",
]

def validate_mobility_data(file_path: str = "data/processed/retail_mobility_clean.csv") -> dict:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found at {path}")

    df = pd.read_csv(path)
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    report = {
        "row_count": int(len(df)),
        "null_cells": int(df[REQUIRED_COLUMNS].isna().sum().sum()),
        "negative_traffic": int((df["foot_traffic"] < 0).sum()),
        "negative_revenue": int((df["revenue"] < 0).sum()),
        "transactions_exceed_traffic": int((df["transactions"] > df["foot_traffic"]).sum()),
        "zones_count": int(df["zone"].nunique()),
    }
    report["is_valid"] = (
        report["row_count"] > 0
        and report["null_cells"] == 0
        and report["negative_traffic"] == 0
        and report["negative_revenue"] == 0
    )
    return report

if __name__ == "__main__":
    summary = validate_mobility_data()
    for key, val in summary.items():
        print(f"{key}: {val}")
