import pandas as pd
from pathlib import Path
from analytics import load_cleaned_data

def compute_hourly_metrics(df: pd.DataFrame) -> pd.DataFrame:
    hourly = (
        df.groupby(['zone', 'hour'], as_index=False)
        .agg(
            visits=('foot_traffic', 'sum'),
            dwell_time=('avg_dwell_mins', 'mean'),
            txns=('transactions', 'sum'),
            sales=('revenue', 'sum')
        )
    )
    hourly['dwell_time'] = hourly['dwell_time'].round(1)
    hourly['conversion_rate_pct'] = ((hourly['txns'] / hourly['visits'].replace(0, pd.NA)) * 100).round(2)
    return hourly.sort_values(['zone', 'hour'])

def save_hourly_metrics(hourly_df: pd.DataFrame, output_path: str = 'reports/hourly_zone_metrics.csv') -> Path:
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    hourly_df.to_csv(out, index=False)
    return out

if __name__ == '__main__':
    cleaned = load_cleaned_data()
    hourly_df = compute_hourly_metrics(cleaned)
    out_path = save_hourly_metrics(hourly_df)
    print('Saved hourly metrics to:', out_path)
    print(hourly_df)
