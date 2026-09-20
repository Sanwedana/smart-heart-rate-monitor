import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Smart Heart Monitor",
    page_icon="❤️",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    .main {
        background-color: #f7f9fc;
    }

    /* Main title */
    .title {
        font-size: 36px;
        font-weight: 700;
        margin-bottom: 5px;
        color: #f9fafb;
    }

    /* Subtitle */
    .subtitle {
        color: #94a3b8;
        font-size: 17px;
        margin-bottom: 25px;
    }

    /* KPI Cards */
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        text-align: center;
    }

    .card-title {
        color: #4b5563 !important;
        font-size: 14px;
        font-weight: 600;
    }

    .card-value {
        font-size: 34px;
        font-weight: 700;
        margin-top: 5px;
        color: #111827 !important;
    }

    .card div {
        color: #374151;
    }

    /* Statistics / Status cards */
    .status {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        color: #111827;
        line-height: 1.5;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# SIMULATED SENSOR DATA
# =========================================================

np.random.seed(42)

num_readings = 60

times = [
    datetime.now() - timedelta(seconds=(num_readings - i) * 15)
    for i in range(num_readings)
]

# Simulated heart-rate readings
bpm = np.random.normal(78, 5, num_readings)

# Keep simulated BPM within a reasonable range
bpm = np.clip(bpm, 65, 95).round().astype(int)

df = pd.DataFrame({
    "Time": times,
    "BPM": bpm
})

# 5-reading moving average
df["Moving Average"] = df["BPM"].rolling(5).mean()


# =========================================================
# CALCULATIONS
# =========================================================

current_bpm = int(df["BPM"].iloc[-1])
average_bpm = int(df["BPM"].mean())
maximum_bpm = int(df["BPM"].max())
minimum_bpm = int(df["BPM"].min())


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="title">❤️ Smart Heart Monitor</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'IoT-Based Heart Rate Monitoring & Data Analytics Dashboard'
    '</div>',
    unsafe_allow_html=True
)

st.info(
    "🟡 DEMO MODE — Currently displaying simulated MAX30102 data"
)


# =========================================================
# KPI CARDS
# =========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.markdown(f"""
    <div class="card">
        <div class="card-title">CURRENT BPM</div>
        <div class="card-value">{current_bpm}</div>
        <div>BPM</div>
    </div>
    """, unsafe_allow_html=True)


with col2:

    st.markdown(f"""
    <div class="card">
        <div class="card-title">AVERAGE BPM</div>
        <div class="card-value">{average_bpm}</div>
        <div>BPM</div>
    </div>
    """, unsafe_allow_html=True)


with col3:

    st.markdown(f"""
    <div class="card">
        <div class="card-title">MAX BPM</div>
        <div class="card-value">{maximum_bpm}</div>
        <div>BPM</div>
    </div>
    """, unsafe_allow_html=True)


with col4:

    st.markdown(f"""
    <div class="card">
        <div class="card-title">MIN BPM</div>
        <div class="card-value">{minimum_bpm}</div>
        <div>BPM</div>
    </div>
    """, unsafe_allow_html=True)


st.write("")


# =========================================================
# HEART RATE OVER TIME
# =========================================================

st.subheader("📈 Heart Rate Over Time")

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=df["Time"],
        y=df["BPM"],
        mode="lines+markers",
        name="Heart Rate",
        line=dict(width=3)
    )
)

fig.update_layout(
    height=320,
    xaxis_title="Time",
    yaxis_title="Heart Rate (BPM)",
    hovermode="x unified",
    template="plotly_white"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# MOVING AVERAGE / TREND ANALYSIS
# =========================================================

st.subheader("📊 Heart Rate Trend Analysis")

fig2 = go.Figure()

fig2.add_trace(
    go.Scatter(
        x=df["Time"],
        y=df["BPM"],
        mode="lines",
        name="BPM"
    )
)

fig2.add_trace(
    go.Scatter(
        x=df["Time"],
        y=df["Moving Average"],
        mode="lines",
        name="5-Reading Moving Average",
        line=dict(width=4)
    )
)

fig2.update_layout(
    height=300,
    xaxis_title="Time",
    yaxis_title="BPM",
    hovermode="x unified",
    template="plotly_white"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# =========================================================
# SESSION STATISTICS + SYSTEM STATUS
# =========================================================

col1, col2 = st.columns(2)

# -------------------------
# SESSION STATISTICS
# -------------------------

with col1:

    st.subheader("📋 Session Statistics")

    st.markdown(
        f"""
        <div class="status">
        <b>Total Readings:</b> {len(df)}<br><br>
        <b>Average Heart Rate:</b> {average_bpm} BPM<br><br>
        <b>Minimum Heart Rate:</b> {minimum_bpm} BPM<br><br>
        <b>Maximum Heart Rate:</b> {maximum_bpm} BPM<br><br>
        <b>Data Duration:</b> {len(df) * 15 // 60} minutes
        </div>
        """,
        unsafe_allow_html=True
    )


# -------------------------
# SYSTEM STATUS
# -------------------------

with col2:

    st.subheader("🔌 System Status")

    st.markdown(
        """
        <div class="status">
        🟡 <b>Operating Mode:</b> Demo / Simulated Data<br><br>
        🟡 <b>MAX30102:</b> Simulation<br><br>
        🟢 <b>Dashboard:</b> Running<br><br>
        🟡 <b>NodeMCU:</b> Not Connected<br><br>
        🟡 <b>Cloud:</b> Not Connected
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# RAW SENSOR DATA
# =========================================================

st.subheader("🗃️ Sensor Data")

display_df = df.copy()

display_df["Time"] = display_df["Time"].dt.strftime("%H:%M:%S")

display_df["Moving Average"] = display_df[
    "Moving Average"
].round(2)

st.dataframe(
    display_df[
        ["Time", "BPM", "Moving Average"]
    ].tail(15),
    use_container_width=True,
    hide_index=True
)


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "Smart Heart Monitor | IoT + Data Analytics Mini Project | "
    "MAX30102 + NodeMCU ESP8266"
)