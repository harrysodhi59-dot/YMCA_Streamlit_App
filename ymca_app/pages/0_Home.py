import streamlit as st
from pathlib import Path

# ======================
#  PAGE CONFIG
# ======================
st.set_page_config(
    page_title="Data Alchemists Analytics Platform",
    layout="wide",
)

# ======================
#  CUSTOM STYLING
# ======================
st.markdown(
    """
    <style>
        /* Main Background */
        .main {
            background-color: #ffe0e0;
        }

        /* Title Styling */
        .title {
            font-size: 42px;
            font-weight: 800;
            color: #8b0000;
            text-align: center;
            margin-top: -20px;
        }

        .subtitle {
            font-size: 22px;
            font-weight: 500;
            color: #a30000;
            text-align: center;
        }

        /* Card Styling */
        .card {
            background-color: #ffd6d6;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }

        .card-title {
            font-size: 22px;
            color: #7a0000;
            font-weight: 700;
        }

        .card-text {
            font-size: 16px;
            color: #4a0000;
            line-height: 1.5;
        }

        footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

# ======================
#  CONTENT
# ======================

st.markdown("<div class='title'>📊 Data Alchemists Analytics Platform</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Transforming raw YMCA member data into actionable business insights</div>", unsafe_allow_html=True)
st.write("")

# ------ SECTION 1: ABOUT ------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='card-title'>🔍 What This Platform Does</div>", unsafe_allow_html=True)
st.markdown(
    """
    <div class='card-text'>
        The Data Alchemists Analytics Platform is designed to help the YMCA understand  
        **member hold behaviour**, its financial impact, and hidden usage patterns  
        using clustering, dashboards, and automated insights.
        <br><br>
        Our mission is to support **data-driven decision-making** that improves  
        retention, financial sustainability, and member engagement.
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("</div>", unsafe_allow_html=True)

# ------ SECTION 2: PROJECT OBJECTIVE ------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='card-title'>🎯 Core Objective</div>", unsafe_allow_html=True)
st.markdown(
    """
    <div class='card-text'>
        <b>Revenue Impact Analysis of Hold Behavior</b>
        <ul>
            <li>Quantify how hold frequency and duration affect YMCA annual revenue.</li>
            <li>Identify clusters of members: <b>frequent holders</b>, <b>seasonal holders</b>, and <b>stable members</b>.</li>
            <li>Estimate member-level revenue loss using financial modeling.</li>
            <li>Support policy adjustments that balance member needs with YMCA sustainability.</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("</div>", unsafe_allow_html=True)

# ------ SECTION 3: FEATURES ------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='card-title'>🧩 Key Features of This Dashboard</div>", unsafe_allow_html=True)
st.markdown(
    """
    <div class='card-text'>
        ✔ Interactive data filtering and exploration<br>
        ✔ Automated cluster detection and visualization<br>
        ✔ Financial loss calculations<br>
        ✔ Behaviour pattern insights for each YMCA location<br>
        ✔ Clean, professional data analyst interface
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("</div>", unsafe_allow_html=True)

# ------ SECTION 4: TEAM ------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='card-title'>🤝 Created By</div>", unsafe_allow_html=True)
st.markdown(
    """
    <div class='card-text'>
        <b>Team: Data Alchemists</b><br>
        Harnessing data science, machine learning, and business analytics  
        to deliver high-value insights for community organizations.
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("</div>", unsafe_allow_html=True)
