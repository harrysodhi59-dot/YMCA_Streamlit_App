import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.markdown(
    "<h1 style='color:#8b0000;'>🔎 Segment Deep Dive</h1>",
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

# Segment columns
seg_cols = {
    "Location": "membership_location",
    "Membership Type": "application_subscription_membership_type",
    "Package Category": "application_package_category",
    "Age Category": "application_contact_age_category",
    "Reason for Hold": "reason_for_hold",
    "Cluster": "cluster_label" if "cluster_label" in df.columns else None,
}

seg_cols = {k: v for k, v in seg_cols.items() if v is not None}

seg_name = st.selectbox("Select segment dimension:", list(seg_cols.keys()))
seg_col = seg_cols[seg_name]

values = sorted(df[seg_col].dropna().unique().tolist())
seg_value = st.selectbox(f"Choose a {seg_name} to analyze:", values)

sub = df[df[seg_col] == seg_value]

st.markdown(f"## 📌 Segment: {seg_name} = **{seg_value}**")

c1, c2, c3 = st.columns(3)
c1.metric("Members in Segment", f"{len(sub):,}")
if "fee_loss" in sub.columns:
    c2.metric("Total Fee Loss", f"${sub['fee_loss'].sum():,.0f}")
if "hold_duration_days" in sub.columns:
    c3.metric("Avg Hold Duration", f"{sub['hold_duration_days'].mean():.1f} days")

st.markdown("### 💳 Membership Fee & Fee Loss (If Available)")
if "membership_fee" in sub.columns and "fee_loss" in sub.columns:
    fig_scatter = px.scatter(
        sub,
        x="membership_fee",
        y="fee_loss",
        title="Membership Fee vs Fee Loss",
        color="hold_duration_group" if "hold_duration_group" in sub.columns else None,
        opacity=0.7
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("### ⏳ Hold Duration Distribution")
if "hold_duration_days" in sub.columns:
    fig_hold = px.histogram(
        sub,
        x="hold_duration_days",
        nbins=30,
        title="Hold Duration (Days)",
        color_discrete_sequence=["#8b0000"]
    )
    st.plotly_chart(fig_hold, use_container_width=True)

st.markdown("### 🧱 Cluster Mix (If Cluster Available)")
if "cluster_label" in sub.columns:
    cl_counts = sub["cluster_label"].value_counts().reset_index()
    cl_counts.columns = ["cluster_label", "count"]
    fig_cl = px.bar(
        cl_counts,
        x="cluster_label",
        y="count",
        title="Cluster Distribution in This Segment",
        color_discrete_sequence=["#8b0000"]
    )
    st.plotly_chart(fig_cl, use_container_width=True)

st.markdown("### 🧾 Sample Records")
st.dataframe(sub.head(50), use_container_width=True)
