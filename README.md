# GeoPulse: Hyper-Local Retail Mobility Analytics

End-to-end Python analytics pipeline and interactive Streamlit dashboard for hyper-local retail foot-traffic, dwell-time, conversion, and revenue insights.

## Project Architecture
- src/ingest.py - Loads raw retail mobility records.
- src/clean.py - Standardizes fields, validates ranges, and engineers revenue_per_visitor.
- src/validate.py - Runs automated schema and data-quality checks.
- src/analytics.py - Aggregates zone-level foot traffic, dwell time, transactions, revenue, and peak hours.
- src/hourly_metrics.py - Computes hourly conversion rates and traffic trends by zone.
- src/database.py - Persists cleaned mobility records into SQLite via SQLAlchemy.
- src/report_generator.py - Generates reports/executive_mobility_summary.md.
- src/pipeline.py - Orchestrates the complete 6-step ETL workflow.
- dashboard/app.py - Interactive Streamlit dashboard for zone filtering and KPI visualization.
- tests/test_pipeline.py - Unit tests verifying cleaning, zone summaries, and hourly metrics.

## Quickstart
1. Install dependencies: py -m pip install -r requirements.txt
2. Run full ETL pipeline: py src/pipeline.py
3. Run unit tests: py -m unittest discover -s tests -v
4. Launch dashboard: py -m streamlit run dashboard/app.py
