from ingest import load_retail_data
from clean import clean_retail_data, save_cleaned_data
from validate import validate_mobility_data
from analytics import summarize_by_zone, save_zone_summary
from hourly_metrics import compute_hourly_metrics, save_hourly_metrics
from database import load_to_sqlite

def run_pipeline() -> None:
    print("1/5 Ingesting raw retail mobility data...")
    raw_df = load_retail_data()

    print("2/5 Cleaning and engineering features...")
    clean_df = clean_retail_data(raw_df)
    clean_path = save_cleaned_data(clean_df)

    print("3/5 Validating cleaned dataset...")
    report = validate_mobility_data(str(clean_path))
    if not report["is_valid"]:
        raise RuntimeError(f"Data validation failed: {report}")

    print("4/5 Generating zone and hourly analytical summaries...")
    zone_df = summarize_by_zone(clean_df)
    save_zone_summary(zone_df)
    hourly_df = compute_hourly_metrics(clean_df)
    save_hourly_metrics(hourly_df)

    print("5/5 Loading cleaned records into SQLite...")
    inserted = load_to_sqlite(str(clean_path))
    print(f"Pipeline complete! {inserted} records verified and persisted.")

if __name__ == "__main__":
    run_pipeline()
