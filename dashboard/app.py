import pandas as pd
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="GeoPulse Retail Mobility", layout="wide")
st.title("GeoPulse: Hyper-Local Retail Mobility Analytics")

clean_path = Path("data/processed/retail_mobility_clean.csv")
summary_path = Path("reports/zone_mobility_summary.csv")
hourly_path = Path("reports/hourly_zone_metrics.csv")

if not clean_path.exists() or not summary_path.exists():
    st.error("Processed data or zone summary not found. Run src/clean.py and src/analytics.py first.")
    st.stop()

df = pd.read_csv(clean_path)
summary = pd.read_csv(summary_path)

zones = ["All"] + sorted(df["zone"].unique().tolist())
selected_zone = st.sidebar.selectbox("Filter by Zone", zones)
filtered_df = df if selected_zone == "All" else df[df["zone"] == selected_zone]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Foot Traffic", int(filtered_df["foot_traffic"].sum()))
col2.metric("Avg Dwell (mins)", round(float(filtered_df["avg_dwell_mins"].mean()), 1))
col3.metric("Total Transactions", int(filtered_df["transactions"].sum()))
col4.metric("Total Revenue", f"{int(filtered_df['revenue'].sum()):,}")

left_col, right_col = st.columns(2)
with left_col:
    st.subheader("Revenue by Zone")
    st.bar_chart(summary.set_index("zone")["total_revenue"])

with right_col:
    st.subheader("Hourly Conversion Rate (%)")
    if hourly_path.exists():
        hourly_df = pd.read_csv(hourly_path)
        if selected_zone != "All":
            hourly_df = hourly_df[hourly_df["zone"] == selected_zone]
        st.bar_chart(hourly_df.set_index("hour")["conversion_rate_pct"])

st.subheader("Filtered Mobility Records")
st.dataframe(filtered_df, use_container_width=True)
