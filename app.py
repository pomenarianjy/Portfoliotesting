import streamlit as st
import numpy as np
import pandas as pd
import datetime

# Strict live data feed environment tracking engine
try:
    import yfinance as yf
except ModuleNotFoundError:
    st.error("🔧 ENVIRONMENT ERROR: Add 'yfinance' to your requirements.txt file.")
    st.stop()

# 1. CORE VISUAL WINDOW SETUP
st.set_page_config(layout="wide", page_title="Jasmine's Live Portfolio Panel")

# 2. SEED METADATA REGISTRATION TERMINAL (ALL 48 GLOBAL TECHNOLOGY STOCKS)
@st.cache_data
def get_full_global_matrix():
    tickers = [
        "NVDA", "MSFT", "AAPL", "GOOGL", "AMZN", "META", "TSLA", # Magnificent Seven
        "AMD", "MU", "AVGO", "AMAT", "INTC", "KLAC", "LRCX", "TXN", "MRVL", "QCOM", "MPWR", "NXPI", "ADI", # SOXX Top 15
        "TSM", "UMC", "5347.TW", "2454.TW", "3034.TW", "2379.TW", "3661.TW", "ASX", # Taiwan
        "8035.T", "6857.T", "6146.T", "6920.T", "7735.T", "6525.T", "285A.T", "6723.T", "4062.T", "6963.T", # Japan
        "005930.KS", "000660.KS", # South Korea
        "ASML", "IFX", # Europe
        "0981.HK", "1347.HK", "1385.HK", "2577.HK", "6082.HK", "9903.HK" # HKEX / China nodes
    ]
    
    names = [
        "Nvidia Corp.", "Microsoft Corp.", "Apple Inc.", "Alphabet Inc.", "Amazon.com Inc.", "Meta Platforms", "Tesla Inc.",
        "Advanced Micro Devices", "Micron Technology", "Broadcom Inc.", "Applied Materials", "Intel Corp.", "KLA Corporation", "Lam Research Corp.", "Texas Instruments", "Marvell Technology", "Qualcomm Inc.", "Monolithic Power", "NXP Semiconductors", "Analog Devices",
        "TSMC", "United Microelectronics", "Vanguard International", "MediaTek Inc.", "Novatek Micro", "Realtek Semiconductor", "Alchip Technologies", "ASE Technology",
        "Tokyo Electron", "Advantest Corp.", "Disco Corp.", "Lasertec Corp.", "SCREEN Holdings", "Kokusai Electric", "Kioxia Holdings", "Renesas Electronics", "Ibiden Co.", "ROHM Co.",
        "Samsung Electronics", "SK Hynix",
        "ASML Holding N.V.", "Infineon Technologies",
        "SMIC", "Hua Hong Semi", "Shanghai Fudan Micro", "InnoScience Tech", "Shanghai Biren Tech", "Shanghai Iluvatar"
    ]
    
    categories = [
        "Magnificent Seven", "Magnificent Seven", "Magnificent Seven", "Magnificent Seven", "Magnificent Seven", "Magnificent Seven", "Magnificent Seven",
        "SOXX Top 15 Holdings", "SOXX Top 15 Holdings", "SOXX Top 15 Holdings", "SOXX Top 15 Holdings", "SOXX Top 15 Holdings", "SOXX Top 15 Holdings", "SOXX Top 15 Holdings", "SOXX Top 15 Holdings", "SOXX Top 15 Holdings", "SOXX Top 15 Holdings", "SOXX Top 15 Holdings", "SOXX Top 15 Holdings", "SOXX Top 15 Holdings",
        "Taiwan", "Taiwan", "Taiwan", "Taiwan", "Taiwan", "Taiwan", "Taiwan", "Taiwan",
        "Japan", "Japan", "Japan", "Japan", "Japan", "Japan", "Japan", "Japan", "Japan", "Japan",
        "South Korea", "South Korea",
        "Europe", "Europe",
        "HKEX / China Nodes", "HKEX / China Nodes", "HKEX / China Nodes", "HKEX / China Nodes", "HKEX / China Nodes", "HKEX / China Nodes"
    ]
    
    def_prices = [
        135.50, 420.10, 225.40, 175.60, 185.30, 495.20, 210.50,
        154.40, 94.50, 164.80, 192.40, 28.10, 685.20, 842.50, 178.60, 68.20, 168.20, 720.40, 265.22, 210.50,
        178.20, 7.80, 112.50, 1240.00, 510.00, 485.00, 2450.00, 14.50,
        24500.00, 5800.00, 41200.00, 22400.00, 9800.00, 3100.00, 2850.00, 2450.00, 4800.00, 1850.00,
        68500.00, 165000.00,
        820.10, 34.20,
        22.40, 18.50, 14.20, 8.50, 12.10, 9.40
    ]
    
    def_returns = [
        0.452, 0.245, 0.221, 0.195, 0.212, 0.228, 0.384,
        0.315, 0.198, 0.294, 0.264, 0.012, 0.256, 0.284, 0.142, 0.201, 0.185, 0.312, 0.161, 0.164,
        0.261, 0.114, 0.095, 0.184, 0.141, 0.162, 0.412, 0.124,
        0.231, 0.252, 0.342, 0.485, 0.221, 0.165, 0.112, 0.154, 0.132, 0.084,
        0.112, 0.214,
        0.225, 0.145,
        0.125, 0.091, 0.154, 0.050, 0.060, 0.045
    ]
    
    def_vols = [
        0.44, 0.22, 0.20, 0.24, 0.28, 0.36, 0.52,
        0.42, 0.49, 0.27, 0.34, 0.39, 0.31, 0.37, 0.23, 0.41, 0.35, 0.33, 0.26, 0.25,
        0.33, 0.36, 0.32, 0.38, 0.30, 0.34, 0.55, 0.29,
        0.36, 0.39, 0.41, 0.48, 0.38, 0.35, 0.43, 0.32, 0.33, 0.29,
        0.31, 0.42,
        0.28, 0.33,
        0.45, 0.41, 0.48, 0.50, 0.55, 0.58
    ]
    
    matrix = []
    for i in range(len(tickers)):
        matrix.append({
            "ticker": tickers[i],
            "name": names[i],
            "category": categories[i],
            "def_price": def_prices[i],
            "def_r": def_returns[i],
            "def_v": def_vols[i],
            "currency": "USD" if i < 22 or i == 27 or i >= 40 and i <= 41 else ("TWD" if i <= 26 else ("JPY" if i <= 37 else "KRW" if i <= 39 else "HKD"))
        })
    return matrix

# Caching engine to isolate download loops from component click events
@st.cache_data(ttl=3600)
def load_live_market_data():
    raw_matrix = get_full_global_matrix()
    enriched_data = []
    for item in raw_matrix:
        ticker_symbol = item["ticker"]
        last_price = item["def_price"]
        ann_10y = item["def_r"]
        vol = item["def_v"]
        
        try:
            # Safe parsing layout handles non-US symbols dynamically without crashing loops
            ticker_clean = ticker_symbol if (".TW" in ticker_symbol or ".T" in ticker_symbol or ".KS" in ticker_symbol or ".HK" in ticker_symbol) else ticker_symbol
            ticker_obj = yf.Ticker(ticker_clean)
            history = ticker_obj.history(period="3d")
            if history is not None and not history.empty:
                last_price = float(history['Close'].iloc[-1])
                info = ticker_obj.info
                if info is not None:
                    fetched_r = info.get('threeYearAverageReturn')
                    fetched_v = info.get('beta')
                    if fetched_r is not None and fetched_r != 0: ann_10y = float(fetched_r)
                    if fetched_v is not None and fetched_v != 0: vol = float(fetched_v) * 0.25
        except Exception:
            pass
            
        enriched_item = item.copy()
        enriched_item.update({"price": last_price, "ann_10y": ann_10y, "vol": vol})
        enriched_data.append(enriched_item)
    return enriched_data

with st.spinner("Streaming full global terminal universe via Yahoo Finance API feeds..."):
    LIVE_DATA = load_live_market_data()

# 3. GLOBAL APPLICATION INTERACTIVE STATE STORE ENGINE
if "focused_key" not in st.session_state:
    st.session_state.focused_key = "NVDA"

if "portfolio_weights" not in st.session_state:
    st.session_state.portfolio_weights = {str(item["ticker"]): 0 for item in LIVE_DATA}

if "checked_tickers" not in st.session_state:
    st.session_state.checked_tickers = {str(item["ticker"]): False for item in LIVE_DATA}

def select_focused_asset(ticker):
    st.session_state.focused_key = ticker

def sync_checkbox_state(ticker, key_str):
    st.session_state.checked_tickers[ticker] = st.session_state[key_str]

# MACRO BUTTON LOGIC: CALCULATE EXACT EQUAL WEIGHTS FOR CHECKED POSITIONS INSTANTLY
def trigger_equal_weight_normalization():
    active_tickers = [t for t, checked in st.session_state.checked_tickers.items() if checked]
    num_active = len(active_tickers)
    
    if num_active > 0:
        base_weight = 100 // num_active
        remainder = 100 % num_active
        
        for t in st.session_state.portfolio_weights.keys():
            if t in active_tickers:
                st.session_state.portfolio_weights[t] = base_weight
            else:
                st.session_state.portfolio_weights[t] = 0
                
        for i in range(remainder):
            st.session_state.portfolio_weights[active_tickers[i]] += 1
    else:
        for t in st.session_state.portfolio_weights.keys():
            st.session_state.portfolio_weights[t] = 0

st.title("📊 JASMINE'S LIVE PORTFOLIO PANEL")

panel_left, panel_right = st.columns([1.3, 1.0], gap="large")

with panel_left:
    st.subheader("📂 Register Matrix")
    
    categories = ["All", "Magnificent Seven", "SOXX Top 15 Holdings", "Taiwan", "Japan", "South Korea", "Europe", "HKEX / China Nodes"]
    selected_cat = st.selectbox("Filter Active Assets Region", options=categories, index=0)
    
    st.button(
        "🎚️ DISTRIBUTE EQUAL WEIGHTS (CHECKED ONLY)", 
        on_click=trigger_equal_weight_normalization, 
        use_container_width=True
    )
    st.write("")

    ch1, ch2, ch3, ch4 = st.columns([0.6, 2.4, 1.2, 1.2])
    ch1.markdown("**TICK**")
    ch2.markdown("**STOCK ASSET LIST**")
    ch3.markdown("**ALLOCATION %**")
    ch4.markdown("**LIVE PRICE**")
    
    for idx, item in enumerate(LIVE_DATA):
        if selected_cat != "All" and item["category"] != selected_cat:
            continue
            
        r1, r2, r3, r4 = st.columns([0.6, 2.4, 1.2, 1.2])
        ticker = str(item["ticker"])
        name = str(item["name"])
        
        cb_key = f"cb_live_{ticker}_{idx}"
        
        is_checked = r1.checkbox(
            "", 
            value=st.session_state.checked_tickers[ticker], 
            key=cb_key, 
            label_visibility="collapsed",
            on_change=sync_checkbox_state,
            args=(ticker, cb_key)
        )
        
        r2.button(f"🔗 {ticker} | {name[:18]}", key=f"lk_live_{ticker}_{idx}", on_click=select_focused_asset, args=(ticker,))
            
        if is_checked:
            old_val = st.session_state.portfolio_weights[ticker]
            initial_val = int(old_val) if old_val > 0 else 0
            new_alloc = r3.number_input("", min_value=0, max_value=100, value=initial_val, step=5, key=f"al_live_{ticker}_{idx}", label_visibility="collapsed")
            st.session_state.portfolio_weights[ticker] = new_alloc
        else:
            st.session_state.portfolio_weights[ticker] = 0
            r3.markdown("<span style='color: #888888;'>MUTED</span>", unsafe_allow_html=True)

