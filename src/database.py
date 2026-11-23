import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine

def load_to_sqlite(
    clean_csv: str = "data/processed/retail_mobility_clean.csv",
    db_path: str = "data/geopulse_retail.db",
    table_name: str = "retail_mobility"
) -> int:
    csv_file = Path(clean_csv)
    if not csv_file.exists():
        raise FileNotFoundError(f"Cleaned CSV not found at {csv_file}")
    df = pd.read_csv(csv_file)
    engine = create_engine(f"sqlite:///{db_path}")
    df.to_sql(table_name, con=engine, if_exists="replace", index=False)
    return len(df)

if __name__ == "__main__":
    rows = load_to_sqlite()
    print(f"Loaded {rows} records into SQLite table 'retail_mobility'")
