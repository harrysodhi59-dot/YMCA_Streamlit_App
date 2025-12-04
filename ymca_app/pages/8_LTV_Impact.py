import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import numpy as np

st.markdown(
    "<h1 style='color:#8b0000;'>💸 Lifetime Value (LTV) Impact</h1>",
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

# ----- Configurable assumptions -----
st.markdown("### ⚙️ LTV Model Assumptions (Simple Approximation)")
col_a1, col_a2 = st.columns(2)

base_months = col_a1.slider("Assumed Active Months (no holds)", 6, 48, 24)
hold_penalty_factor = col_a2.slider("Hold Penalty Factor (months lost per 30 days on hold)", 0.0, 1.5, 1.0, step=0.1)

# ----- Choose grouping dimension -----
group_options = {}
if "cluster_label" in df.columns:
    group_options["Cluster"] = "cluster_label"
if "cluster_name" in df.columns:
    group_options["Cluster Name"] = "cluster_name"
group_options["Membership Type"] = "application_subscription_membership_type"
group_options["Package Category"] = "application_package_category"
group_options["Location"] = "membership_location"
group_options["Age Category"] = "application_contact_age_category"

st.markdown("### 🎯 Select Segment Dimension")
seg_label = st.selectbox("Group members by:", list(group_options.keys()))
seg_col = group_options[seg_label]

# ----- Compute LTV metrics -----
if "membership_fee" not in df.columns or "hold_duration_days" not in df.columns:
    st.error("Need 'membership_fee' and 'hold_duration_days' columns for LTV analysis.")
    st.stop()

grouped = (
    df.groupby(seg_col)[["membership_fee", "hold_duration_days"]]
    .mean()
    .reset_index()
    .rename(columns={"membership_fee": "avg_fee", "hold_duration_days": "avg_hold_days"})
)

# Baseline and adjusted LTV
grouped["baseline_ltv"] = grouped["avg_fee"] * base_months
grouped["hold_months_lost"] = (grouped["avg_hold_days"] / 30.0) * hold_penalty_factor
grouped["effective_months"] = np.maximum(base_months - grouped["hold_months_lost"], 0)
grouped["adjusted_ltv"] = grouped["avg_fee"] * grouped["effective_months"]
grouped["ltv_impact"] = grouped["baseline_ltv"] - grouped["adjusted_ltv"]

st.markdown("### 📊 LTV Summary Table")
st.dataframe(grouped[[seg_col, "avg_fee", "avg_hold_days", "baseline_ltv", "adjusted_ltv", "ltv_impact"]]
             .round(2), use_container_width=True)

st.markdown("### 💥 LTV Loss by Segment")
fig = px.bar(
    grouped.sort_values("ltv_impact", ascending=False),
    x=seg_col,
    y="ltv_impact",
    title=f"LTV Loss per {seg_label} (due to holds)",
    labels={seg_col: seg_label, "ltv_impact": "LTV Loss"},
    color="ltv_impact",
    color_continuous_scale="Reds"
)
fig.update_layout(xaxis_tickangle=-35)
st.plotly_chart(fig, use_container_width=True)

top_row = grouped.sort_values("ltv_impact", ascending=False).iloc[0]
st.info(
    f"📌 Segment **{top_row[seg_col]}** has the highest LTV reduction, "
    f"with an average loss of about **${top_row['ltv_impact']:.0f}** per member."
)
