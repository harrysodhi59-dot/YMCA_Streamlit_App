import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ==========================
# PAGE TITLE
# ==========================
st.markdown(
    "<h1 style='color:#8b0000;'>📂 Data Foundation & Quality Check</h1>",
    unsafe_allow_html=True
)

# ==========================
# LOAD DATA
# ==========================
@st.cache_data
def load_data():
    here = Path(__file__).resolve()
    base_dir = here.parent.parent
    excel_path = base_dir / "ymca_clusters.xlsx"

    df = pd.read_excel(excel_path, engine="openpyxl")

    # Convert date column if present
    if "start_date" in df.columns:
        df["start_date"] = pd.to_datetime(df["start_date"], errors="coerce")

    return df

df = load_data()

# ==========================
# KPI CARDS
# ==========================
st.markdown("### 🔢 Key Dataset Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Records", f"{len(df):,}")
col2.metric("Total Columns", df.shape[1])
col3.metric("Unique Locations", df["membership_location"].nunique())
col4.metric("Unique Age Categories", df["application_contact_age_category"].nunique())

st.markdown("<hr>", unsafe_allow_html=True)

# ==========================
# SAMPLE PREVIEW
# ==========================
st.markdown("### 🧾 Sample Data Preview")
st.dataframe(df.head(20), use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ==========================
# MISSING VALUE ANALYSIS
# ==========================
st.markdown("### 🚨 Missing Value Summary")

missing_df = (
    df.isnull().sum()
    .reset_index()
    .rename(columns={"index": "Column", 0: "Missing Values"})
)
missing_df["Missing %"] = round((missing_df["Missing Values"] / len(df)) * 100, 2)

st.dataframe(missing_df, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ==========================
# COLUMN DETAILS
# ==========================
st.markdown("### 📑 Column Information")

col_info = pd.DataFrame({
    "Column": df.columns,
    "Datatype": df.dtypes.astype(str),
    "Unique Values": [df[col].nunique() for col in df.columns]
})

st.dataframe(col_info, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ==========================
# LOCATION DISTRIBUTION
# ==========================
st.markdown("### 🏢 Distribution of Members by Location")

location_counts = df["membership_location"].value_counts().reset_index()
location_counts.columns = ["Location", "Count"]

fig_loc = px.bar(
    location_counts,
    x="Location",
    y="Count",
    text="Count",
    title="Members per YMCA Location",
    color="Count",
    color_continuous_scale="Reds"
)

fig_loc.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_loc, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ==========================
# AGE CATEGORY DISTRIBUTION
# ==========================
st.markdown("### 🎂 Age Category Breakdown")

fig_age = px.pie(
    df,
    names="application_contact_age_category",
    title="Age Distribution",
    color_discrete_sequence=px.colors.sequential.Reds
)

st.plotly_chart(fig_age, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ==========================
# OPTIONAL FILTERS
# ==========================
st.markdown("### 🔍 Explore Data by Filters (Optional)")

loc_filter = st.selectbox("Filter by Location", ["All"] + df["membership_location"].unique().tolist())

if loc_filter != "All":
    df_filtered = df[df["membership_location"] == loc_filter]
else:
    df_filtered = df

st.write(f"Showing **{len(df_filtered):,}** records")
st.dataframe(df_filtered.head(20), use_container_width=True)
