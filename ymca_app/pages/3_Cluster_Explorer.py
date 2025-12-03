import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px

st.title("📄 Data Overview")

# ------------ LOAD DATA ------------
@st.cache_data
def load_data():
    here = Path(__file__).resolve()
    base_dir = here.parent.parent
    file_path = base_dir / "ymca_clusters.xlsx"

    df = pd.read_excel(file_path, engine="openpyxl")
    if "start_date" in df.columns:
        df["start_date"] = pd.to_datetime(df["start_date"], errors="coerce")
    return df

df = load_data()

# ------------ KPIs ------------
st.markdown("### **📊 Dataset Summary**")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Records", f"{len(df):,}")
col2.metric("Locations", df["membership_location"].nunique())
col3.metric("Package Types", df["application_package_category"].nunique())
col4.metric("Clusters", df["cluster_label"].nunique())

st.markdown("---")

# ------------ PREVIEW ------------
st.subheader("🔍 Sample Data")
st.dataframe(df.head(20), use_container_width=True)

# ------------ LOCATION DISTRIBUTION ------------
st.subheader("🏢 Members by Location")
loc_counts = df["membership_location"].value_counts().reset_index()
loc_counts.columns = ["location", "count"]
fig = px.bar(loc_counts, x="location", y="count", title="Membership Distribution by Location")
fig.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig, use_container_width=True)

# ------------ AGE GROUP ------------
if "application_contact_age_category" in df.columns:
    st.subheader("🎂 Age Category Breakdown")
    fig_age = px.pie(df, names="application_contact_age_category", title="Age Segment Distribution")
    st.plotly_chart(fig_age, use_container_width=True)
