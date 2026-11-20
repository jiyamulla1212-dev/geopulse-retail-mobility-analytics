import pandas as pd
from pathlib import Path

def load_cleaned_data(file_path: str = 'data/processed/retail_mobility_clean.csv') -> pd.DataFrame:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f'Cleaned dataset not found at {path}')
    return pd.read_csv(path)

def summarize_by_zone(df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        df.groupby('zone', as_index=False)
        .agg(
            total_foot_traffic=('foot_traffic', 'sum'),
            avg_dwell_mins=('avg_dwell_mins', 'mean'),
            total_transactions=('transactions', 'sum'),
            total_revenue=('revenue', 'sum'),
            peak_hour=('hour', lambda s: s.mode().iloc[0] if not s.mode().empty else s.iloc[0])
        )
    )
    summary['avg_dwell_mins'] = summary['avg_dwell_mins'].round(1)
    return summary.sort_values('total_revenue', ascending=False)

def save_zone_summary(summary_df: pd.DataFrame, output_path: str = 'reports/zone_mobility_summary.csv') -> Path:
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    summary_df.to_csv(out, index=False)
    return out

if __name__ == '__main__':
    clean_df = load_cleaned_data()
    zone_summary = summarize_by_zone(clean_df)
    out_file = save_zone_summary(zone_summary)
    print('Saved zone summary to:', out_file)
    print(zone_summary)
