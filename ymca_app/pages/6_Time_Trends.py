import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.markdown(
    "<h1 style='color:#8b0000;'>📆 Time & Seasonality Trends</h1>",
    unsafe_allow_html=True
)

@st.cache_data
def load_data():
    here = Path(__file__).resolve()
    base_dir = here.parent.parent
    excel_path = base_dir / "ymca_clusters.xlsx"
    df = pd.read_excel(excel_path, engine="openpyxl")

    # Ensure date, year, month fields
    if "start_date" in df.columns:
        df["start_date"] = pd.to_datetime(df["start_date"], errors="coerce")
    if "hold_year" not in df.columns and "start_date" in df.columns:
        df["hold_year"] = df["start_date"].dt.year
    if "hold_month" not in df.columns and "start_date" in df.columns:
        df["hold_month"] = df["start_date"].dt.month

    return df

df = load_data()

if "hold_year" not in df.columns or "hold_month" not in df.columns:
    st.error("Need 'hold_year' and 'hold_month' or 'start_date' to build time trends.")
    st.stop()

# Year filter
years = sorted(df["hold_year"].dropna().unique().tolist())
year_choice = st.multiselect("Select year(s):", years, default=years)

df_year = df[df["hold_year"].isin(year_choice)]

st.markdown("### 📉 Monthly Fee Loss Trend")

if "fee_loss" in df.columns:
    monthly = (
        df_year.groupby(["hold_year", "hold_month"])["fee_loss"]
        .sum()
        .reset_index()
        .sort_values(["hold_year", "hold_month"])
    )
    monthly["year_month"] = monthly["hold_year"].astype(str) + "-" + monthly["hold_month"].astype(str).str.zfill(2)

    fig_line = px.line(
        monthly,
        x="year_month",
        y="fee_loss",
        title="Total Fee Loss Over Time (Monthly)",
        markers=True
    )
    fig_line.update_layout(xaxis_title="Year-Month", yaxis_title="Total Fee Loss")
    st.plotly_chart(fig_line, use_container_width=True)

# Holds per month
st.markdown("### 📦 Number of Holds per Month")

monthly_count = (
    df_year.groupby(["hold_year", "hold_month"])
    .size()
    .reset_index(name="count")
)
monthly_count["year_month"] = monthly_count["hold_year"].astype(str) + "-" + monthly_count["hold_month"].astype(str).str.zfill(2)

fig_bar = px.bar(
    monthly_count,
    x="year_month",
    y="count",
    title="Number of Holds per Month",
)
fig_bar.update_layout(xaxis_title="Year-Month", yaxis_title="Holds")
st.plotly_chart(fig_bar, use_container_width=True)

# Heatmap by month vs location
if "membership_location" in df.columns and "fee_loss" in df.columns:
    st.markdown("### 🌡 Fee Loss Heatmap by Location & Month")

    heat_df = (
        df_year.groupby(["membership_location", "hold_month"])["fee_loss"]
        .sum()
        .reset_index()
    )

    pivot = heat_df.pivot(index="membership_location", columns="hold_month", values="fee_loss").fillna(0)
    pivot = pivot.sort_index()

    fig_heat = px.imshow(
        pivot,
        aspect="auto",
        labels=dict(x="Month", y="Location", color="Total Fee Loss"),
        title="Monthly Fee Loss Heatmap by Location",
        color_continuous_scale="Reds"
    )
    st.plotly_chart(fig_heat, use_container_width=True)
