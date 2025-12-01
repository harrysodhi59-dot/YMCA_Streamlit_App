import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px

st.title("📊 Insights Summary")

@st.cache_data
def load_data():
    here = Path(__file__).resolve()
    data_path = here.parent.parent / "data" / "ymca_clusters.csv"

    st.write("📌 Looking for file here:", str(data_path))

    return pd.read_csv(data_path)

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filters")
locations = df["membership_location"].unique()
selected = st.sidebar.multiselect("Select Location(s):", locations, default=locations)

filtered_df = df[df["membership_location"].isin(selected)]

# KPI Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("👥 Total Members", len(filtered_df))
col2.metric("🔢 Unique Clusters", df["cluster_label"].nunique())
col3.metric("🏷 Most Common Cluster", int(df["cluster_label"].mode()[0]))
col4.metric("📅 Avg Age", round(filtered_df["avg_hold_days"].mean(), 1))

st.write("### 📄 Filtered Dataset Preview")
st.dataframe(filtered_df.head())

# Optional chart example
st.write("### 📈 Members per Cluster")
chart = px.histogram(filtered_df, x="cluster_label", nbins=10, title="Cluster Distribution")
st.plotly_chart(chart)
