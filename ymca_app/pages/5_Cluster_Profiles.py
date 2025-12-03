import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.markdown(
    "<h1 style='color:#8b0000;'>🧬 Cluster Profiling Lab</h1>",
    unsafe_allow_html=True
)

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
    if "cluster_label" in c.lower() or "cluster_name" in c.lower() or c.lower() == "cluster":
        cluster_col = c
        break

if not cluster_col:
    st.error("No cluster column found (cluster_label / cluster_name).")
    st.stop()

clusters = sorted(df[cluster_col].dropna().unique().tolist())

st.markdown("### 🎛 Cluster Selection")
c1, c2 = st.columns([3, 1])
selected_clusters = c1.multiselect(
    "Select clusters to profile:",
    options=clusters,
    default=clusters
)
if not selected_clusters:
    st.warning("Please select at least one cluster.")
    st.stop()

compare_mode = c2.radio("Comparison mode:", ["Single view", "Compare all"], index=1)

df_sel = df[df[cluster_col].isin(selected_clusters)]

# Metrics to profile
metric_cols = []
for col in ["fee_loss", "hold_duration_days", "membership_fee", "avg_hold_contact", "age_at_hold"]:
    if col in df.columns:
        metric_cols.append(col)

if not metric_cols:
    st.error("No numeric profile metrics found (fee_loss, hold_duration_days, membership_fee, avg_hold_contact, age_at_hold).")
    st.stop()

# Cluster summary table
st.markdown("### 📊 Cluster Summary Table")

summary = df_sel.groupby(cluster_col)[metric_cols].agg(["mean", "sum", "count"])
summary.columns = [f"{a}_{b}" for a, b in summary.columns.to_flat_index()]
summary = summary.reset_index()

st.dataframe(summary, use_container_width=True)

# Radar chart for first selected cluster
st.markdown("### 🕸 Radar Profile (First Selected Cluster)")
first_cluster = selected_clusters[0]
cluster_means = df.groupby(cluster_col)[metric_cols].mean()

values = cluster_means.loc[first_cluster].values.tolist()
values.append(values[0])  # close loop

labels = metric_cols + [metric_cols[0]]

fig_radar = go.Figure()
fig_radar.add_trace(go.Scatterpolar(
    r=values,
    theta=labels,
    fill='toself',
    name=f"Cluster {first_cluster}",
    line_color="#8b0000"
))
fig_radar.update_layout(
    showlegend=False,
    polar=dict(radialaxis=dict(visible=True))
)
st.plotly_chart(fig_radar, use_container_width=True)

# Bar: total fee_loss vs hold_duration per cluster
st.markdown("### 💰 Fee Loss & Hold Duration by Cluster")

if "fee_loss" in df.columns and "hold_duration_days" in df.columns:
    cluster_bar = (
        df_sel.groupby(cluster_col)[["fee_loss", "hold_duration_days"]]
        .mean()
        .reset_index()
        .round(2)
    )
    fig_bar = px.bar(
        cluster_bar,
        x=cluster_col,
        y=["fee_loss", "hold_duration_days"],
        barmode="group",
        title="Avg Fee Loss & Hold Duration per Cluster",
        labels={"value": "Average", "variable": "Metric"},
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# Distribution by age category & membership type per cluster
st.markdown("### 🧱 Composition by Age & Membership Type")

comp_cols = []
if "application_contact_age_category" in df.columns:
    comp_cols.append(("Age Category", "application_contact_age_category"))
if "application_subscription_membership_type" in df.columns:
    comp_cols.append(("Membership Type", "application_subscription_membership_type"))

for title, col in comp_cols:
    st.markdown(f"#### {title} Distribution (Selected Clusters)")
    comp = (
        df_sel.groupby([cluster_col, col])
        .size()
        .reset_index(name="count")
    )
    fig_comp = px.bar(
        comp,
        x=cluster_col,
        y="count",
        color=col,
        barmode="group",
        title=f"{title} by Cluster",
    )
    st.plotly_chart(fig_comp, use_container_width=True)

# Behaviour insight text
st.markdown("### 🧠 Behaviour Insights (Auto-generated)")

for cl in selected_clusters:
    sub = df[df[cluster_col] == cl]
    size = len(sub)
    avg_hold = sub["hold_duration_days"].mean() if "hold_duration_days" in sub.columns else None
    avg_loss = sub["fee_loss"].mean() if "fee_loss" in sub.columns else None

    desc = f"- **Cluster {cl}** → {size} records"
    if avg_hold is not None:
        desc += f", avg hold ≈ {avg_hold:.1f} days"
    if avg_loss is not None:
        desc += f", avg fee loss ≈ ${avg_loss:,.0f}"
    st.write(desc)
