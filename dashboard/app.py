import os

import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="TRADEXBOT Dashboard", layout="wide")
st.title("TRADEXBOT Control Panel")

st.write("Configure timeframe, strategy, live-trading mode, and run manual scans.")

left, right = st.columns(2)

with left:
    timeframe = st.selectbox("Timeframe", ["5m", "15m", "1h"], index=0)
    strategy = st.selectbox("Strategy", ["breakout_v1", "trend_follow_v1", "mean_reversion_v1"], index=0)
    symbols_raw = st.text_input("Symbols (comma separated)", value="BTCUSDT,ETHUSDT")

with right:
    live_trading = st.toggle("Enable Live Trading", value=False)
    news_filter = st.toggle("Enable Economic News Filter", value=True)

if st.button("Save Config"):
    payload = {
        "timeframe": timeframe,
        "strategy": strategy,
        "live_trading_enabled": live_trading,
        "news_filter_enabled": news_filter,
        "symbols": [symbol.strip() for symbol in symbols_raw.split(",") if symbol.strip()],
    }
    response = requests.post(f"{BACKEND_URL}/config", json=payload, timeout=10)
    if response.ok:
        st.success("Configuration updated")
    else:
        st.error(f"Failed to update config: {response.text}")

if st.button("Run Scan"):
    response = requests.post(f"{BACKEND_URL}/scan", timeout=30)
    if response.ok:
        data = response.json()
        st.subheader("Economic Events")
        st.json(data.get("economic_events", []))
        st.subheader("Signals")
        st.json(data.get("signals", []))
    else:
        st.error(f"Scan failed: {response.text}")

st.divider()
st.subheader("Service Health")

try:
    health = requests.get(f"{BACKEND_URL}/health", timeout=10).json()
    st.success(f"Backend status: {health.get('status', 'unknown')}")
except requests.RequestException as exc:
    st.error(f"Backend unavailable: {exc}")
