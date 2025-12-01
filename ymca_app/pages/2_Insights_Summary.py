import streamlit as st
import pandas as pd
from pathlib import Path

st.title("📊 Insights Summary")

# ------------------------
# Load Dataset
# ------------------------
@st.cache_data
def load_data():
    here = Path(__file__).resolve()
    base_dir = here.parent.parent  # go up to ymca_app
    csv_path = base_dir / "data" / "ymca_clusters.csv"
    return pd.read_csv(csv_path)

df = load_data()

# ------------------------
# DEBUG: Show Column Names
# ------------------------
st.write("🧪 DEBUG: Column names in dataset:")
st.write(list(df.columns))



# ------------------------
# Auto-detect Clust
