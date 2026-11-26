import pandas as pd
from pathlib import Path
from analytics import load_cleaned_data

def compute_store_benchmarks(df: pd.DataFrame) -> pd.DataFrame:
    stores = (
        df.groupby(['store_id', 'zone'], as_index=False)
        .agg(
            total_visitors=('foot_traffic', 'sum'),
            avg_dwell_mins=('avg_dwell_mins', 'mean'),
            total_orders=('transactions', 'sum'),
            total_revenue=('revenue', 'sum')
        )
    )
    stores['avg_dwell_mins'] = stores['avg_dwell_mins'].round(1)
    stores['revenue_per_visitor'] = (stores['total_revenue'] / stores['total_visitors'].replace(0, pd.NA)).round(2)
    return stores.sort_values('total_revenue', ascending=False)

def save_store_benchmarks(store_df: pd.DataFrame, output_path: str = 'reports/store_benchmarks.csv') -> Path:
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    store_df.to_csv(out, index=False)
    return out

if __name__ == '__main__':
    cleaned = load_cleaned_data()
    benchmarks = compute_store_benchmarks(cleaned)
    out_file = save_store_benchmarks(benchmarks)
    print('Saved store benchmarks to:', out_file)
    print(benchmarks)
