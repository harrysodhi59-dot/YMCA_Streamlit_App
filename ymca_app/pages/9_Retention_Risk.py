import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import numpy as np

st.markdown(
    "<h1 style='color:#8b0000;'>⚠️ Retention Risk Dashboard</h1>",
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

# Simple risk score = normalized combo of hold_duration_days + fee_loss
if "hold_duration_days" not in df.columns or "fee_loss" not in df.columns:
    st.error("Need 'hold_duration_days' and 'fee_loss' for risk scoring.")
    st.stop()

hold_norm = (df["hold_duration_days"] - df["hold_duration_days"].min()) / (
    df["hold_duration_days"].max() - df["hold_duration_days"].min() + 1e-9
)
fee_norm = (df["fee_loss"] - df["fee_loss"].min()) / (
    df["fee_loss"].max() - df["fee_loss"].min() + 1e-9
)

df["retention_risk_score"] = (0.6 * hold_norm + 0.4 * fee_norm) * 100

st.markdown("### 📈 Risk Score Distribution")
fig_hist = px.histogram(
    df,
    x="retention_risk_score",
    nbins=30,
    title="Distribution of Retention Risk Scores",
    color_discrete_sequence=["#8b0000"]
)
st.plotly_chart(fig_hist, use_container_width=True)

# Risk banding
bins = [0, 33, 66, 100]
labels = ["Low", "Medium", "High"]
df["risk_band"] = pd.cut(df["retention_risk_score"], bins=bins, labels=labels, include_lowest=True)

c1, c2, c3 = st.columns(3)
c1.metric("Low Risk Members", (df["risk_band"] == "Low").sum())
c2.metric("Medium Risk Members", (df["risk_band"] == "Medium").sum())
c3.metric("High Risk Members", (df["risk_band"] == "High").sum())

st.markdown("### 🧱 Risk by Segment")

seg_col = st.selectbox(
    "Group risk by:",
    ["membership_location", "application_subscription_membership_type", "application_contact_age_category", "reason_for_hold"]
)

risk_seg = (
    df.groupby([seg_col, "risk_band"])
    .size()
    .reset_index(name="count")
)

fig_seg = px.bar(
    risk_seg,
    x=seg_col,
    y="count",
    color="risk_band",
    barmode="stack",
    title=f"Retention Risk Bands by {seg_col}",
)
fig_seg.update_layout(xaxis_tickangle=-35)
st.plotly_chart(fig_seg, use_container_width=True)

st.markdown("### 🔝 High-Risk Members (Sample)")
st.dataframe(
    df.sort_values("retention_risk_score", ascending=False)
      .head(50)[[seg_col, "hold_duration_days", "fee_loss", "retention_risk_score"]],
    use_container_width=True
)
