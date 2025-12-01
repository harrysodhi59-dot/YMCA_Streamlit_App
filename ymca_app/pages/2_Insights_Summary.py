import streamlit as st
import pandas as pd
from pathlib import Path

st.title("📊 Insights Summary")

# ------------------------
# Load Dataset using same logic as first page
# ------------------------
@st.cache_data
def load_data():
    # Path of THIS file: ymca_app/pages/2_Insights_Summary.py
    here = Path(__file__).resolve()
    
    # go up to ymca_app folder
    base_dir = here.parent.parent  

    # Load data from the same file used in page 1
    csv_path = base_dir / "data" / "ymca_clusters.csv"

    st.write("📌 Using CSV path:", str(csv_path))  # Debug

    return pd.read_csv(csv_path)

df = load_data()

# ------------------------
# DEBUG: Show Column Names
# ------------------------
st.write("🧪 DEBUG: Column names in dataset:")
st.write(list(df.columns))

# ------------------------
# Auto-detect Cluster Column
# ------------------------
cluster_cols = [c for c in df.columns if "cluster" in c.lower()]
cluster_col = cluster_cols[0] if cluster_cols else None

# ------------------------
# Auto-detect Age Column
# ------------------------
age_cols = [c for c in df.columns if "age" in c.lower()]
age_col = age_cols[0] if age_cols else None

# ------------------------
# Calculations
# ------------------------
total_members = len(df)
unique_clusters = df[cluster_col].nunique() if cluster_col else None
most_common_cluster = df[cluster_col].mode()[0] if cluster_col else None
average_age = round(df[age_col].mean(), 1) if age_col else None

# ------------------------
# UI Metrics
# ------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("👥 Total Members", f"{total_members:,}"_
