import streamlit as st

# ----------------------------------------------------
# GLOBAL PAGE CONFIGURATION
# ----------------------------------------------------
st.set_page_config(
    page_title="Data Alchemists Analytics Platform",
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

    /* Page background */
    .main {
        background-color: #f5f7fa;
    }

    /* Main Title */
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

    /* Team line */
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
# HEADER (MAIN TITLE SECTION)
# ----------------------------------------------------
st.markdown(
    "<div class='title'>Data Alchemists Analytics Platform</div>",
    unsafe_allow_html=True,
)

st.markdown(
    "<div class='subtitle'>Advanced analytics on YMCA hold behavior, revenue impact, and member value.</div>",
    unsafe_allow_html=True,
)

st.markdown(
    "<div class='teamline'>Created by <b>Data Alchemists</b> • CMPT 3830 Machine Learning Work Integrated Project</div>",
    unsafe_allow_html=True,
)

st.markdown("---")

# ----------------------------------------------------
# EXECUTIVE SUMMARY / HOME CONTENT
# ----------------------------------------------------

left, right = st.columns([2, 1])

with left:
    st.markdown("### 🧭 Project Problem Focus")
    st.write(
        """
We analyse YMCA membership **hold behaviour** to answer key strategic questions:

1. **How do hold frequency and duration impact YMCA revenue and cash flow?**  
2. **Which behavioral segments (clusters) produce the highest financial risk?**  
3. **What policy recommendations can reduce revenue leakage while staying member-friendly?**

Navigate using the sidebar to explore:
- **📂 Data Foundation & Quality Check**  
- **📊 Revenue & Hold Behaviour Insights**  
- **🧩 Behaviour Segmentation Explorer**  
- Future Add-Ons:  
  - 💰 Revenue Impact Modeling  
  - ⚖️ Policy Scenario Simulator  
  - 🔮 Predictive Churn Analysis  
        """
    )

with right:
    st.markdown("### 📌 How to Use This Platform")
    st.write(
        """
- Start with **Data Foundation** to understand the dataset.  
- Explore **Revenue Insights** for financial impact.  
- Use **Segmentation Explorer** to deep-dive into member groups.  
- Apply insights for **policy, strategy, and operations decisions**.
        """
    )

st.markdown("---")

# ----------------------------------------------------
# FOOTER
# ----------------------------------------------------
st.markdown(
    """
    <div class="footer-text">
        Data Alchemists • YMCA Hold Analytics Platform • 2025
    </div>
    """,
    unsafe_allow_html=True,
)
