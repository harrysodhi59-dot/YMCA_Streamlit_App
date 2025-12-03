import streamlit as st
from PIL import Image
from io import BytesIO
import requests

# ==========================
# PAGE CONFIGURATION
# ==========================
st.set_page_config(
    page_title="Data Alchemists Analytics Platform",
    layout="wide"
)

# ==========================
# LOAD YMCA LOGO FROM URL
# ==========================
logo_url = "https://lethbridgeymca.ca/wp-content/uploads/2020/08/YMCA-Logo.png"

try:
    response = requests.get(logo_url)
    logo = Image.open(BytesIO(response.content))
except:
    logo = None


# ==========================
# CUSTOM STYLES (LIGHT RED SIDEBAR)
# ==========================
st.markdown(
    """
    <style>
        /* Sidebar background */
        [data-testid="stSidebar"] {
            background-color: #ffe0e0 !important;
        }

        /* Sidebar title styling */
        .sidebar-title {
            font-size: 26px;
            font-weight: 700;
            color: #8b0000;
            text-align: center;
            margin-bottom: 15px;
        }

        /* Horizontal divider */
        .styled-hr {
            border: 1px solid #aa0000;
            margin-top: 10px;
            margin-bottom: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# ==========================
# SIDEBAR LAYOUT
# ==========================
with st.sidebar:

    # Dashboard name
    st.markdown("<div class='sidebar-title'>Data Alchemists</div>", unsafe_allow_html=True)

    # YMCA logo
    if logo:
        st.image(logo, use_column_width=True)
    else:
        st.warning("⚠ Unable to load YMCA logo.")

    st.markdown("<hr class='styled-hr'>", unsafe_allow_html=True)

    st.write("Welcome to the Data Alchemists Analytics Platform!")


# ==========================
# MAIN HOMEPAGE CONTENT
# ==========================
st.markdown(
    """
    <h1 style='text-align:center; color:#8b0000;'>
        📊 Data Alchemists Analytics Platform
    </h1>
    """,
    unsafe_allow_html=True
)

# Show logo on homepage
if logo:
    st.image(logo, width=200)

st.markdown(
    """
    <p style='font-size:18px; text-align:center; color:#444;'>
        Turning raw YMCA data into actionable financial insights.
    </p>
    """,
    unsafe_allow_html=True
)
