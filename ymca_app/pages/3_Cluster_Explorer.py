import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px

st.title("🔍 Cluster Explorer")

@st.cache_data
def load_data():
    here = Path(__file__).resolve()
    base_dir = here.parent.parent
    data_path = base_dir / "ymca_clusters.csv"

    st.write("📌 Using CSV path:", str(data_path))

    df = pd.read_csv(data_path)

    # Convert numeric columns safely
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="ignore")

    return df

df = load_data()

# Show dataset columns for debugging
st.write("🧾 Columns in dataset:", list(df.columns))

# Detect cluster label column
possible_names = ["cluster", "cluster_label", "labels", "segment"]
cluster_column = None

for name in possible_names:
    if name in df.columns:
        cluster_column = name
        break

if cluster_column:
    st.success(f"🎯 Cluster Column Detected: **{cluster_column}**")
else:
    st.error("❌ No cluster column found.")
    st.stop()

# Cluster selection dropdown
clusters = sorted(df[cluster_column].unique())
selected_cluster = st.selectbox("Select Cluster", clusters)

filtered_df = df[df[cluster_column] == selected_cluster]

st.subheader("📊 Filtered Dataset Preview")
st.dataframe(filtered_df.head())

# Identify numeric columns
numeric_cols = filtered_df.select_dtypes(include="number").columns.tolist()

if not numeric_cols:
    st.warning("⚠ No numeric columns available for visualization.")
else:
    st.subheader("📈 Distribution of Numeric Features")
    feature = st.selectbox("Choose a feature to plot", numeric_cols)

    fig = px.histogram(filtered_df, x=feature, nbins=20, title=f"{feature} Distribution")
    st.plotly_chart(fig, use_container_width=True)
