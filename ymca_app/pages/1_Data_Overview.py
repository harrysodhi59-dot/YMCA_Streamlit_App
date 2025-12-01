import streamlit as st
import pandas as pd

st.title("📄 Data Overview")

@st.cache_data
def load_data():
    return pd.read_csv("ymca_app/data/ymca_clusters.csv")

df = load_data()

st.write("### Sample Data")
st.dataframe(df.head())

st.write(f"📊 Rows: {len(df)}")
st.write(f"📁 Columns: {df.shape[1]}")
