import streamlit as st
import pandas as pd
from pathlib import Path

st.title("📄 Data Overview")

@st.cache_data
def load_data():
    # Path of THIS file: ymca_app/pages/1_Data_Overview.py
    here = Path(__file__).resolve()
    # Go up one level → ymca_app
    base_dir = here.parent.parent
    # Build path to data/ymca_clusters.csv
    csv_path = base_dir / "data" / "ymca_clusters.csv"

    # Small debug info to be sure
    st.write("📌 Using CSV path:", str(csv_path))

    return pd.read_csv(csv_path)

df = load_data()

st.write("### Sample Data")
st.dataframe(df.head())

st.write(f"📊 Rows: {len(df)}")
st.write(f"📁 Columns: {df.shape[1]}")
