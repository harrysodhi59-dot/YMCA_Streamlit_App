import streamlit as st
import pandas as pd
from pathlib import Path

st.title("📄 Data Overview")

@st.cache_data
def load_data():
    # Get folder where THIS file exists → /ymca_app/pages
    here = Path(__file__).resolve()
    
    # Go up to parent folder → /ymca_app
    base_dir = here.parent.parent
    
    # CSV file path
    csv_path = base_dir / "ymca_clusters.csv"

    st.write("📌 Using CSV path:", csv_path)

    return pd.read_csv(csv_path)

# Load
df = load_data()

# Display preview
st.write("### Sample Data Preview")
st.dataframe(df.head())

# Dataset stats
st.write(f"📊 **Total Rows:** {len(df)}")
st.write(f"📁 **Total Columns:** {df.shape[1]}")
