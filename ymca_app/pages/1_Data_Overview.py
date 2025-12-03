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

# Detect cluster column if present
cluster_col = None
for c in df.columns:
    if "cluster" in c.lower():
        cluster_col = c
        break

# ==========================
# FILTERS SECTION
# ==========================
st.markdown("### 🎛 Interactive Filters")

with st.expander("Click to expand filters", expanded=True):
    col_f1, col_f2, col_f3 = st.columns(3)
    col_f4, col_f5, col_f6 = st.columns(3)

    # Location filter
    if "membership_location" in df.columns:
        locations = sorted(df["membership_location"].dropna().unique().tolist())
        loc_sel = col_f1.multiselect(
            "Membership Location",
            options=locations,
            default=locations
        )
    else:
        loc_sel = None

    # Package category
    if "application_package_category" in df.columns:
        pkg = sorted(df["application_package_category"].dropna().unique().tolist())
        pkg_sel = col_f2.multiselect(
            "Package Category",
            options=pkg,
            default=pkg
        )
    else:
        pkg_sel = None

    # Membership type
    if "application_subscription_membership_type" in df.columns:
        mtypes = sorted(df["application_subscription_membership_type"].dropna().unique().tolist())
        mtype_sel = col_f3.multiselect(
            "Membership Type",
            options=mtypes,
            default=mtypes
        )
    else:
        mtype_sel = None

    # Age category
    if "application_contact_age_category" in df.columns:
        ages = sorted(df["application_contact_age_category"].dropna().unique().tolist())
        age_sel = col_f4.multiselect(
            "Age Category",
            options=ages,
            default=ages
        )
    else:
        age_sel = None

    # Reason for hold
    if "reason_for_hold" in df.columns:
        reasons = sorted(df["reason_for_hold"].dropna().unique().tolist())
        reason_sel = col_f5.multiselect(
            "Reason for Hold",
            options=reasons,
            default=reasons
        )
    else:
        reason_sel = None

    # Cluster filter
    if cluster_col is not None:
        clusters = sorted(df[cluster_col].dropna().unique().tolist())
        cluster_sel = col_f6.multiselect(
            "Cluster",
            options=clusters,
            default=clusters
        )
    else:
        cluster_sel = None

    # Date range filter
    date_range = None
    if "start_date" in df.columns:
        min_date = df["start_date"].dropna().min()
        max_date = df["start_date"].dropna().max()
        if pd.notna(min_date) and pd.notna(max_date):
            date_range = st.date_input(
                "Filter by Start Date Range",
                value=(min_date.date(), max_date.date())
            )

# Apply filters
filtered_df = df.copy()

if loc_sel is not None and len(loc_sel) > 0:
    filtered_df = filtered_df[filtered_df["membership_location"].isin(loc_sel)]

if pkg_sel is not None and len(pkg_sel) > 0:
    filtered_df = filtered_df[filtered_df["application_package_category"].isin(pkg_sel)]

if mtype_sel is not None and len(mtype_sel) > 0:
    filtered_df = filtered_df[filtered_df["application_subscription_membership_type"].isin(mtype_sel)]

if age_sel is not None and len(age_sel) > 0:
    filtered_df = filtered_df[filtered_df["application_contact_age_category"].isin(age_sel)]

if reason_sel is not None and len(reason_sel) > 0:
    filtered_df = filtered_df[filtered_df["reason_for_hold"].isin(reason_sel)]

if cluster_sel is not None and len(cluster_sel) > 0 and cluster_col is not None:
    filtered_df = filtered_df[filtered_df[cluster_col].isin(cluster_sel)]

if date_range is not None and "start_date" in df.columns:
    start_d, end_d = date_range
    filtered_df = filtered_df[
        (filtered_df["start_date"].dt.date >= start_d) &
        (filtered_df["start_date"].dt.date <= end_d)
    ]

st.write(f"📌 Showing **{len(filtered_df):,}** records after filters.")

st.markdown("<hr>", unsafe_allow_html=True)

# ==========================
# KPI CARDS (on filtered data)
# ==========================
st.markdown("### 🔢 Key Metrics (Filtered Subset)")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Records", f"{len(filtered_df):,}")
col2.metric("Total Columns", filtered_df.shape[1])

if "membership_location" in filtered_df.columns:
    col3.metric("Unique Locations", filtered_df["membership_location"].nunique())
else:
    col3.metric("Unique Locations", "N/A")

if "application_contact_age_category" in filtered_df.columns:
    col4.metric("Age Groups", filtered_df["application_contact_age_category"].nunique())
else:
    col4.metric("Age Groups", "N/A")

st.markdown("<hr>", unsafe_allow_html=True)

# ==========================
# SAMPLE PREVIEW
# ==========================
st.markdown("### 🧾 Sample Data Preview (Filtered)")
st.dataframe(filtered_df.head(20), use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ==========================
# MISSING VALUE ANALYSIS (FULL DATASET)
# ==========================
st.markdown("### 🚨 Missing Value Summary (Full Dataset)")

missing_df = (
    df.isnull().sum()
    .reset_index()
    .rename(columns={"index": "Column", 0: "Missing Values"})
)
missing_df["Missing %"] = round((missing_df["Missing Values"] / len(df)) * 100, 2)

st.dataframe(missing_df, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ==========================
# COLUMN DETAILS (FULL DATASET)
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
# ADVANCED GRAPHS (ON FILTERED DATA)
# ==========================

# 1. Members by Location
if "membership_location" in filtered_df.columns:
    st.markdown("### 🏢 Members by Location (Filtered)")
    loc_counts = filtered_df["membership_location"].value_counts().reset_index()
    loc_counts.columns = ["Location", "Count"]

    fig_loc = px.bar(
        loc_counts,
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

# 2. Age Category Breakdown
if "application_contact_age_category" in filtered_df.columns:
    st.markdown("### 🎂 Age Category Breakdown (Filtered)")
    fig_age = px.pie(
        filtered_df,
        names="application_contact_age_category",
        title="Age Distribution",
        color_discrete_sequence=px.colors.sequential.Reds
    )
    st.plotly_chart(fig_age, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)

# 3. Hold Duration Histogram
if "hold_duration_days" in filtered_df.columns:
    st.markdown("### ⏳ Hold Duration Distribution (Days)")
    fig_hold = px.histogram(
        filtered_df,
        x="hold_duration_days",
        nbins=30,
        title="Distribution of Hold Duration (Days)"
    )
    st.plotly_chart(fig_hold, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)

# 4. Membership Fee Distribution
if "membership_fee" in filtered_df.columns:
    st.markdown("### 💳 Membership Fee Distribution")
    fig_fee = px.box(
        filtered_df,
        y="membership_fee",
        title="Membership Fee Distribution (Box Plot)"
    )
    st.plotly_chart(fig_fee, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)

# 5. Fee Loss by Location
if "fee_loss" in filtered_df.columns and "membership_location" in filtered_df.columns:
    st.markdown("### 💰 Total Fee Loss by Location")
    fee_loc = (
        filtered_df.groupby("membership_location")["fee_loss"]
        .sum()
        .reset_index()
        .sort_values("fee_loss", ascending=False)
    )
    fig_fee_loc = px.bar(
        fee_loc,
        x="membership_location",
        y="fee_loss",
        title="Total Fee Loss by Location",
        labels={"membership_location": "Location", "fee_loss": "Total Fee Loss"},
        color="fee_loss",
        color_continuous_scale="Reds"
    )
    fig_fee_loc.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_fee_loc, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)

# 6. Cluster Comparison (Average Fee Loss & Hold Duration)
if cluster_col is not None and "fee_loss" in filtered_df.columns and "hold_duration_days" in filtered_df.columns:
    st.markdown("### 🧩 Cluster Comparison (Avg Fee Loss & Hold Duration)")

    cluster_summary = (
        filtered_df.groupby(cluster_col)[["fee_loss", "hold_duration_days"]]
        .mean()
        .reset_index()
        .round(2)
    )

    fig_cluster = px.bar(
        cluster_summary,
        x=cluster_col,
        y=["fee_loss", "hold_duration_days"],
        barmode="group",
        title="Cluster Comparison: Avg Fee Loss & Hold Duration",
        labels={"value": "Average", "variable": "Metric"}
    )
    st.plotly_chart(fig_cluster, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)

# 7. Hold Reason vs Age Group
if "reason_for_hold" in filtered_df.columns and "application_contact_age_category" in filtered_df.columns:
    st.markdown("### 🧠 Hold Reason by Age Group")

    reason_age = (
        filtered_df.groupby(["reason_for_hold", "application_contact_age_category"])
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
        labels={"reason_for_hold": "Reason", "count": "Members", "application_contact_age_category": "Age Group"}
    )
    fig_reason_age.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_reason_age, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)

# 8. Fee Loss vs Hold Duration Scatter (with clusters if available)
if "fee_loss" in filtered_df.columns and "hold_duration_days" in filtered_df.columns:
    st.markdown("### 📈 Fee Loss vs Hold Duration")

    if cluster_col is not None:
        fig_scatter = px.scatter(
            filtered_df,
            x="hold_duration_days",
            y="fee_loss",
            color=cluster_col,
            title="Fee Loss vs Hold Duration (Colored by Cluster)",
            labels={"hold_duration_days": "Hold Duration (Days)", "fee_loss": "Fee Loss"}
        )
    else:
        fig_scatter = px.scatter(
            filtered_df,
            x="hold_duration_days",
            y="fee_loss",
            title="Fee Loss vs Hold Duration",
            labels={"hold_duration_days": "Hold Duration (Days)", "fee_loss": "Fee Loss"}
        )

    st.plotly_chart(fig_scatter, use_container_width=True)
