import pandas as pd
from pathlib import Path

def load_retail_data(file_path: str = 'data/raw/retail_mobility_raw.csv') -> pd.DataFrame:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f'Dataset not found at {path}')
    df = pd.read_csv(path)
    return df

if __name__ == '__main__':
    df = load_retail_data()
    print('Loaded rows:', len(df))
    print('Columns:', list(df.columns))
    print(df.head())
