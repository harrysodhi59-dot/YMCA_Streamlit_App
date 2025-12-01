import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px

st.title("📊 Insights Summary")

# << COPY THIS EXACTLY FROM PAGE 1 >>
@st.cache_data
def load_data():
    here = Path(__file__).resolve()
    base_dir = here.parent.parent
    csv_path = base_dir / "data" / "ymca_clusters.csv"

    st.write("📌 Using CSV path:", str(csv_path))

    return pd.read_csv(csv_path)

# Load dataset
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
col4.metric("📅 Avg Days on Hold", round(filtered_df["avg_hold_days"].mean(), 1))

# Preview table
st.write("### 📄 Filtered Dataset Preview")
st.dataframe(filtered_df.head())

# Chart
st.write("### 📈 Cluster Distribution")
chart = px.histogram(filtered_df, x="cluster_label", nbins=10, title="Cluster Distribution")
st.plotly_chart(chart)
