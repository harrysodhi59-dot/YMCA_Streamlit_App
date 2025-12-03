import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import numpy as np

# ==========================
# PAGE TITLE
# ==========================
st.markdown(
    "<h1 style='color:#8b0000;'>🧩 Cluster Intelligence Lab</h1>",
    unsafe_allow_html=True
)
st.write("Deep-dive into cluster characteristics, behaviour patterns, and revenue impact.")

# ==========================
# LOAD DATA
# ==========================
@st.cache_data
def load_data():
    here = Path(__file__).resolve()
    base_dir = here.parent.parent
    excel_path = base_dir / "ymca_clusters.xlsx"
    df = pd.read_excel(excel_path, engine="openpyxl")
    return df

df = load_data()

# Detect cluster column
cluster_col = None
for c in df.columns:
    if "cluster" in c.lower():
        cluster_col = c
        break

if cluster_col is None:
    st.error("No cluster column found in dataset!")
    st.stop()

clusters = sorted(df[cluster_col].unique())

# ==========================
# SELECT CLUSTER
# ==========================
st.markdown("### 🎛 Cluster Selection")

col_sel1, col_sel2 = st.columns([3, 1])

selected_cluster = col_sel1.selectbox(
    "Select Cluster to Explore",
    options=clusters
)

compare_mode = col_sel2.radio(
    "Comparison Mode",
    ["Single Cluster", "Compare All"]
)

filtered_df = df[df[cluster_col] == selected_cluster]

# ==========================
# CLUSTER KPI PANEL
# ==========================

st.markdown(f"## 🔍 Cluster {selected_cluster} Summary")

cluster_size = len(filtered_df)
total_size = len(df)
cluster_share = (cluster_size / total_size) * 100

avg_fee_loss = filtered_df["fee_loss"].mean()
avg_hold_duration = filtered_df["hold_duration_days"].mean()
avg_acc = filtered_df["avg_hold_account"].mean()
avg_contact = filtered_df["avg_hold_contact"].mean()

k1, k2, k3, k4 = st.columns(4)

k1.metric("Cluster Size", f"{cluster_size:,}")
k2.metric("Cluster Share", f"{cluster_share:.1f}%")
k3.metric("Avg Fee Loss", f"${avg_fee_loss:,.0f}")
k4.metric("Avg Hold Duration", f"{avg_hold_duration:.1f} days")

# Behaviour summary
st.markdown("<hr>", unsafe_allow_html=True)

st.markdown("### 🧠 Behavioural Interpretation")

if avg_hold_duration > df["hold_duration_days"].mean():
    hold_msg = "longer than average holds (high churn risk)"
else:
    hold_msg = "shorter, more stable hold patterns"

if avg_fee_loss > df["fee_loss"].mean():
    fee_msg = "high fee loss impact"
else:
    fee_msg = "low fee loss contribution"

st.info(
    f"Cluster **{selected_cluster}** shows **{hold_msg}** and **{fee_msg}**. "
    f"Members in this group typically pause memberships for **{avg_hold_duration:.1f} days**, "
    f"costing around **${avg_fee_loss:,.0f}** per member."
)

st.markdown("<hr>", unsafe_allow_html=True)

# ==========================
# RADAR CHART FOR CLUSTER
# ==========================
st.markdown("### 🕸 Cluster Radar Profile")

metrics = ["fee_loss", "hold_duration_days", "avg_hold_account", "avg_hold_contact"]
metric_labels = ["Fee Loss", "Hold Duration", "Avg Hold (Account)", "Avg Hold (Contact)"]

cluster_means = df.groupby(cluster_col)[metrics].mean()

radar_values = cluster_means.loc[selected_cluster].values.tolist()
radar_values.append(radar_values[0])  # loop back

fig_radar = go.Figure()

fig_radar.add_trace(go.Scatterpolar(
    r=radar_values,
    theta=metric_labels + [metric_labels[0]],
    fill='toself',
    name=f'Cluster {selected_cluster}',
    line_color="red"
))

fig_radar.update_layout(
    polar=dict(radialaxis=dict(visible=True)),
    showlegend=False
)

st.plotly_chart(fig_radar, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ==========================
# DISTRIBUTION CHARTS
# ==========================
st.markdown("## 📊 Cluster Composition Breakdown")

cat_cols = {
    "Age Category": "application_contact_age_category",
    "Membership Type": "application_subscription_membership_type",
    "Package Category": "application_package_category",
    "Reason for Hold": "reason_for_hold",
    "Location": "membership_location"
}

for title, col_name in cat_cols.items():
    if col_name in df.columns:
        st.markdown(f"### {title}")

        dist = filtered_df[col_name].value_counts().reset_index()
        dist.columns = [title, "Count"]

        fig = px.bar(
            dist,
            x=title,
            y="Count",
            text="Count",
            title=f"{title} Distribution in Cluster {selected_cluster}",
            color="Count",
            color_continuous_scale="Reds"
        )
        fig.update_layout(xaxis_tickangle=-35)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("<hr>", unsafe_allow_html=True)

# ==========================
# SCATTER: Fee Loss vs Hold Duration
# ==========================
st.markdown("### 📈 Cluster Scatter — Fee Loss vs Hold Duration")

fig_scatter = px.scatter(
    df,
    x="hold_duration_days",
    y="fee_loss",
    color=cluster_col,
    opacity=0.7,
    title="Fee Loss vs Hold Duration (All Clusters)"
)

# highlight selected cluster
highlight = filtered_df
fig_scatter.add_trace(
    go.Scatter(
        x=highlight["hold_duration_days"],
        y=highlight["fee_loss"],
        mode="markers",
        marker=dict(size=12, color="black"),
        name=f"Cluster {selected_cluster}"
    )
)

st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ==========================
# HEATMAP: CLUSTER COMPARISON (if compare mode)
# ==========================
if compare_mode == "Compare All":
    st.markdown("## 🔥 Cluster Comparison Heatmap")

    heat_df = df.groupby(cluster_col)[metrics].mean()

    fig_heat = px.imshow(
        heat_df,
        labels=dict(x="Metric", y="Cluster", color="Value"),
        x=metric_labels,
        title="Cluster Comparison Heatmap"
    )

    st.plotly_chart(fig_heat, use_container_width=True)
