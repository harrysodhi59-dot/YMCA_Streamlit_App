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

    # Auto-detect delimiter (tab, comma, etc.)
    try:
        df = pd.read_csv(data_path, sep=None, engine="python")
    except Exception:
        # fallback in case auto-detect fails
        df = pd.read_csv(data_path, delimiter="\t")

    # Convert numeric-like values
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="ignore")

    return df


# Load dataset
try:
    df = load_data()
except Exception as e:
    st.error(f"❌ Could not read file. Error: {e}")
    st.stop()

# Show columns
st.subheader("🧾 Columns in dataset:")
st.write(list(df.columns))

# Detect cluster column
possible_cluster_cols = [
    col for col in df.columns if "cluster" in col.lower()
]

if not possible_cluster_cols:
    st.error("❌ No cluster column found in the dataset.")
    st.stop()

cluster_column = possible_cluster_cols[0]  # pick the first match

st.success(f"🎯 Cluster Column Detected: **{cluster_column}**")

# Dropdown to select cluster
unique_clusters = sorted(df[cluster_column].unique())
selected_cluster = st.selectbox("📌 Select a Cluster", unique_clusters)

# Filter dataset by selected cluster
filtered_df = df[df[cluster_column] == selected_cluster]

st.subheader("📊 Filtered Data Preview")
st.write(filtered_df.head(10))

# Check for numeric columns for visualization
numeric_cols = filtered_df.select_dtypes(include=["float64", "int64"]).columns.tolist()

if not numeric_cols:
    st.warning("⚠️ No numeric columns available for visualization.")
else:
    st.subheader("📈 Numeric Feature Distribution")
    selected_feature = st.selectbox("Pick a numeric column to visualize:", numeric_cols)

    fig = px.histogram(
        filtered_df,
        x=selected_feature,
        nbins=20,
        title=f"Distribution of '{selected_feature}' for Cluster {selected_cluster}",
        color_discrete_sequence=['#0174BE']
    )
    st.plotly_chart(fig, use_container_width=True)
