import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.markdown(
    "<h1 style='color:#8b0000;'>🗺 Revenue at Risk by Location</h1>",
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

if "fee_loss" not in df.columns or "membership_location" not in df.columns:
    st.error("Need 'fee_loss' and 'membership_location' columns.")
    st.stop()

loc_summary = (
    df.groupby("membership_location")[["fee_loss", "hold_duration_days"]]
    .agg(["sum", "mean", "count"])
)
loc_summary.columns = [f"{a}_{b}" for a, b in loc_summary.columns.to_flat_index()]
loc_summary = loc_summary.reset_index()

# Risk bucket
q = loc_summary["fee_loss_sum"].quantile([0.33, 0.66]).values
def bucket(x):
    if x <= q[0]:
        return "Low"
    elif x <= q[1]:
        return "Medium"
    else:
        return "High"

loc_summary["risk_level"] = loc_summary["fee_loss_sum"].apply(bucket)

st.markdown("### 📊 Location Risk Table")
st.dataframe(loc_summary, use_container_width=True)

st.markdown("### 💰 Total Fee Loss by Location")
fig = px.bar(
    loc_summary.sort_values("fee_loss_sum", ascending=False),
    x="membership_location",
    y="fee_loss_sum",
    color="risk_level",
    title="Total Fee Loss & Risk Level by Location",
)
fig.update_layout(xaxis_tickangle=-35, yaxis_title="Total Fee Loss")
st.plotly_chart(fig, use_container_width=True)

st.markdown("### ⏳ Avg Hold Duration vs Fee Loss")
fig2 = px.scatter(
    loc_summary,
    x="hold_duration_days_mean",
    y="fee_loss_sum",
    size="fee_loss_sum",
    color="risk_level",
    hover_name="membership_location",
    title="Avg Hold Duration vs Total Fee Loss by Location",
    labels={"hold_duration_days_mean": "Avg Hold Duration (Days)", "fee_loss_sum": "Total Fee Loss"}
)
st.plotly_chart(fig2, use_container_width=True)
