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


# -------- Detect Cluster Column --------
possible_cluster_names = ["cluster", "clusters", "label", "segment", "Cluster"]
cluster_col = None

for name in possible_cluster_names:
    if name in df.columns:
        cluster_col = name
        break


# -------- Detect Age Column --------
possible_age_cols = ["age", "Age", "member_age", "Age_Years", "AGE"]
age_col = None

for col in possible_age_cols:
    if col in df.columns:
        age_col = col
        break


# -------- Sidebar Filters --------
st.sidebar.header("🔍 Filters")

df_filtered = df.copy()

# Filter by Cluster if available
if cluster_col:
    selected_clusters = st.sidebar.multiselect(
        "Select Cluster:", 
        options=sorted(df[cluster_col].unique()),
        default=sorted(df[cluster_col].unique())
    )
    df_filtered = df_filtered[df_filtered[cluster_col].isin(selected_clusters)]

st.write("---")


# -------- Metrics Display --------
col1, col2, col3, col4 = st.columns(4)

col1.metric("👤 Total Members", len(df_filtered))

if cluster_col:
    col2.metric("📈 Unique Clusters", df_filtered[cluster_col].nunique())
    col3.metric("🏷 Most Common Cluster", df_filtered[cluster_col].mode()[0])
else:
    col2.metric("📈 Unique Clusters", "N/A")
    col3.metric("🏷 Most Common Cluster", "N/A")

if age_col:
    col4.metric("📅 Average Age", round(df_filtered[age_col].mean(), 1))
else:
    col4.metric("📅 Average Age", "N/A")


# -------- Table Preview --------
st.write("### 💡 Filtered Dataset Preview")
st.dataframe(df_filtered.head())
