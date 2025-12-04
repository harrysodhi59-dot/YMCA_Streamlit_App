from PIL import Image
import os

logo_path = os.path.join(os.path.dirname(__file__), "assets", "ymca_logo.png")

try:
    logo = Image.open(logo_path)
    st.sidebar.image(logo, use_column_width=True)
except:
    st.sidebar.write("")  # no crash if missing

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
# SIDEBAR BRANDING (Header inside sidebar)
# ----------------------------------------------------
with st.sidebar:
    st.markdown("""
        <h2 style='font-weight:700; margin-bottom:0px; color:#4A0000;'>
            Data Alchemists<br>Analytics Platform
        </h2>
        <p style='font-size:14px; margin-top:2px; margin-bottom:5px; color:#4A0000;'>
            YMCA Revenue Intelligence Dashboard
        </p>
        <hr style='margin:10px 0 20px 0; border-color:#FFBABA;'>
    """, unsafe_allow_html=True)

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

    /* ------------------------------------------------------ */
    /* LIGHT RED SIDEBAR THEME                                */
    /* ------------------------------------------------------ */

    section[data-testid="stSidebar"] {
        background-color: #FFD6D6 !important;   /* soft light red */
        color: #4A0000 !important;              /* dark red text */
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label {
        color: #4A0000 !important;
    }

    section[data-testid="stSidebar"] hr {
        border-color: #FFBABA !important;       /* soft pink divider */
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
We analyze YMCA membership **hold behavior** to answer three strategic questions:

1. **How do hold frequency and duration impact YMCA revenue and cash flow?**  
2. **Which behavior clusters create the highest financial risk?**  
3. **What policy recommendations reduce revenue leakage while maintaining fairness?**

Use the sidebar to explore:

- 📂 Data Foundation & Quality Check  
- 📊 Revenue & Hold Behaviour Insights  
- 🧩 Behaviour Segmentation Explorer  

(Upcoming advanced modules)  
- 💰 Revenue Impact Modeling  
- ⚖️ Policy Scenario Simulator  
- 🔮 Predictive Churn Analysis  
        """
    )

with right:
    st.markdown("### 📌 How to Use This Platform")
    st.write(
        """
- Start with **Data Foundation**  
- Move to **Revenue Insights**  
- Explore **Segmentation Explorer**  
- Use insights for policy + decision-making  
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
