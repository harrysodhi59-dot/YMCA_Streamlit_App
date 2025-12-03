import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(layout="wide")

# -----------------------------
# Load Excel Dataset
# -----------------------------
@st.cache_data
def load_data():
    here = Path(__file__).resolve()
    base = here.parent.parent
    file_path = base / "ymca_clusters.xlsx"
    return pd.read_excel(file_path)

df = load_data()

# -----------------------------
# Page Title
# -----------------------------
st.markdown("""
<h1 style='color:#8A0303;'>🔍 Cluster Explorer</h1>
<p style='font-size:18px;'>Explore behavioral and financial characteristics of each cluster.</p>
""", unsafe_allow_html=True)

# -----------------------------
# Validate cluster column
# -----------------------------
if "cluster_label" not in df.columns:
    st.error("❌ The file is missing 'cluster_label' column. Cannot explore clusters.")
    st.write("Available columns:", list(df.columns))
    st.stop()

clusters = sorted(df["cluster_label"].unique())
cluster_choice = st.selectbox("Select a Cluster", clusters)

filtered = df[df["cluster_label"] == cluster_choice]

st.markdown(f"## 📊 Cluster {cluster_choice} Summary")

# -----------------------------
# 1️⃣ Summary Metrics
# -----------------------------
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Total Members", len(filtered))

with c2:
    st.metric("Avg Membership Fee", round(filtered["membership_fee"].mean(), 2))

with c3:
    st.metric("Avg Hold Duration (Days)", round(filtered["hold_duration_days"].mean(), 2))

with c4:
    st.metric("Avg Revenue Loss", round(filtered["fee_loss"].mean(), 2))

# -----------------------------
# 2️⃣ Select Numeric Column for Visualization
# -----------------------------
numeric_cols = ["membership_fee", "hold_duration_days", "fee_loss", "age_at_hold"]
num_col = st.selectbox("Choose numeric field to visualize:", numeric_cols)

# Histogram
fig1 = px.histogram(filtered, x=num_col, nbins=30,
                    title=f"Distribution of {num_col} for Cluster {cluster_choice}",
                    color_discrete_sequence=["#8A0303"])
st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# 3️⃣ Categorical Column Breakdown
# -----------------------------
categorical_cols = [
    "membership_location",
    "application_package_category",
    "application_subscription_membership_type",
    "reason_for_hold",
    "application_contact_age_category",
    "application_contact_gender",
    "hold_duration_group",
    "cluster_name"
]

cat_col = st.selectbox("Break down by category:", categorical_cols)

fig2 = px.bar(
    filtered[cat_col].value_counts().reset_index(),
    x="index", y=cat_col,
    title=f"{cat_col} Distribution – Cluster {cluster_choice}",
    color_discrete_sequence=["#AA2B2B"]
)
fig2.update_layout(xaxis_title=cat_col, yaxis_title="Count")
st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# 4️⃣ Revenue Scatter (Fee vs Loss)
# -----------------------------
fig3 = px.scatter(
    filtered, x="membership_fee", y="fee_loss",
    color="hold_duration_group",
    size="hold_duration_days",
    title="💸 Fee vs Revenue Loss (Bubble Shows Hold Days)",
    color_discrete_sequence=px.colors.sequential.OrRd
)
st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# 5️⃣ Raw Data Preview
# -----------------------------
st.markdown("## 🧾 Filtered Dataset Preview")
st.dataframe(filtered.head(50))

