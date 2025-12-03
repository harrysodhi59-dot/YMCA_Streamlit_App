import streamlit as st

st.set_page_config(
    page_title="YMCA Hold Analytics",
    page_icon="📊",
    layout="wide"
)

# Global styling
st.markdown("""
    <style>
        .big-font {
            font-size:22px !important;
            font-weight:600 !important;
        }
        .metric-card {
            padding: 15px;
            border-radius: 10px;
            background-color: #f7f7f9;
            border: 1px solid #e0e0e0;
            margin-bottom: 15px;
        }
        .center-text {
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

import streamlit as st
import pandas as pd

st.set_page_config(page_title="YMCA Membership Dashboard", layout="wide")

st.title("🏊 YMCA Membership Dashboard")

st.write("""
Welcome!  
This dashboard is built as part of the CMPT 3830 YMCA project.

You can explore membership behavior, clusters, trends and insights using the sidebar navigation.
""")
