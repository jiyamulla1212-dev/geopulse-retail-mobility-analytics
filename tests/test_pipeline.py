import sys
import unittest
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from clean import clean_retail_data
from analytics import summarize_by_zone
from hourly_metrics import compute_hourly_metrics

class TestGeoPulsePipeline(unittest.TestCase):
    def setUp(self):
        self.sample_raw = pd.DataFrame([
            {"store_id": " s001 ", "zone": " downtown ", "date": "2026-11-10", "hour": 10, "foot_traffic": 50, "avg_dwell_mins": 20, "transactions": 10, "revenue": 5000},
            {"store_id": "S001", "zone": "Downtown", "date": "2026-11-10", "hour": 18, "foot_traffic": 100, "avg_dwell_mins": 30, "transactions": 25, "revenue": 15000},
        ])

    def test_clean_retail_data(self):
        cleaned = clean_retail_data(self.sample_raw)
        self.assertEqual(len(cleaned), 2)
        self.assertEqual(cleaned.iloc[0]["store_id"], "S001")
        self.assertEqual(cleaned.iloc[0]["zone"], "Downtown")
        self.assertEqual(cleaned.iloc[0]["revenue_per_visitor"], 100.0)

    def test_summarize_by_zone(self):
        cleaned = clean_retail_data(self.sample_raw)
        summary = summarize_by_zone(cleaned)
        self.assertEqual(int(summary.iloc[0]["total_foot_traffic"]), 150)
        self.assertEqual(int(summary.iloc[0]["total_revenue"]), 20000)

    def test_compute_hourly_metrics(self):
        cleaned = clean_retail_data(self.sample_raw)
        hourly = compute_hourly_metrics(cleaned)
        self.assertEqual(len(hourly), 2)
        self.assertEqual(float(hourly.iloc[0]["conversion_rate_pct"]), 20.0)

if __name__ == "__main__":
    unittest.main()
