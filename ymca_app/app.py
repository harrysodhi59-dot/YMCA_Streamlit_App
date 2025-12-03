import streamlit as st

# ----------------------------------------------------
# GLOBAL PAGE CONFIGURATION
# ----------------------------------------------------
st.set_page_config(
    page_title="YMCA Hold Revenue Impact Dashboard | Data Alchemists",
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
        margin-bottom: -8px;
    }

    /* Subtitle */
    .subtitle {
        font-size: 18px;
        color: #44546A;
        margin-bottom: 6px;
    }

    .teamline {
        font-size: 15px;
        color: #666666;
        margin-bottom: 24px;
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
# HEADER
# ----------------------------------------------------
st.markdown(
    "<div class='title'>YMCA Hold Revenue Impact Dashboard</div>",
    unsafe_allow_html=True,
)

st.markdown(
    "<div class='subtitle'>Quantifying how hold behaviour impacts member Lifetime Value (LTV) and YMCA revenue.</div>",
    unsafe_allow_html=True,
)

st.markdown(
    "<div class='teamline'>Built by <b>Data Alchemists</b> &bull; CMPT 3830 Machine Learning Work Integrated Project</div>",
    unsafe_allow_html=True,
)

st.markdown("---")

# ----------------------------------------------------
# EXECUTIVE SUMMARY / HOME CONTENT
# ----------------------------------------------------
left, right = st.columns([2, 1])

with left:
    st.markdown("### 🧭 Problem Focus: Revenue Impact of Holds")
    st.write(
        """
We analyse **hold behaviour** across YMCA members to answer three key business questions:

1. **How do hold frequency and duration affect revenue and cash flow?**  
2. **Which member segments (clusters) contribute most to fee loss and risk?**  
3. **What kind of hold policies can balance member fairness and financial sustainability?**

Use the pages in the left sidebar to explore:

- **📂 Data Foundation & Quality Check** – cleaned dataset and structure  
- **📊 Revenue & Hold Behaviour Insights** – key KPIs and trends  
- **🧩 Behaviour Segmentation Explorer** – clusters of member hold patterns  
- (Next steps) **💰 Revenue Impact Modeling** & **⚖️ Policy Scenarios**
        """
    )

with right:
    st.markdown("### 📌 How to Use This Dashboard")
    st.write(
        """
- Start with **Data Foundation** to understand the dataset.  
- Move to **Revenue & Hold Behaviour** to see high-level trends.  
- Use **Behaviour Segmentation** to deep–dive into clusters.  
- Share insights with YMCA stakeholders to guide **policy decisions**.
        """
    )

st.markdown("---")

# ----------------------------------------------------
# FOOTER
# ----------------------------------------------------
st.markdown(
    """
    <div class="footer-text">
        Data Alchemists • YMCA Hold Revenue Impact • 2025
    </div>
    """,
    unsafe_allow_html=True,
)
