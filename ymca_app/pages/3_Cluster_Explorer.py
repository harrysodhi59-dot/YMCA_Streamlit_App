import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px

st.title("🔍 Cluster Explorer")

@st.cache_data
def load_data():
    here = Path(__file__).resolve()
    base_dir = here.parent.parent  # go back to /ymca_app
    data_path = base_dir / "ymca_clusters.csv"

    st.write("📌 Using CSV path:", str(data_path))

    return pd.read_csv(data_path)

df = load_data()

st.write("🧪 Columns in dataset:")
st.write(list(df.columns))

# Try to detect the cluster column
possible_cluster_columns = [col for col in df.columns if "cluster" in col.lower()]

st.write("🔍 Searching for anything similar to 'cluster_label'...")
st.write(possible_cluster_columns)

if len(possible_cluster_columns) == 0:
    st.error("❌ No cluster column found. Check column spelling.")
    st.stop()

# Use the first matching column
cluster_column = possible_cluster_columns[0]

st.success(f"🎯 Cluster Column Detected: `{cluster_column}`")

# Sidebar Filter
selected_cluster = st.sidebar.selectbox(
    "Select Cluster", sorted(df[cluster_column].unique())
)

filtered_df = df[df[cluster_column] == selected_cluster]

st.write("### 📊 Filtered Data Preview")
st.dataframe(filtered_df.head())

# Optional: Plot
numeric_columns = filtered_df.select_dtypes(include=['number']).columns

if len(numeric_columns) > 0:
    feature = st.selectbox("Select feature to visualize", numeric_columns)
    fig = px.histogram(filtered_df, x=feature, title=f"{feature} Distribution in Cluster {selected_cluster}")
    st.plotly_chart(fig)
else:
    st.warning("⚠ No numeric columns available for visualization.")
