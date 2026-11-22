import pandas as pd
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="GeoPulse Retail Mobility", layout="wide")
st.title("GeoPulse: Hyper-Local Retail Mobility Analytics")

clean_path = Path("data/processed/retail_mobility_clean.csv")
summary_path = Path("reports/zone_mobility_summary.csv")

if not clean_path.exists() or not summary_path.exists():
    st.error("Processed data or zone summary not found. Run src/clean.py and src/analytics.py first.")
    st.stop()

df = pd.read_csv(clean_path)
summary = pd.read_csv(summary_path)

zones = ["All"] + sorted(df["zone"].unique().tolist())
selected_zone = st.sidebar.selectbox("Filter by Zone", zones)
filtered_df = df if selected_zone == "All" else df[df["zone"] == selected_zone]

col1, col2, col3 = st.columns(3)
col1.metric("Total Foot Traffic", int(filtered_df["foot_traffic"].sum()))
col2.metric("Total Transactions", int(filtered_df["transactions"].sum()))
col3.metric("Total Revenue", f"{int(filtered_df['revenue'].sum()):,}")

st.subheader("Revenue by Zone")
st.bar_chart(summary.set_index("zone")["total_revenue"])

st.subheader("Filtered Mobility Records")
st.dataframe(filtered_df, use_container_width=True)
