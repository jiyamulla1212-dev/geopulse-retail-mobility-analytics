import pandas as pd
from pathlib import Path
from ingest import load_retail_data

def clean_retail_data(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned['store_id'] = cleaned['store_id'].astype(str).str.strip().str.upper()
    cleaned['zone'] = cleaned['zone'].astype(str).str.strip().str.title()
    cleaned['date'] = pd.to_datetime(cleaned['date'], errors='coerce')
    numeric_cols = ['hour', 'foot_traffic', 'avg_dwell_mins', 'transactions', 'revenue']
    for col in numeric_cols:
        cleaned[col] = pd.to_numeric(cleaned[col], errors='coerce')
    cleaned = cleaned.dropna(subset=['store_id', 'zone', 'date', 'foot_traffic', 'revenue']).drop_duplicates()
    cleaned = cleaned[(cleaned['hour'].between(0, 23)) & (cleaned['foot_traffic'] >= 0) & (cleaned['revenue'] >= 0)]
    cleaned['revenue_per_visitor'] = (cleaned['revenue'] / cleaned['foot_traffic'].replace(0, pd.NA)).round(2)
    return cleaned

def save_cleaned_data(df: pd.DataFrame, output_path: str = 'data/processed/retail_mobility_clean.csv') -> Path:
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    return out

if __name__ == '__main__':
    raw_df = load_retail_data()
    clean_df = clean_retail_data(raw_df)
    saved_file = save_cleaned_data(clean_df)
    print('Cleaned rows:', len(clean_df))
    print('Saved to:', saved_file)
    print(clean_df.head())
