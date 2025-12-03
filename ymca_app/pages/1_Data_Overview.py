import streamlit as st
import pandas as pd
from pathlib import Path

st.title("📄 Data Overview")

@st.cache_data
def load_data():
    here = Path(__file__).resolve()
    base_dir = here.parent.parent  # ymca_app folder
    excel_path = base_dir / "ymca_clusters.xlsx"

    st.write("📌 Using Excel path:", str(excel_path))

    df = pd.read_excel(excel_path, engine="openpyxl")

    # Convert dates
    if "start_date" in df.columns:
        df["start_date"] = pd.to_datetime(df["start_date"], errors="coerce")

    return df

df = load_data()

st.write("### Sample Data")
st.dataframe(df.head())

st.write(f"📊 Rows: {len(df)}")
st.write(f"📁 Columns: {df.shape[1]}")
