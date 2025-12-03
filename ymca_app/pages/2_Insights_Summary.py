import streamlit as st
import pandas as pd
from pathlib import Path

st.title("📊 Insights Summary")

@st.cache_data
def load_data():
    here = Path(__file__).resolve()
    base_dir = here.parent.parent
    excel_path = base_dir / "ymca_clusters.xlsx"

    st.write("📌 Using Excel path:", str(excel_path))

    df = pd.read_excel(excel_path, engine="openpyxl")

    # Fix dates if present
    if "start_date" in df.columns:
        df["start_date"] = pd.to_datetime(df["start_date"], errors="coerce")

    return df

df = load_data()

st.metric("Total Members", len(df))

if "cluster_label" in df.columns:
    st.metric("Unique Clusters", df["cluster_label"].nunique())
    st.metric("Most Common Cluster", int(df["cluster_label"].mode()[0]))
else:
    st.warning("⚠️ No cluster_label column found in dataset")

# Age average (based on age_at_hold)
if "age_at_hold" in df.columns:
    st.metric("Avg Age", round(df["age_at_hold"].mean(), 2))
