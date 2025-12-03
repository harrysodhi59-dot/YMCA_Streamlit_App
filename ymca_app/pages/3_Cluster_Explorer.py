import streamlit as st
import pandas as pd
from pathlib import Path

st.title("🔍 Cluster Explorer")

@st.cache_data
def load_data():
    here = Path(__file__).resolve()
    base_dir = here.parent.parent
    excel_path = base_dir / "ymca_clusters.xlsx"

    st.write("📌 Using Excel path:", str(excel_path))

    df = pd.read_excel(excel_path, engine="openpyxl")

    # convert date column
    if "start_date" in df.columns:
        df["start_date"] = pd.to_datetime(df["start_date"], errors="coerce")

    return df

df = load_data()

# Automatically find cluster column
cluster_col = None
for col in df.columns:
    if "cluster" in col.lower():
        cluster_col = col
        break

if cluster_col is None:
    st.error("❌ No cluster column found in this Excel file.")
    st.stop()

st.success(f"🎯 Cluster Column Detected: **{cluster_col}**")

# Dropdown for cluster selection
cluster_options = sorted(df[cluster_col].unique())
selected_cluster = st.selectbox("Select Cluster", cluster_options)

filtered = df[df[cluster_col] == selected_cluster]

st.write("### 📄 Filtered Data Preview")
st.dataframe(filtered.head())

# Show numeric columns for charts
numeric_cols = filtered.select_dtypes(include=['int64', 'float64']).columns.tolist()

if len(numeric_cols) == 0:
    st.warning("⚠️ No numeric columns available for visualization.")
else:
    st.write("### 📊 Statistics")
    st.write(filtered[numeric_cols].describe())
