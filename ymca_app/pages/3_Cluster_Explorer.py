import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.title("🔍 Cluster Explorer")

@st.cache_data
def load_data():
    here = Path(__file__).resolve()
    base_dir = here.parent.parent
    csv_path = base_dir / "ymca_clusters.csv"
    
    st.write("📌 Using CSV path:", csv_path)
    return pd.read_csv(csv_path)

df = load_data()

# Check if cluster column exists
if "cluster_label" not in df.columns:
    st.error("⚠️ The dataset does not contain a `cluster_label` column.")
    st.stop()

# Sidebar filter
cluster_options = sorted(df["cluster_label"].unique())
selected_cluster = st.sidebar.selectbox("Select Cluster Group:", cluster_options)

st.subheader(f"📍 Showing Cluster: **{selected_cluster}**")

cluster_df = df[df["cluster_label"] == selected_cluster]

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("👥 Members in Cluster", len(cluster_df))
col2.metric("📅 Avg Age", round(cluster_df["age"].mean(), 2) if "age" in cluster_df.columns else "N/A")
col3.metric("💰 Avg Fee Loss", round(cluster_df["fee_loss"].mean(), 2) if "fee_loss" in cluster_df.columns else "N/A")

# Chart: Age Distribution
if "age" in cluster_df.columns:
    st.write("📊 Age Distribution")
    fig1 = px.histogram(cluster_df, x="age", title="Age Distribution", nbins=20)
    st.plotly_chart(fig1, use_container_width=True)

# Chart: Membership Type Breakdown
if "membership_subscription_type" in cluster_df.columns:
    st.write("📌 Membership Type Breakdown")
    fig2 = px.pie(cluster_df, names="membership_subscription_type", title="Membership Type Split")
    st.plotly_chart(fig2, use_container_width=True)

# Show dataset
st.write("📄 Members in this Cluster")
st.dataframe(cluster_df.head(50))
