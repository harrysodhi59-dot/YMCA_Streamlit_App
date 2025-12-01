import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.title("📊 Insights Summary")

@st.cache_data
def load_data():
    here = Path(__file__).resolve()
    base_dir = here.parent.parent
    csv_path = base_dir / "ymca_clusters.csv"
    
    st.write("📌 Using CSV path:", csv_path)
    return pd.read_csv(csv_path)

# Load dataset
df = load_data()

# KPIs
total_members = len(df)

unique_clusters = df["cluster_label"].nunique() if "cluster_label" in df.columns else "N/A"
most_common_cluster = df["cluster_label"].mode()[0] if "cluster_label" in df.columns else "N/A"
avg_age = round(df["age"].mean(), 2) if "age" in df.columns else "N/A"

# KPI Display
col1, col2, col3, col4 = st.columns(4)

col1.metric("👥 Total Members", total_members)
col2.metric("🧩 Unique Clusters", unique_clusters)
col3.metric("🏷 Most Common Cluster", most_common_cluster)
col4.metric("📅 Average Age", avg_age)

# Chart if cluster exists
if "cluster_label" in df.columns:
    fig = px.histogram(df, x="cluster_label", title="Cluster Distribution", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

# Dataset preview
st.write("### 🔍 Filtered Dataset Preview")
st.dataframe(df.head())
