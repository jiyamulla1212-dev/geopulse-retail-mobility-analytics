import pandas as pd
from pathlib import Path

def generate_markdown_report(
    zone_csv: str = "reports/zone_mobility_summary.csv",
    hourly_csv: str = "reports/hourly_zone_metrics.csv",
    store_csv: str = "reports/store_benchmarks.csv",
    anomaly_csv: str = "reports/traffic_anomalies.csv",
    output_md: str = "reports/executive_mobility_summary.md",
) -> Path:
    zone_path = Path(zone_csv)
    hourly_path = Path(hourly_csv)
    if not zone_path.exists() or not hourly_path.exists():
        raise FileNotFoundError("Required summary CSVs not found. Run src/pipeline.py first.")

    zone_df = pd.read_csv(zone_path)
    hourly_df = pd.read_csv(hourly_path)

    top_zone = zone_df.iloc[0]
    best_conv = hourly_df.sort_values("conversion_rate_pct", ascending=False).iloc[0]

    highlights = [
        f"- **Top Revenue Zone:** {top_zone['zone']} (Revenue: {int(top_zone['total_revenue']):,}, Foot Traffic: {int(top_zone['total_foot_traffic'])})",
        f"- **Peak Conversion Window:** {best_conv['zone']} at Hour {int(best_conv['hour'])}:00 ({best_conv['conversion_rate_pct']}% conversion)",
        f"- **Total Zones Analyzed:** {len(zone_df)}",
    ]

    if Path(store_csv).exists():
        store_df = pd.read_csv(store_csv)
        top_store = store_df.iloc[0]
        highlights.append(
            f"- **Top Performing Store:** {top_store['store_id']} ({top_store['zone']}) — Revenue/Visitor: {top_store['revenue_per_visitor']}"
        )

    if Path(anomaly_csv).exists():
        anomaly_df = pd.read_csv(anomaly_csv)
        spike_count = int(anomaly_df["is_spike"].sum())
        highlights.append(f"- **Detected Traffic Spikes:** {spike_count} flagged window(s)")

    lines = [
        "# GeoPulse Retail Mobility - Executive Summary",
        "",
        "## Key Highlights",
        *highlights,
        "",
        "## Zone Performance Breakdown",
        zone_df.to_markdown(index=False),
        "",
    ]

    out = Path(output_md)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    return out

if __name__ == "__main__":
    report_file = generate_markdown_report()
    print("Generated executive report at:", report_file)
    print(report_file.read_text(encoding="utf-8"))
