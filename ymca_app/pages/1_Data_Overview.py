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

st.write("Explore the cleaned & clustered YMCA dataset, check data quality, and slice by key dimensions.")

# ==========================
# LOAD DATA
# ==========================
@st.cache_data
def load_data():
    here = Path(__file__).resolve()
    base_dir = here.parent.parent        # ymca_app/
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
    if "cluster_label" in c.lower() or "cluster" in c.lower():
        cluster_col = c
        break

# ==========================
# DATA DICTIONARY / SCHEMA
# ==========================
st.markdown("### 📑 Data Dictionary")

# Build schema table
schema = pd.DataFrame({
    "Column": df.columns,
    "Datatype": df.dtypes.astype(str),
    "Non-Null Count": df.notnull().sum().values,
    "Missing Count": df.isnull().sum().values,
    "Missing %": (df.isnull().sum().values / len(df) * 100).round(2),
    "Unique Values": [df[col].nunique() for col in df.columns],
    "Example Value": [df[col].dropna().iloc[0] if df[col].notna().any() else "" for col in df.columns]
})

# Column search
search_term = st.text_input("🔎 Search column name (optional):", "")

if search_term.strip():
    schema_filtered = schema[schema["Column"].str.contains(search_term.strip(), case=False, na=False)]
else:
    schema_filtered = schema

st.dataframe(schema_filtered, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ==========================
# FILTERS
# ==========================
st.markdown("### 🎛 Interactive Filters")

with st.expander("Click to expand filters", expanded=True):
    f1, f2, f3 = st.columns(3)
    f4, f5, f6 = st.columns(3)

    # Location
    if "membership_location" in df.columns:
        loc_opts = sorted(df["membership_location"].dropna().unique().tolist())
        loc_sel = f1.multiselect("Membership Location", loc_opts, default=loc_opts)
    else:
        loc_sel = None

    # Package category
    if "application_package_category" in df.columns:
        pkg_opts = sorted(df["application_package_category"].dropna().unique().tolist())
        pkg_sel = f2.multiselect("Package Category", pkg_opts, default=pkg_opts)
    else:
        pkg_sel = None

    # Membership type
    if "application_subscription_membership_type" in df.columns:
        mtype_opts = sorted(df["application_subscription_membership_type"].dropna().unique().tolist())
        mtype_sel = f3.multiselect("Membership Type", mtype_opts, default=mtype_opts)
    else:
        mtype_sel = None

    # Age category
    if "application_contact_age_category" in df.columns:
        age_opts = sorted(df["application_contact_age_category"].dropna().unique().tolist())
        age_sel = f4.multiselect("Age Category", age_opts, default=age_opts)
    else:
        age_sel = None

    # Reason for hold
    if "reason_for_hold" in df.columns:
        reason_opts = sorted(df["reason_for_hold"].dropna().unique().tolist())
        reason_sel = f5.multiselect("Reason for Hold", reason_opts, default=reason_opts)
    else:
        reason_sel = None

    # Cluster
    if cluster_col is not None:
        cluster_opts = sorted(df[cluster_col].dropna().unique().tolist())
        cluster_sel = f6.multiselect("Cluster", cluster_opts, default=cluster_opts)
    else:
        cluster_sel = None

    # Date range
    date_range = None
    if "start_date" in df.columns and df["start_date"].notna().any():
        min_date = df["start_date"].min().date()
        max_date = df["start_date"].max().date()
        date_range = st.date_input(
            "Filter by Start Date Range",
            value=(min_date, max_date)
        )

# Apply filters to dataframe
df_filt = df.copy()

if loc_sel is not None:
    df_filt = df_filt[df_filt["membership_location"].isin(loc_sel)]

if pkg_sel is not None:
    df_filt = df_filt[df_filt["application_package_category"].isin(pkg_sel)]

if mtype_sel is not None:
    df_filt = df_filt[df_filt["application_subscription_membership_type"].isin(mtype_sel)]

if age_sel is not None:
    df_filt = df_filt[df_filt["application_contact_age_category"].isin(age_sel)]

if reason_sel is not None:
    df_filt = df_filt[df_filt["reason_for_hold"].isin(reason_sel)]

if cluster_sel is not None and cluster_col is not None:
    df_filt = df_filt[df_filt[cluster_col].isin(cluster_sel)]

if date_range is not None and "start_date" in df.columns:
    start_d, end_d = date_range
    df_filt = df_filt[
        (df_filt["start_date"].dt.date >= start_d) &
        (df_filt["start_date"].dt.date <= end_d)
    ]

st.write(f"📌 Showing **{len(df_filt):,}** records after filters.")
st.markdown("<hr>", unsafe_allow_html=True)

# ==========================
# KPI CARDS (FILTERED)
# ==========================
st.markdown("### 🔢 Key Metrics (Filtered Subset)")

k1, k2, k3, k4 = st.columns(4)

k1.metric("Total Records", f"{len(df_filt):,}")

if "membership_location" in df_filt.columns:
    k2.metric("Unique Locations", df_filt["membership_location"].nunique())
else:
    k2.metric("Unique Locations", "N/A")

if "fee_loss" in df_filt.columns:
    k3.metric("Total Fee Loss", f"${df_filt['fee_loss'].sum():,.0f}")
else:
    k3.metric("Total Fee Loss", "N/A")

if "hold_duration_days" in df_filt.columns:
    k4.metric("Avg Hold Duration", f"{df_filt['hold_duration_days'].mean():.1f} days")
else:
    k4.metric("Avg Hold Duration", "N/A")

st.markdown("<hr>", unsafe_allow_html=True)

# ==========================
# SAMPLE PREVIEW (FILTERED)
# ==========================
st.markdown("### 🧾 Sample Data Preview (Filtered)")
st.dataframe(df_filt.head(20), use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ==========================
# MISSING VALUE HEATMAP (TOP 200 ROWS)
# ==========================
st.markdown("### 🚨 Missing Value Heatmap (Top 200 Rows)")

if len(df) > 0:
    miss_sample = df.head(200).isnull().astype(int)
    if miss_sample.sum().sum() == 0:
        st.success("✅ No missing values in the first 200 rows.")
    else:
        fig_miss = px.imshow(
            miss_sample.T,
            color_continuous_scale="Reds",
            aspect="auto",
            labels=dict(x="Row Index", y="Column", color="Missing"),
            title="Missing Value Pattern (1 = missing, 0 = present)"
        )
        st.plotly_chart(fig_miss, use_container_width=True)
else:
    st.info("No data available to show missing value heatmap.")

st.markdown("<hr>", unsafe_allow_html=True)

# ==========================
# VISUALS ON FILTERED DATA
# ==========================

# 1. Members by Location
if "membership_location" in df_filt.columns:
    st.markdown("### 🏢 Members by Location (Filtered)")

    loc_counts = (
        df_filt["membership_location"]
        .value_counts()
        .reset_index()
        .rename(columns={"index": "Location", "membership_location": "Count"})
    )

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
if "application_contact_age_category" in df_filt.columns:
    st.markdown("### 🎂 Age Category Breakdown (Filtered)")

    fig_age = px.pie(
        df_filt,
        names="application_contact_age_category",
        title="Age Distribution",
        color_discrete_sequence=px.colors.sequential.Reds
    )
    st.plotly_chart(fig_age, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)

# 3. Hold Duration Histogram
if "hold_duration_days" in df_filt.columns:
    st.markdown("### ⏳ Hold Duration Distribution (Days)")

    fig_hold = px.histogram(
        df_filt,
        x="hold_duration_days",
        nbins=30,
        title="Distribution of Hold Duration (Days)",
        color_discrete_sequence=["#8b0000"]
    )
    st.plotly_chart(fig_hold, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)

# 4. Membership Fee Distribution
if "membership_fee" in df_filt.columns:
    st.markdown("### 💳 Membership Fee Distribution")

    fig_fee = px.box(
        df_filt,
        y="membership_fee",
        title="Membership Fee Distribution (Box Plot)",
        points="outliers"
    )
    st.plotly_chart(fig_fee, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)

# 5. Fee Loss by Location
if "fee_loss" in df_filt.columns and "membership_location" in df_filt.columns:
    st.markdown("### 💰 Total Fee Loss by Location")

    fee_loc = (
        df_filt.groupby("membership_location")["fee_loss"]
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

# 6. Hold Reason vs Age Group
if "reason_for_hold" in df_filt.columns and "application_contact_age_category" in df_filt.columns:
    st.markdown("### 🧠 Hold Reason by Age Group (Filtered)")

    reason_age = (
        df_filt.groupby(["reason_for_hold", "application_contact_age_category"])
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
            "application_contact_age_category": "Age Category"
        }
    )
    fig_reason_age.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_reason_age, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)

# 7. Fee Loss vs Hold Duration Scatter
if "fee_loss" in df_filt.columns and "hold_duration_days" in df_filt.columns:
    st.markdown("### 📈 Fee Loss vs Hold Duration (Filtered)")

    if cluster_col is not None and cluster_col in df_filt.columns:
        fig_scatter = px.scatter(
            df_filt,
            x="hold_duration_days",
            y="fee_loss",
            color=cluster_col,
            title="Fee Loss vs Hold Duration (Colored by Cluster)",
            labels={"hold_duration_days": "Hold Duration (Days)", "fee_loss": "Fee Loss"},
            opacity=0.7
        )
    else:
        fig_scatter = px.scatter(
            df_filt,
            x="hold_duration_days",
            y="fee_loss",
            title="Fee Loss vs Hold Duration",
            labels={"hold_duration_days": "Hold Duration (Days)", "fee_loss": "Fee Loss"},
            opacity=0.7
        )

    st.plotly_chart(fig_scatter, use_container_width=True)
