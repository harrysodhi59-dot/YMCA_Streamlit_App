import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px

st.title("📊 Insights Summary")

# -----------------------------
# Load Dataset
# -----------------------------
@st.cache_data
def load_data():
    here = Path(__file__).resolve()
    base_dir = here.parent.parent
    csv_path = base_dir / "data" / "ymca_clusters.csv"
    return pd.read_csv(csv_path)

df = load_data()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔍 Filters")

# Location Filter
if "membership_location" in df.columns:
    locations = sorted(df["membership_location"].dropna().unique())
    selected_locations = st.sidebar.multiselect("Filter by Location", locations)

    if selected_locations:
        df = df[df["membership_location"].isin(selected_locations)]

# Cluster Filter
if "cluster_label" in df.columns:
    clusters = sorted(df["cluster_label"].dropna().unique())
    selected_clusters = st.sidebar.multiselect("Filter by Cluster", clusters)

    if selected_clusters:
        df = df[df["cluster_label"].isin(selected_clusters)]

# -----------------------------
# KPI Metrics
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("🧍 Total Members", len(df))
col2.metric("🔢 Unique Clusters", df["cluster_label"].nunique())
col3.metric("📌 Most Common Cluster", int(df["cluster_label"].mode()[0]) if len(df) > 0 else "N/A")

# Try to detect age column
age_col = None
for c in df.columns:
    if "age" in c.lower():
        age_col = c

if age_col:
    col4.metric("🎂 Average Age", round(df[age_col].mean(), 1))
else:
    col4.metric("🎂 Average Age", "N/A")

st.write("---")


# -----------------------------
# Visualizations
# -----------------------------

st.subheader("📍 Cluster Distribution")
fig1 = px.pie(df, names="cluster_label", title="Members per Cluster")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("📍 Top Membership Locations")
top_locations = df["membership_location"].value_counts().head(10)
fig2 = px.bar(top_locations, title="Top 10 YMCA Membership Locations")
st.plotly_chart(fig2, use_container_width=True)

if age_col:
    st.subheader("🎂 Age Distribution")
    fig3 = px.histogram(df, x=age_col, nbins=20, title="Age Frequency")
    st.plotly_chart(fig3, use_container_width=True)


# -----------------------------
# Dataset Preview
# -----------------------------
st.write("🧾 Filtered Dataset Preview")
st.dataframe(df.head())

# -----------------------------
# Download Option
# -----------------------------
csv = df.to_csv(index=False)
st.download_button("⬇️ Download Filtered Data", data=csv, file_name="filtered_members.csv", mime="text/csv")
