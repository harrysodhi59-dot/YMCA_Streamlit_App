import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import numpy as np

st.markdown(
    "<h1 style='color:#8b0000;'>📊 Revenue & Hold Behaviour Insights</h1>",
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

# Detect cluster column
cluster_col = None
for c in df.columns:
    if "cluster" in c.lower():
        cluster_col = c
        break

# ==========================
# HIGH-LEVEL KPIs
# ==========================
st.markdown("### 🔢 Key Revenue & Behaviour Metrics")

total_fee_loss = df["fee_loss"].sum() if "fee_loss" in df.columns else np.nan
avg_fee_loss = df["fee_loss"].mean() if "fee_loss" in df.columns else np.nan
avg_hold_duration = df["hold_duration_days"].mean() if "hold_duration_days" in df.columns else np.nan
total_members = len(df)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Records", f"{total_members:,}")
if not np.isnan(total_fee_loss):
    col2.metric("Total Fee Loss", f"${total_fee_loss:,.0f}")
else:
    col2.metric("Total Fee Loss", "N/A")

if not np.isnan(avg_hold_duration):
    col3.metric("Avg Hold Duration", f"{avg_hold_duration:.1f} days")
else:
    col3.metric("Avg Hold Duration", "N/A")

if cluster_col is not None:
    col4.metric("Number of Clusters", df[cluster_col].nunique())
else:
    col4.metric("Number of Clusters", "N/A")

st.markdown("<hr>", unsafe_allow_html=True)

# ==========================
# DIMENSION SELECTION
# ==========================
st.markdown("### 🎛 Choose Dimension to Analyze")

dimension_options = []
col_map = {}

if "membership_location" in df.columns:
    dimension_options.append("Location")
    col_map["Location"] = "membership_location"

if "application_contact_age_category" in df.columns:
    dimension_options.append("Age Category")
    col_map["Age Category"] = "application_contact_age_category"

if "application_package_category" in df.columns:
    dimension_options.append("Package Category")
    col_map["Package Category"] = "application_package_category"

if "application_subscription_membership_type" in df.columns:
    dimension_options.append("Membership Type")
    col_map["Membership Type"] = "application_subscription_membership_type"

if "reason_for_hold" in df.columns:
    dimension_options.append("Reason for Hold")
    col_map["Reason for Hold"] = "reason_for_hold"

if cluster_col is not None:
    dimension_options.append("Cluster")
    col_map["Cluster"] = cluster_col

if not dimension_options:
    st.error("No valid categorical columns found for analysis.")
    st.stop()

dim_col1, dim_col2 = st.columns([2, 1])

selected_dimension = dim_col1.selectbox(
    "Analyze Fee Loss By:",
    options=dimension_options,
    index=0
)

selected_dim_col = col_map[selected_dimension]

top_n = dim_col2.slider("Top N Categories", min_value=3, max_value=15, value=8)

st.markdown("<hr>", unsafe_allow_html=True)

# ==========================
# MAIN BAR: FEE LOSS BY DIMENSION
# ==========================
if "fee_loss" in df.columns:
    st.markdown(f"### 💰 Fee Loss by {selected_dimension}")

    dim_group = (
        df.groupby(selected_dim_col)["fee_loss"]
        .sum()
        .reset_index()
        .sort_values("fee_loss", ascending=False)
        .head(top_n)
    )

    fig_main = px.bar(
        dim_group,
        x=selected_dim_col,
        y="fee_loss",
        title=f"Total Fee Loss by {selected_dimension} (Top {top_n})",
        labels={selected_dim_col: selected_dimension, "fee_loss": "Total Fee Loss"},
        text_auto=".2s",
        color="fee_loss",
        color_continuous_scale="Reds"
    )
    fig_main.update_layout(xaxis_tickangle=-35)
    st.plotly_chart(fig_main, use_container_width=True)

    # Simple narrative insight
    top_row = dim_group.iloc[0]
    st.info(
        f"📌 **Highest Fee Loss Segment:** {selected_dimension} = **{top_row[selected_dim_col]}**, "
        f"with approximately **${top_row['fee_loss']:,.0f}** in total fee loss."
    )

else:
    st.warning("Fee loss column not found, cannot compute fee loss by dimension.")

st.markdown("<hr>", unsafe_allow_html=True)

# ==========================
# DONUT: DISTRIBUTION OF RECORDS
# ==========================
st.markdown(f"### 🍩 Distribution of Records by {selected_dimension}")

cat_counts = df[selected_dim_col].value_counts().reset_index()
cat_counts.columns = [selected_dimension, "Count"]

fig_donut = px.pie(
    cat_counts,
    names=selected_dimension,
    values="Count",
    hole=0.5,
    title=f"Share of Records by {selected_dimension}",
    color_discrete_sequence=px.colors.sequential.Reds
)
st.plotly_chart(fig_donut, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ==========================
# CLUSTER PERFORMANCE PANEL
# ==========================
if cluster_col is not None and "fee_loss" in df.columns and "hold_duration_days" in df.columns:
    st.markdown("### 🧩 Cluster Performance Overview")

    cluster_summary = (
        df.groupby(cluster_col)[["fee_loss", "hold_duration_days"]]
        .agg(["mean", "sum", "count"])
    )
    # flatten columns
    cluster_summary.columns = [
        f"{a}_{b}" for a, b in cluster_summary.columns.to_flat_index()
    ]
    cluster_summary = cluster_summary.reset_index()

    # Add % of total fee loss
    total_loss = cluster_summary["fee_loss_sum"].sum()
    cluster_summary["fee_loss_share_%"] = (cluster_summary["fee_loss_sum"] / total_loss * 100).round(1)

    st.dataframe(cluster_summary, use_container_width=True)

    col_c1, col_c2 = st.columns(2)

    fig_cluster_fee = px.bar(
        cluster_summary,
        x=cluster_col,
        y="fee_loss_sum",
        title="Total Fee Loss by Cluster",
        labels={cluster_col: "Cluster", "fee_loss_sum": "Total Fee Loss"},
        text_auto=".2s",
        color="fee_loss_sum",
        color_continuous_scale="Reds"
    )
    col_c1.plotly_chart(fig_cluster_fee, use_container_width=True)

    fig_cluster_hold = px.bar(
        cluster_summary,
        x=cluster_col,
        y="hold_duration_days_mean",
        title="Average Hold Duration by Cluster",
        labels={cluster_col: "Cluster", "hold_duration_days_mean": "Avg Hold Duration (Days)"},
        text_auto=".1f"
    )
    col_c2.plotly_chart(fig_cluster_hold, use_container_width=True)

    # Insight
    worst_cluster = cluster_summary.sort_values("fee_loss_sum", ascending=False).iloc[0]
    st.warning(
        f"⚠️ **Cluster {worst_cluster[cluster_col]}** contributes the highest total fee loss "
        f"(${worst_cluster['fee_loss_sum']:,.0f}), representing **{worst_cluster['fee_loss_share_%']}%** "
        f"of all fee loss in the dataset."
    )

    st.markdown("<hr>", unsafe_allow_html=True)

# ==========================
# SCATTER: FEE LOSS VS HOLD DURATION
# ==========================
if "fee_loss" in df.columns and "hold_duration_days" in df.columns:
    st.markdown("### 📈 Fee Loss vs Hold Duration")

    if cluster_col is not None:
        fig_scatter = px.scatter(
            df,
            x="hold_duration_days",
            y="fee_loss",
            color=cluster_col,
            title="Fee Loss vs Hold Duration (Colored by Cluster)",
            labels={"hold_duration_days": "Hold Duration (Days)", "fee_loss": "Fee Loss"},
            opacity=0.7
        )
    else:
        fig_scatter = px.scatter(
            df,
            x="hold_duration_days",
            y="fee_loss",
            title="Fee Loss vs Hold Duration",
            labels={"hold_duration_days": "Hold Duration (Days)", "fee_loss": "Fee Loss"},
            opacity=0.7
        )
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)

# ==========================
# HOLD REASON vs AGE GROUP
# ==========================
if "reason_for_hold" in df.columns and "application_contact_age_category" in df.columns:
    st.markdown("### 🧠 Hold Reason by Age Group")

    reason_age = (
        df.groupby(["reason_for_hold", "application_contact_age_category"])
        .size()
        .reset_index(name="count")
    )

    fig_reason_age = px.bar(
        reason_age,
        x="reason_for_hold",
        y="count",
        color="application_contact_age_category",
        barmode="group",
        title="Hold Reasons by Age Group",
        labels={
            "reason_for_hold": "Reason for Hold",
            "count": "Number of Holds",
            "application_contact_age_category": "Age Category",
        }
    )
    fig_reason_age.update_layout(xaxis_tickangle=-35)
    st.plotly_chart(fig_reason_age, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)

# ==========================
# OPTIONAL: TREEMAP OF FEE LOSS
# ==========================
if "fee_loss" in df.columns and "membership_location" in df.columns and "application_contact_age_category" in df.columns:
    st.markdown("### 🌳 Fee Loss Treemap (Location + Age Category)")

    treemap_df = (
        df.groupby(["membership_location", "application_contact_age_category"])["fee_loss"]
        .sum()
        .reset_index()
    )

    fig_tree = px.treemap(
        treemap_df,
        path=["membership_location", "application_contact_age_category"],
        values="fee_loss",
        title="Fee Loss by Location and Age Category"
    )
    st.plotly_chart(fig_tree, use_container_width=True)

# ==========================
# END
# ==========================
