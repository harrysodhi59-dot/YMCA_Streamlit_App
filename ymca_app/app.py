import streamlit as st

# ----------------------------------------------------
# GLOBAL PAGE CONFIGURATION
# ----------------------------------------------------
st.set_page_config(
    page_title="YMCA Hold Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------------------
# GLOBAL STYLING (CSS)
# ----------------------------------------------------
st.markdown("""
<style>

    /* Hide Streamlit menu + footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Main page background */
    .main {
        background-color: #f5f7fa;
    }

    /* Title styling */
    .title {
        font-size: 40px;
        font-weight: 700;
        color: #1a3c6e;
        margin-bottom: -10px;
    }

    /* Subtitle */
    .subtitle {
        font-size: 18px;
        color: #44546A;
        margin-bottom: 30px;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #1a3c6e;
        color: white;
    }
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3 {
        color: white;
    }

    /* Metric card custom */
    .metric-card {
        padding: 18px;
        border-radius: 12px;
        background-color: #ffffff;
        border: 1px solid #e3e6eb;
        text-align: center;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }

    /* Footer */
    .footer-text {
        text-align: center;
        padding: 20px;
        font-size: 13px;
        color: #8a8a8a;
        margin-top: 40px;
    }

</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# MAIN HEADER (HOME PAGE DISPLAY)
# ----------------------------------------------------

st.markdown("<div class='title'>YMCA Hold Analytics Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Advanced insights on membership holds, clusters, demographics, and revenue risk.</div>", unsafe_allow_html=True)

st.markdown("---")

# ----------------------------------------------------
# HOME PAGE CONTENT
# ----------------------------------------------------
st.markdown("### 📌 Welcome to the YMCA Analytics Platform")

st.write(
    """
This dashboard provides interactive insights into YMCA membership hold patterns, 
cluster behaviors, demographics, fee loss, and operational metrics.

Use the **left sidebar** to navigate through:
- **📄 Data Overview**  
- **📊 Insights Summary**  
- **🔍 Cluster Explorer**  
- **📊 Cluster Comparison Dashboard** (optional)  
- **⏳ Hold Duration Analysis** (optional)  
- **📈 Trends & Forecasts** (optional)

The system reads the cleaned and clustered dataset directly from Excel and updates all visualizations automatically.
"""
)

# ----------------------------------------------------
# OPTIONAL: Add quick KPI cards on Home Page
# (You can enable this once df loading is added here)
# ----------------------------------------------------
st.markdown("### 🚀 Start by selecting a page from the sidebar")

st.markdown("---")

# ----------------------------------------------------
# FOOTER
# ----------------------------------------------------
st.markdown(
    """
    <div class="footer-text">
        Built by Team CMPT 3830 • YMCA Holdings Analytics • 2025
    </div>
    """,
    unsafe_allow_html=True,
)
