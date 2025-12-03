import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.markdown(
    "<h1 style='color:#8b0000;'>📉 Revenue Impact Simulator</h1>",
    unsafe_allow_html=True
)

st.write("Use the controls below to explore how member hold behavior affects YMCA revenue.")


# ==========================
# SECTION 1 — SIMPLE SLIDER
# ==========================
st.markdown("## 🎚 Adjustable Threshold Slider")

hold_threshold = st.slider(
    "Select Hold Duration Threshold (Days)",
    min_value=0,
    max_value=200,
    value=30
)

st.success(f"Current Threshold: **{hold_threshold} days**")


# ==========================
# SECTION 2 — CIRCULAR GAUGE METER
# ==========================
st.markdown("## 🧭 Revenue Risk Gauge Meter")

risk_value = st.slider(
    "Adjust Revenue Risk Level",
    min_value=0,
    max_value=100,
    value=50
)

gauge = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=risk_value,
        title={"text": "Revenue Risk Level"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "red"},
            "steps": [
                {"range": [0, 30], "color": "#ffe5e5"},
                {"range": [30, 70], "color": "#ffb3b3"},
                {"range": [70, 100], "color": "#ff7b7b"}
            ],
        }
    )
)

st.plotly_chart(gauge, use_container_width=True)


# ==========================
# SECTION 3 — MOVING DOT ON LINE GRAPH
# ==========================
st.markdown("## 🔴 Moving Impact Dot (Interactive Curve)")

# Create base curve (simulated revenue impact curve)
x = np.linspace(0, 200, 200)
y = np.exp(-x / 80) * 100  # drops as hold duration increases

dot_x = st.slider(
    "Move Dot Along Curve (Hold Duration)",
    min_value=0,
    max_value=200,
    value=50
)

dot_y = float(np.exp(-dot_x / 80) * 100)

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name="Revenue Retention Curve"))
fig.add_trace(go.Scatter(
    x=[dot_x],
    y=[dot_y],
    mode="markers",
    marker=dict(size=14, color="red"),
    name="Selected Point"
))

fig.update_layout(
    title="Revenue Retention vs Hold Duration",
    xaxis_title="Hold Duration (Days)",
    yaxis_title="Revenue Retained (%)"
)

st.plotly_chart(fig, use_container_width=True)

st.info(
    f"📌 Revenue retained at **{dot_x} days hold** ≈ **{dot_y:.2f}%**"
)
