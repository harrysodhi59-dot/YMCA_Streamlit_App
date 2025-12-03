import streamlit as st
import pandas as pd
from pathlib import Path

st.markdown(
    "<h1 style='color:#8b0000;'>📊 Pivot Explorer</h1>",
    unsafe_allow_html=True
)

st.write("Build custom summaries by choosing rows, columns, and metrics – similar to Excel / Power BI pivot tables.")

@st.cache_data
def load_data():
    here = Path(__file__).resolve()
    base_dir = here.parent.parent
    excel_path = base_dir / "ymca_clusters.xlsx"
    df = pd.read_excel(excel_path, engine="openpyxl")
    return df

df = load_data()

# Split columns by type
num_cols = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
cat_cols = df.select_dtypes(include=["object"]).columns.tolist()

# Controls
st.markdown("### 🎛 Pivot Controls")

c1, c2, c3 = st.columns(3)

index_col = c1.selectbox(
    "Row index (group by):",
    options=cat_cols,
    index=cat_cols.index("membership_location") if "membership_location" in cat_cols else 0
)

columns_col = c2.selectbox(
    "Column groups (optional):",
    options=["(None)"] + cat_cols,
    index=0
)

value_col = c3.selectbox(
    "Value (metric):",
    options=num_cols,
    index=num_cols.index("fee_loss") if "fee_loss" in num_cols else 0
)

aggfunc = st.selectbox(
    "Aggregation function:",
    options=["sum", "mean", "count"],
    index=0
)

# Build pivot table
kwargs = {}
if columns_col != "(None)":
    kwargs["columns"] = columns_col

pivot = pd.pivot_table(
    df,
    index=index_col,
    values=value_col,
    aggfunc=aggfunc,
    **kwargs,
    fill_value=0
)

st.markdown("### 📊 Pivot Table Result")
st.dataframe(pivot, use_container_width=True)

# Download as CSV
csv = pivot.to_csv().encode("utf-8")
st.download_button(
    label="📥 Download Pivot as CSV",
    data=csv,
    file_name="ymca_pivot_export.csv",
    mime="text/csv"
)
