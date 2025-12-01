import streamlit as st
import pandas as pd

st.title("📄 Data Overview")

@st.cache_data
def load_data():
    return pd.read_csv("../data/ymca_clusters.csv")
import os
st.write("📌 Current Working Directory:", os.getcwd())
st.write("📂 Files in current directory:", os.listdir())
st.write("📂 Files in parent directory:", os.listdir(".."))

df = load_data()

st.write("### Sample Data")
st.dataframe(df.head())

st.write(f"📊 Rows: {len(df)}")
st.write(f"📁 Columns: {df.shape[1]}")
