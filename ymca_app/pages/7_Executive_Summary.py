import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.markdown(
    "<h1 style='color:#8b0000;'>📋 Executive Summary</h1>",
    unsafe_allow_html=True
)

@st.cache_data
def load_data():
    here = Path(__file__).resolve()
    base_dir = here.parent.parent
    excel_path = base_dir / "ymca_clusters.xlsx"
    df = pd.read_excel(excel_path, engine="openpyxl")
    return df

df = load_data()

st.markdown("""
### 🎯 Project Focus: Revenue Impact of Hold Behaviour

This dashboard helps YMCA understand **how membership hold behaviour impacts revenue** and 
which **member segments** contribute most to lost fee income.  
Below is a high-level summary suitable for stakeholders and leadership.
""")

# Basic numbers
total_records = len(df)
total_fee_loss = df["fee_loss"].sum() if "fee_loss" in df.columns else 0
avg_hold = df["hold_duration_days"].mean() if "hold_duration_days" in df.columns else 0

c1, c2, c3 = st.columns(3)
c1.metric("Total Hold Records", f"{total_records:,}")
c2.metric("Total Estimated Fee Loss", f"${total_fee_loss:,.0f}")
c3.metric("Average Hold Duration", f"{avg_hold:.1f} days")

st.markdown("---")

# Top locations by fee loss
if "membership_location" in df.columns and "fee_loss" in df.columns:
    st.markdown("### 🏢 Top Locations by Fee Loss")

    loc_loss = (
        df.groupby("membership_location")["fee_loss"]
        .sum()
        .reset_index()
        .sort_values("fee_loss", ascending=False)
        .head(5)
    )
    fig_loc = px.bar(
        loc_loss,
        x="membership_location",
        y="fee_loss",
        title="Top 5 Locations by Fee Loss",
        color="fee_loss",
        color_continuous_scale="Reds"
    )
    st.plotly_chart(fig_loc, use_container_width=True)

# Top reasons by fee loss
if "reason_for_hold" in df.columns and "fee_loss" in df.columns:
    st.markdown("### 🧠 Hold Reasons Driving Fee Loss")

    reason_loss = (
        df.groupby("reason_for_hold")["fee_loss"]
        .sum()
        .reset_index()
        .sort_values("fee_loss", ascending=False)
    )
    fig_reason = px.bar(
        reason_loss,
        x="reason_for_hold",
        y="fee_loss",
        title="Fee Loss by Hold Reason",
    )
    fig_reason.update_layout(xaxis_tickangle=-35)
    st.plotly_chart(fig_reason, use_container_width=True)

st.markdown("---")

# Cluster summary (if available)
cluster_col = None
for c in df.columns:
    if "cluster_label" in c.lower() or "cluster_name" in c.lower():
        cluster_col = c
        break

if cluster_col and "fee_loss" in df.columns:
    st.markdown("### 🧩 Cluster-Level Summary")

    cluster_summary = (
        df.groupby(cluster_col)["fee_loss"]
        .agg(["sum", "mean", "count"])
        .reset_index()
        .rename(columns={"sum": "Total Fee Loss", "mean": "Avg Fee Loss", "count": "Members"})
    )

    st.dataframe(cluster_summary, use_container_width=True)

    top_cluster = cluster_summary.sort_values("Total Fee Loss", ascending=False).iloc[0]
    st.info(
        f"📌 **Key Insight:** Cluster **{top_cluster[cluster_col]}** has the highest total fee loss "
        f"(${top_cluster['Total Fee Loss']:,.0f}) and should be prioritized for policy review and engagement strategies."
    )

st.markdown("---")

st.markdown("""
### ✅ Recommended Actions (High-Level)

- **Review hold policies** for clusters and locations with highest fee loss.
- **Target member communication** for segments with long hold durations (e.g., seasonal or high-risk groups).
- **Experiment with alternative options** such as partial fees during holds or benefit adjustments.
- Use this dashboard to **monitor impact over time** after policy changes.
""")
