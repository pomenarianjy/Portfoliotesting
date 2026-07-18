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

# 1. CORE VISUAL WINDOW PROPERTIES
st.set_page_config(layout="wide", page_title="Jasmine's Live Portfolio Panel")

# 2. DEFINITIVE SEED MATRIX (ALL 48 KEY GLOBAL TECHNOLOGY ASSETS RESTORED)
@st.cache_data
def get_definitive_global_universe():
    assets_data = [
        # --- Magnificent Seven ---
        {"ticker": "NVDA", "name": "Nvidia Corp.", "category": "Magnificent Seven", "def_price": 135.50, "def_r": 0.452, "def_v": 0.44, "currency": "USD"},
        {"ticker": "MSFT", "name": "Microsoft Corp.", "category": "Magnificent Seven", "def_price": 420.10, "def_r": 0.245, "def_v": 0.22, "currency": "USD"},
        {"ticker": "AAPL", "name": "Apple Inc.", "category": "Magnificent Seven", "def_price": 225.40, "def_r": 0.221, "def_v": 0.20, "currency": "USD"},
        {"ticker": "GOOGL", "name": "Alphabet Inc.", "category": "Magnificent Seven", "def_price": 175.60, "def_r": 0.195, "def_v": 0.24, "currency": "USD"},
        {"ticker": "AMZN", "name": "Amazon.com Inc.", "category": "Magnificent Seven", "def_price": 185.30, "def_r": 0.212, "def_v": 0.28, "currency": "USD"},
        {"ticker": "META", "name": "Meta Platforms Inc.", "category": "Magnificent Seven", "def_price": 495.20, "def_r": 0.228, "def_v": 0.36, "currency": "USD"},
        {"ticker": "TSLA", "name": "Tesla Inc.", "category": "Magnificent Seven", "def_price": 210.50, "def_r": 0.384, "def_v": 0.52, "currency": "USD"},
        
        # --- SOXX Top 15 Holdings ---
        {"ticker": "AMD", "name": "Advanced Micro Devices", "category": "SOXX Top 15 Holdings", "def_price": 154.40, "def_r": 0.315, "def_v": 0.42, "currency": "USD"},
        {"ticker": "MU", "name": "Micron Technology", "category": "SOXX Top 15 Holdings", "def_price": 94.50, "def_r": 0.198, "def_v": 0.49, "currency": "USD"},
        {"ticker": "AVGO", "name": "Broadcom Inc.", "category": "SOXX Top 15 Holdings", "def_price": 164.80, "def_r": 0.294, "def_v": 0.27, "currency": "USD"},
        {"ticker": "AMAT", "name": "Applied Materials", "category": "SOXX Top 15 Holdings", "def_price": 192.40, "def_r": 0.264, "def_v": 0.34, "currency": "USD"},
        {"ticker": "INTC", "name": "Intel Corp.", "category": "SOXX Top 15 Holdings", "def_price": 28.10, "def_r": 0.012, "def_v": 0.39, "currency": "USD"},
        {"ticker": "KLAC", "name": "KLA Corporation", "category": "SOXX Top 15 Holdings", "def_price": 685.20, "def_r": 0.256, "def_v": 0.31, "currency": "USD"},
        {"ticker": "LRCX", "name": "Lam Research Corp.", "category": "SOXX Top 15 Holdings", "def_price": 842.50, "def_r": 0.284, "def_v": 0.37, "currency": "USD"},
        {"ticker": "TXN", "name": "Texas Instruments", "category": "SOXX Top 15 Holdings", "def_price": 178.60, "def_r": 0.142, "def_v": 0.23, "currency": "USD"},
        {"ticker": "MRVL", "name": "Marvell Technology", "category": "SOXX Top 15 Holdings", "def_price": 68.20, "def_r": 0.201, "def_v": 0.41, "currency": "USD"},
        {"ticker": "QCOM", "name": "Qualcomm Inc.", "category": "SOXX Top 15 Holdings", "def_price": 168.20, "def_r": 0.185, "def_v": 0.35, "currency": "USD"},
        {"ticker": "MPWR", "name": "Monolithic Power", "category": "SOXX Top 15 Holdings", "def_price": 720.40, "def_r": 0.312, "def_v": 0.33, "currency": "USD"},
        {"ticker": "NXPI", "name": "NXP Semiconductors", "category": "SOXX Top 15 Holdings", "def_price": 265.22, "def_r": 0.161, "def_v": 0.26, "currency": "USD"},
        {"ticker": "ADI", "name": "Analog Devices Inc.", "category": "SOXX Top 15 Holdings", "def_price": 210.50, "def_r": 0.164, "def_v": 0.25, "currency": "USD"},
        
        # --- Taiwan ---
        {"ticker": "TSM", "name": "TSMC", "category": "Taiwan", "def_price": 178.20, "def_r": 0.261, "def_v": 0.33, "currency": "USD"},
        {"ticker": "UMC", "name": "United Microelectronics", "category": "Taiwan", "def_price": 7.80, "def_r": 0.114, "def_v": 0.36, "currency": "USD"},
        {"ticker": "5347.TW", "name": "Vanguard International", "category": "Taiwan", "def_price": 112.50, "def_r": 0.095, "def_v": 0.32, "currency": "TWD"},
        {"ticker": "2454.TW", "name": "MediaTek Inc.", "category": "Taiwan", "def_price": 1240.00, "def_r": 0.184, "def_v": 0.38, "currency": "TWD"},
        {"ticker": "3034.TW", "name": "Novatek Micro", "category": "Taiwan", "def_price": 510.00, "def_r": 0.141, "def_v": 0.30, "currency": "TWD"},
        {"ticker": "2379.TW", "name": "Realtek Semiconductor", "category": "Taiwan", "def_price": 485.00, "def_r": 0.162, "def_v": 0.34, "currency": "TWD"},
        {"ticker": "3661.TW", "name": "Alchip Technologies", "category": "Taiwan", "def_price": 2450.00, "def_r": 0.412, "def_v": 0.55, "currency": "TWD"},
        {"ticker": "ASX", "name": "ASE Technology Holding", "category": "Taiwan", "def_price": 14.50, "def_r": 0.124, "def_v": 0.29, "currency": "USD"},
        
        # --- Japan ---
        {"ticker": "8035.T", "name": "Tokyo Electron", "category": "Japan", "def_price": 24500.00, "def_r": 0.231, "def_v": 0.36, "currency": "JPY"},
        {"ticker": "6857.T", "name": "Advantest Corp.", "category": "Japan", "def_price": 5800.00, "def_r": 0.252, "def_v": 0.39, "currency": "JPY"},
        {"ticker": "6146.T", "name": "Disco Corp.", "category": "Japan", "def_price": 41200.00, "def_r": 0.342, "def_v": 0.41, "currency": "JPY"},
        {"ticker": "6920.T", "name": "Lasertec Corp.", "category": "Japan", "def_price": 22400.00, "def_r": 0.485, "def_v": 0.48, "currency": "JPY"},
        {"ticker": "7735.T", "name": "SCREEN Holdings", "category": "Japan", "def_price": 9800.00, "def_r": 0.221, "def_v": 0.38, "currency": "JPY"},
        {"ticker": "6525.T", "name": "Kokusai Electric", "category": "Japan", "def_price": 3100.00, "def_r": 0.165, "def_v": 0.35, "currency": "JPY"},
        {"ticker": "285A.T", "name": "Kioxia Holdings", "category": "Japan", "def_price": 2850.00, "def_r": 0.112, "def_v": 0.43, "currency": "JPY"},
        {"ticker": "6723.T", "name": "Renesas Electronics", "category": "Japan", "def_price": 2450.00, "def_r": 0.154, "def_v": 0.32, "currency": "JPY"},
        {"ticker": "4062.T", "name": "Ibiden Co.", "category": "Japan", "def_price": 4800.00, "def_r": 0.132, "def_v": 0.33, "currency": "JPY"},
        {"ticker": "6963.T", "name": "ROHM Co.", "category": "Japan", "def_price": 1850.00, "def_r": 0.084, "def_v": 0.29, "currency": "JPY"},
        
        # --- South Korea ---
        {"ticker": "005930.KS", "name": "Samsung Electronics", "category": "South Korea", "def_price": 68500.00, "def_r": 0.112, "def_v": 0.31, "currency": "KRW"},
        {"ticker": "000660.KS", "name": "SK Hynix", "category": "South Korea", "def_price": 165000.00, "def_r": 0.214, "def_v": 0.42, "currency": "KRW"},
        
        # --- Europe ---
        {"ticker": "ASML", "name": "ASML Holding N.V.", "category": "Europe", "def_price": 820.10, "def_r": 0.225, "def_v": 0.28, "currency": "USD"},
        {"ticker": "IFX", "name": "Infineon Technologies", "category": "Europe", "def_price": 34.20, "def_r": 0.145, "def_v": 0.33, "currency": "EUR"},
        
        # --- HKEX / China Nodes ---
        {"ticker": "0981.HK", "name": "SMIC", "category": "HKEX / China Nodes", "def_price": 22.40, "def_r": 0.125, "def_v": 0.45, "currency": "HKD"},
        {"ticker": "1347.HK", "name": "Hua Hong Semi", "category": "HKEX / China Nodes", "def_price": 18.50, "def_r": 0.091, "def_v": 0.41, "currency": "HKD"},
        {"ticker": "1385.HK", "name": "Shanghai Fudan Micro", "category": "HKEX / China Nodes", "def_price": 14.20, "def_r": 0.154, "def_v": 0.48, "currency": "HKD"},
        {"ticker": "2577.HK", "name": "InnoScience Tech", "category": "HKEX / China Nodes", "def_price": 8.50, "def_r": 0.050, "def_v": 0.50, "currency": "HKD"},
        {"ticker": "6082.HK", "name": "Shanghai Biren Tech", "category": "HKEX / China Nodes", "def_price": 12.10, "def_r": 0.060, "def_v": 0.55, "currency": "HKD"},
        {"ticker": "9903.HK", "name": "Shanghai Iluvatar CoreX", "category": "HKEX / China Nodes", "def_price": 9.40, "def_r": 0.045, "def_v": 0.58, "currency": "HKD"}
    ]
    return assets_data

@st.cache_data(ttl=3600)
def load_live_market_data():
    raw_universe = get_definitive_global_universe()
    enriched_data = []
    for item in raw_universe:
        ticker_symbol = item["ticker"]
        last_price = item["def_price"]
        ann_10y = item["def_r"]
        vol = item["def_v"]
        try:
            ticker_obj = yf.Ticker(ticker_symbol)
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

with st.spinner("Streaming live price quotes directly from Yahoo Market terminals..."):
    LIVE_DATA = load_live_market_data()

# 3. GLOBAL APPLICATION INTERACTIVE STATE STORE ENGINE
if "focused_key" not in st.session_state:
    st.session_state.focused_key = "NVDA"

if "portfolio_weights" not in st.session_state:
    st.session_state.portfolio_weights = {str(item["ticker"]): 0 for item in LIVE_DATA}



