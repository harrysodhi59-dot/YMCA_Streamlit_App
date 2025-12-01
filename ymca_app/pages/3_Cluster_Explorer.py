import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.title("🔍 Cluster Explorer")

@st.cache_data
def load_data():
    here = Path(__file__).resolve()
    base_dir = here.parent.parent
    csv_path = base_dir / "ymca_clusters.csv"
    
    st.write("📌 Using CSV path:", csv_path)
    return pd.read_csv(csv_path)

df = load_data()

# ---- CONFIRMED cluster column ----
cluster_column = "cluster_label"
st.success(f"🎯 Cluster Column Detected: `{cluster_column}`")

# Sidebar dropdown
cluster_options = sorted(df[cluster_column].unique())
selected_cluster = st.sidebar.selectbox("Select Cluster Group:", cluster_options)

# Filter dataframe
cluster_df = df[df[cluster_column] == selected_cluster]

st.subheader(f"📍 Cluster {selected_cluster} Summary")

# =========================
# KPI Cards
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("👥 Members in Cluster", len(cluster_df))

# Age available? No exact age column exists, but we have category
if "application_contact_age_category" in df.columns:
    most_common_age_group = cluster_df["application_contact_age_category"].mode()[0]
    col2.metric("👶 Most Common Age Group", most_common_age_group)
else:
    col2.metric("👶 Age Group", "N/A")

# Fee loss metric
if "fee_loss" in df.columns:
    col3.metric("💰 Avg Fee Loss", round(cluster_df["fee_loss"].mean(), 2))
else:
    col3.metric("💰 Avg Fee Loss", "N/A")


# =========================
# Charts
# =========================

st.write("### 📈 Membership Fee Distribution")
fig1 = px.box(cluster_df, y="membership_fee", title=f"Membership Fee Distribution in Cluster {selected_cluster}")
st.plotly_chart(fig1, use_container_width=True)

st.write("### 🧠 Reason for Hold Breakdown")
fig2 = px.bar(
    cluster_df["reason_for_hold"].value_counts(),
    title="Most Common Hold Reasons"
)
st.plotly_chart(fig2, use_container_width=True)

# =========================
# Table Preview
# =========================
st.write("### 📄 Members in This Cluster")
st.dataframe(cluster_df.head(50))
