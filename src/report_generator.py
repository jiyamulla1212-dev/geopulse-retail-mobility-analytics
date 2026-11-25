import pandas as pd
from pathlib import Path

def generate_markdown_report(
    zone_csv: str = "reports/zone_mobility_summary.csv",
    hourly_csv: str = "reports/hourly_zone_metrics.csv",
    output_md: str = "reports/executive_mobility_summary.md",
) -> Path:
    zone_path = Path(zone_csv)
    hourly_path = Path(hourly_csv)
    if not zone_path.exists() or not hourly_path.exists():
        raise FileNotFoundError("Required summary CSVs not found. Run analytics and hourly_metrics first.")

    zone_df = pd.read_csv(zone_path)
    hourly_df = pd.read_csv(hourly_path)

    top_zone = zone_df.iloc[0]
    best_conv = hourly_df.sort_values("conversion_rate_pct", ascending=False).iloc[0]

    lines = [
        "# GeoPulse Retail Mobility - Executive Summary",
        "",
        "## Key Highlights",
        f"- **Top Revenue Zone:** {top_zone['zone']} (Revenue: {int(top_zone['total_revenue']):,}, Foot Traffic: {int(top_zone['total_foot_traffic'])})",
        f"- **Peak Conversion Window:** {best_conv['zone']} at Hour {int(best_conv['hour'])}:00 ({best_conv['conversion_rate_pct']}% conversion)",
        f"- **Total Zones Analyzed:** {len(zone_df)}",
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
