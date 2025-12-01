import streamlit as st
import pandas as pd
from pathlib import Path

st.title("📊 Insights Summary")

@st.cache_data
def load_data():
    here = Path(__file__).resolve()
    base_dir = here.parent.parent
    csv_path = base_dir / "ymca_clusters.csv"
    return pd.read_csv(csv_path)

df = load_data()

# Sidebar Filters
st.sidebar.header("🔍 Filters")

# Cluster Filter (if column exists)
cluster_col = "clusters" if "clusters" in df.columns else None

if cluster_col:
    selected_clusters = st.sidebar.multiselect(
        "Select Clusters:", 
        options=sorted(df[cluster_col].unique()), 
        default=sorted(df[cluster_col].unique())
    )
    df_filtered = df[df[cluster_col].isin(selected_clusters)]
else:
    df_filtered = df

# Metrics Row
col1, col2, col3, col4 = st.columns(4)

col1.metric("👤 Total Members", len(df_filtered))
col2.metric("📈 Unique Clusters", df_filtered[cluster_col].nunique() if cluster_col else "N/A")
col3.metric("🎯 Most Common Cluster", df_filtered[cluster_col].mode()[0] if cluster_col else "N/A")

# Average Age (if column exists)
age_col = None
for col in ["Age", "age", "member_age"]:
    if col in df.columns:
        age_col = col
        break

if age_col:
    avg_age = round(df_filtered[age_col].mean(), 1)
    col4.metric("📅 Avg Age", avg_age)
else:
    col4.metric("📅 Avg Age", "N/A")

st.write("---")
st.write("### 💡 Filtered Dataset Preview")
st.dataframe(df_filtered.head())
