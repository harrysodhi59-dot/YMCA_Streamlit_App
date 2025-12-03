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


# ==========================
# DETECT CLUSTER COLUMN
# ==========================
cluster_col = None
for c in df.columns:
    if "cluster_label" in c.lower() or "cluster" in c.lower():
        cluster_col = c
        break


# ==========================
# 🔍 COLUMN EXPLORER
# ==========================
st.markdown("### 🧠 Explore Any Column")

column_choice = st.selectbox("Choose a column to inspect:", df.columns)
col_data = df[column_choice]

with st.expander("Column Summary", expanded=True):
    st.write(f"**Data Type:** {col_data.dtype}")
    st.write(f"**Unique Values:** {col_data.nunique()}")
    st.write(f"**Missing Values:** {col_data.isnull().sum()}")
    st.write("**Example Values:**")
    st.write(col_data.dropna().unique()[:10])

    # Auto visualization
    if col_data.dtype == "object":
        cat_df = col_data.fillna("Unknown").astype(str).value_counts().reset_index()
        cat_df.columns = ["Category", "Count"]

        fig_auto = px.bar(
            cat_df,
            x="Category",
            y="Count",
            title=f"Distribution of {column_choice}",
            color_discrete_sequence=["#8B0000"]
        )
        fig_auto.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_auto, use_container_width=True)

    else:
        fig_auto = px.histogram(
            df,
            x=column_choice,
            nbins=30,
            title=f"Distribution of {column_choice}",
            color_discrete_sequence=["#8B0000"]
        )
        st.plotly_chart(fig_auto, use_container_width=True)


st.markdown("<hr>", unsafe_allow_html=True)


# ==========================
# DATA DICTIONARY
# ==========================
st.markdown("### 📑 Data Dictionary")

schema = pd.DataFrame({
    "Column": df.columns,
    "Datatype": df.dtypes.astype(str),
    "Non-Null Count": df.notnull().sum().values,
    "Missing Count": df.isnull().sum().values,
    "Missing %": (df.isnull().sum().values / len(df) * 100).round(2),
    "Unique Values": [df[col].nunique() for col in df.columns],
    "Example Value": [df[col].dropna().iloc[0] if df[col].notna().any() else "" for col in df.columns]
})

search_term = st.text_input("🔎 Search column name (optional):")
if search_term.strip():
    schema_filtered = schema[schema["Column"].str.contains(search_term.strip(), case=False)]
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

    loc_sel = f1.multiselect(
        "Membership Location",
        sorted(df["membership_location"].dropna().unique().tolist()),
        default=sorted(df["membership_location"].dropna().unique().tolist())
    )

    pkg_sel = f2.multiselect(
        "Package Category",
        sorted(df["application_package_category"].dropna().unique().tolist()),
        default=sorted(df["application_package_category"].dropna().unique().tolist())
    )

    mtype_sel = f3.multiselect(
        "Membership Type",
        sorted(df["application_subscription_membership_type"].dropna().unique().tolist()),
        default=sorted(df["application_subscription_membership_type"].dropna().unique().tolist())
    )

    age_sel = f4.multiselect(
        "Age Category",
        sorted(df["application_contact_age_category"].dropna().unique().tolist()),
        default=sorted(df["application_contact_age_category"].dropna().unique().tolist())
    )

    reason_sel = f5.multiselect(
        "Reason for Hold",
        sorted(df["reason_for_hold"].dropna().unique().tolist()),
        default=sorted(df["reason_for_hold"].dropna().unique().tolist())
    )

    if cluster_col:
        cluster_sel = f6.multiselect(
            "Cluster",
            sorted(df[cluster_col].dropna().unique().tolist()),
            default=sorted(df[cluster_col].dropna().unique().tolist())
        )
    else:
        cluster_sel = None


# ==========================
# APPLY FILTERS
# ==========================
df_filt = df.copy()

df_filt = df_filt[df_filt["membership_location"].isin(loc_sel)]
df_filt = df_filt[df_filt["application_package_category"].isin(pkg_sel)]
df_filt = df_filt[df_filt["application_subscription_membership_type"].isin(mtype_sel)]
df_filt = df_filt[df_filt["application_contact_age_category"].isin(age_sel)]
df_filt = df_filt[df_filt["reason_for_hold"].isin(reason_sel)]

if cluster_sel is not None and cluster_col is not None:
    df_filt = df_filt[df_filt[cluster_col].isin(cluster_sel)]

st.write(f"📌 Showing **{len(df_filt):,}** records after filters.")
st.markdown("<hr>", unsafe_allow_html=True)


# ==========================
# KPI CARDS
# ==========================
st.markdown("### 🔢 Key Metrics (Filtered Subset)")

k1, k2, k3, k4 = st.columns(4)

k1.metric("Total Records", f"{len(df_filt):,}")
k2.metric("Unique Locations", df_filt["membership_location"].nunique())
k3.metric("Total Fee Loss", f"${df_filt['fee_loss'].sum():,.0f}")
k4.metric("Avg Hold Duration", f"{df_filt['hold_duration_days'].mean():.1f} days")

st.markdown("<hr>", unsafe_allow_html=True)


# ==========================
# SAMPLE DATA
# ==========================
st.markdown("### 🧾 Sample Data Preview (Filtered)")
st.dataframe(df_filt.head(20), use_container_width=True)
st.markdown("<hr>", unsafe_allow_html=True)


# ==========================
# FIXED LOCATION BAR CHART
# ==========================
st.markdown("### 🏢 Members by Location (Filtered)")

loc_series = df_filt["membership_location"].fillna("Unknown").astype(str)

loc_counts = (
    loc_series.value_counts()
    .reset_index()
)

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


# ==========================
# AGE CATEGORY PIE
# ==========================
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


# ==========================
# HOLD DURATION HISTOGRAM
# ==========================
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


# ==========================
# MEMBERSHIP FEE BOXPLOT
# ==========================
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
