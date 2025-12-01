import streamlit as st
import pandas as pd

st.title("📊 Insights Summary")

# ------------ FIXED LOAD FUNCTION -----------
@st.cache_data
def load_data():
    csv_path = "/mount/src/ymca_streamlit_app/ymca_app/data/ymca_clusters.csv"
    st.write("📌 Using CSV path:", csv_path)
    return pd.read_csv(csv_path)

df = load_data()

# ------------------------
# Calculations
# ------------------------
total_members = len(df)

# Try to detect cluster column automatically
cluster_cols = [c for c in df.columns if "cluster" in c.lower()]
cluster_col = cluster_cols[0] if cluster_cols else None

unique_clusters = df[cluster_col].nunique() if cluster_col else "N/A"
most_common_cluster = df[cluster_col].mode()[0] if cluster_col else "N/A"

# Detect age column
age_cols = [c for c in df.columns if "age" in c.lower()]
age_col = age_cols[0] if age_cols else None

average_age = round(df[age_col].mean(), 1) if age_col else "N/A"


# ------------------------
# Summary UI
# ------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("👥 Total Members", f"{total_members:,}")
col2.metric("🔢 Unique Clusters", unique_clusters)
col3.metric("🏷 Most Common Cluster", most_common_cluster)
col4.metric("📅 Avg Age", average_age)


st.write("---")
st.subheader("🔍 Dataset Preview")
st.dataframe(df.head(20))
