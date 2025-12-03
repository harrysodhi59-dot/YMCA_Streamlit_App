import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Cluster Explorer | Data Alchemists",
    layout="wide",
)

st.title("🔍 Cluster Explorer")

# -----------------------------
# Load Excel
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("ymca_app/ymca_clusters.xlsx")
    return df

df = load_data()

st.success("📌 Excel Loaded Successfully")
st.write(f"### Columns in dataset:")
st.code(list(df.columns))

# -----------------------------
# Identify cluster column
# -----------------------------
cluster_col = None
possible = ["cluster_label", "cluster", "cluster_name"]

for col in df.columns:
    if col.lower() in possible:
        cluster_col = col
        break

if not cluster_col:
    st.error("❌ No cluster column found in the file.")
    st.stop()

st.success(f"🎯 Cluster Column Detected: **{cluster_col}**")

# -----------------------------
# Sidebar Cluster Filter
# -----------------------------
clusters = sorted(df[cluster_col].unique())
cluster_choice = st.selectbox("Select Cluster:", clusters)

filtered = df[df[cluster_col] == cluster_choice]

st.subheader(f"📊 Cluster {cluster_choice} Summary")

st.write("### Filtered Data Preview")
st.dataframe(filtered.head(50), use_container_width=True)

# -----------------------------
# Numeric Summary
# -----------------------------
numeric_cols = filtered.select_dtypes(include=["float64", "int64"]).columns.tolist()

if len(numeric_cols) > 0:
    st.write("### 📈 Numeric Feature Summary")
    st.dataframe(filtered[numeric_cols].describe(), use_container_width=True)
else:
    st.warning("⚠️ No numeric columns found!")

# -----------------------------
# Category Breakdown (Bar Chart)
# -----------------------------
st.write("---")
st.write("## 📊 Category Breakdown")

all_cat_cols = filtered.select_dtypes(include=["object"]).columns.tolist()
selected_cat = st.selectbox("Break down by category:", all_cat_cols)

# ---- FIXED BAR CHART CODE ----
cat_counts = (
    filtered[selected_cat]
    .fillna("Unknown")
    .astype(str)
    .value_counts()
    .reset_index()
)

cat_counts.columns = ["category", "count"]

fig = px.bar(
    cat_counts,
    x="category",
    y="count",
    title=f"{selected_cat} Distribution – Cluster {cluster_choice}",
    color_discrete_sequence=["#AA2B2B"]
)
fig.update_layout(
    xaxis_title=selected_cat,
    yaxis_title="Count",
    xaxis={'categoryorder':'total descending'}
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Numeric Visualizer
# -----------------------------
st.write("---")
st.write("## 📈 Numeric Feature Visualizer")

if len(numeric_cols) >= 2:
    num_x = st.selectbox("Select X-Axis:", numeric_cols, key="x_axis")
    num_y = st.selectbox("Select Y-Axis:", numeric_cols, key="y_axis")

    fig2 = px.scatter(
        filtered,
        x=num_x,
        y=num_y,
        color_discrete_sequence=["#AA2B2B"],
        title=f"{num_x} vs {num_y} (Cluster {cluster_choice})",
    )

    st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning("⚠️ Not enough numeric columns for scatter plot.")

# -----------------------------
# Histogram Section
# -----------------------------
st.write("---")
st.write("## 📊 Numeric Histogram")

num_hist = st.selectbox("Select numeric column:", numeric_cols)

fig3 = px.histogram(
    filtered,
    x=num_hist,
    nbins=25,
    color_discrete_sequence=["#AA2B2B"],
    title=f"Histogram of {num_hist}"
)
st.plotly_chart(fig3, use_container_width=True)

# End
