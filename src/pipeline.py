from ingest import load_retail_data
from clean import clean_retail_data, save_cleaned_data
from validate import validate_mobility_data
from analytics import summarize_by_zone, save_zone_summary
from hourly_metrics import compute_hourly_metrics, save_hourly_metrics
from store_metrics import compute_store_benchmarks, save_store_benchmarks
from anomaly_detector import detect_traffic_anomalies, save_anomaly_report
from database import load_to_sqlite
from report_generator import generate_markdown_report

def run_pipeline() -> None:
    print("1/6 Ingesting raw retail mobility data...")
    raw_df = load_retail_data()

    print("2/6 Cleaning and engineering features...")
    clean_df = clean_retail_data(raw_df)
    clean_path = save_cleaned_data(clean_df)

    print("3/6 Validating cleaned dataset...")
    report = validate_mobility_data(str(clean_path))
    if not report["is_valid"]:
        raise RuntimeError(f"Data validation failed: {report}")

    print("4/6 Generating zone, hourly, store, and anomaly reports...")
    zone_df = summarize_by_zone(clean_df)
    zone_path = save_zone_summary(zone_df)
    hourly_df = compute_hourly_metrics(clean_df)
    hourly_path = save_hourly_metrics(hourly_df)
    store_df = compute_store_benchmarks(clean_df)
    save_store_benchmarks(store_df)
    anomaly_df = detect_traffic_anomalies(clean_df)
    save_anomaly_report(anomaly_df)

    print("5/6 Loading cleaned records into SQLite...")
    inserted = load_to_sqlite(str(clean_path))

    print("6/6 Generating executive Markdown report...")
    md_path = generate_markdown_report(str(zone_path), str(hourly_path))
    print(f"Pipeline complete! {inserted} records persisted and report saved to {md_path}.")

if __name__ == "__main__":
    run_pipeline()
