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

# 2. SEED DATA GENERATION MATRIX (ALL 48 GLOBAL Technology ASSETS EMBEDDED INTEGRALLY)
@st.cache_data
def get_definitive_global_universe():
    assets_data = [
        # --- Magnificent Seven ---
        {"ticker": "NVDA", "name": "Nvidia Corp.", "category": "Magnificent Seven", "price": 135.50, "ann_10y": 0.452, "vol": 0.44, "currency": "USD"},
        {"ticker": "MSFT", "name": "Microsoft Corp.", "category": "Magnificent Seven", "price": 420.10, "ann_10y": 0.245, "vol": 0.22, "currency": "USD"},
        {"ticker": "AAPL", "name": "Apple Inc.", "category": "Magnificent Seven", "price": 225.40, "ann_10y": 0.221, "vol": 0.20, "currency": "USD"},
        {"ticker": "GOOGL", "name": "Alphabet Inc.", "category": "Magnificent Seven", "price": 175.60, "ann_10y": 0.195, "vol": 0.24, "currency": "USD"},
        {"ticker": "AMZN", "name": "Amazon.com Inc.", "category": "Magnificent Seven", "price": 185.30, "ann_10y": 0.212, "vol": 0.28, "currency": "USD"},
        {"ticker": "META", "name": "Meta Platforms Inc.", "category": "Magnificent Seven", "price": 495.20, "ann_10y": 0.228, "vol": 0.36, "currency": "USD"},
        {"ticker": "TSLA", "name": "Tesla Inc.", "category": "Magnificent Seven", "price": 210.50, "ann_10y": 0.384, "vol": 0.52, "currency": "USD"},
        
        # --- SOXX Top 15 Holdings ---
        {"ticker": "AMD", "name": "Advanced Micro Devices", "category": "SOXX Top 15 Holdings", "price": 154.40, "ann_10y": 0.315, "vol": 0.42, "currency": "USD"},
        {"ticker": "MU", "name": "Micron Technology", "category": "SOXX Top 15 Holdings", "price": 94.50, "ann_10y": 0.198, "vol": 0.49, "currency": "USD"},
        {"ticker": "AVGO", "name": "Broadcom Inc.", "category": "SOXX Top 15 Holdings", "price": 164.80, "ann_10y": 0.294, "vol": 0.27, "currency": "USD"},
        {"ticker": "AMAT", "name": "Applied Materials", "category": "SOXX Top 15 Holdings", "price": 192.40, "ann_10y": 0.264, "vol": 0.34, "currency": "USD"},
        {"ticker": "INTC", "name": "Intel Corp.", "category": "SOXX Top 15 Holdings", "price": 28.10, "ann_10y": 0.012, "vol": 0.39, "currency": "USD"},
        {"ticker": "KLAC", "name": "KLA Corporation", "category": "SOXX Top 15 Holdings", "price": 685.20, "ann_10y": 0.256, "vol": 0.31, "currency": "USD"},
        {"ticker": "LRCX", "name": "Lam Research Corp.", "category": "SOXX Top 15 Holdings", "price": 842.50, "ann_10y": 0.284, "vol": 0.37, "currency": "USD"},
        {"ticker": "TXN", "name": "Texas Instruments", "category": "SOXX Top 15 Holdings", "price": 178.60, "ann_10y": 0.142, "vol": 0.23, "currency": "USD"},
        {"ticker": "MRVL", "name": "Marvell Technology", "category": "SOXX Top 15 Holdings", "price": 68.20, "ann_10y": 0.201, "vol": 0.41, "currency": "USD"},
        {"ticker": "QCOM", "name": "Qualcomm Inc.", "category": "SOXX Top 15 Holdings", "price": 168.20, "ann_10y": 0.185, "vol": 0.35, "currency": "USD"},
        {"ticker": "MPWR", "name": "Monolithic Power Systems", "category": "SOXX Top 15 Holdings", "price": 720.40, "ann_10y": 0.312, "vol": 0.33, "currency": "USD"},
        {"ticker": "NXPI", "name": "NXP Semiconductors N.V.", "category": "SOXX Top 15 Holdings", "price": 265.22, "ann_10y": 0.161, "vol": 0.26, "currency": "USD"},
        {"ticker": "ADI", "name": "Analog Devices, Inc.", "category": "SOXX Top 15 Holdings", "price": 210.50, "ann_10y": 0.164, "vol": 0.25, "currency": "USD"},
        
        # --- Taiwan ---
        {"ticker": "TSM", "name": "TSMC", "category": "Taiwan", "price": 178.20, "ann_10y": 0.261, "vol": 0.33, "currency": "USD"},
        {"ticker": "UMC", "name": "United Microelectronics", "category": "Taiwan", "price": 7.80, "ann_10y": 0.114, "vol": 0.36, "currency": "USD"},
        {"ticker": "5347.TW", "name": "Vanguard International", "category": "Taiwan", "price": 112.50, "ann_10y": 0.095, "vol": 0.32, "currency": "TWD"},
        {"ticker": "2454.TW", "name": "MediaTek Inc.", "category": "Taiwan", "price": 1240.00, "ann_10y": 0.184, "vol": 0.38, "currency": "TWD"},
        {"ticker": "3034.TW", "name": "Novatek Microelectronics", "category": "Taiwan", "price": 510.00, "ann_10y": 0.141, "vol": 0.30, "currency": "TWD"},
        {"ticker": "2379.TW", "name": "Realtek Semiconductor", "category": "Taiwan", "price": 485.00, "ann_10y": 0.162, "vol": 0.34, "currency": "TWD"},
        {"ticker": "3661.TW", "name": "Alchip Technologies", "category": "Taiwan", "price": 2450.00, "ann_10y": 0.412, "vol": 0.55, "currency": "TWD"},
        {"ticker": "ASX", "name": "ASE Technology Holding", "category": "Taiwan", "price": 14.50, "ann_10y": 0.124, "vol": 0.29, "currency": "USD"},
        
        # --- Japan ---
        {"ticker": "8035.T", "name": "Tokyo Electron", "category": "Japan", "price": 24500.00, "ann_10y": 0.231, "vol": 0.36, "currency": "JPY"},
        {"ticker": "6857.T", "name": "Advantest Corp.", "category": "Japan", "price": 5800.00, "ann_10y": 0.252, "vol": 0.39, "currency": "JPY"},
        {"ticker": "6146.T", "name": "Disco Corp.", "category": "Japan", "price": 41200.00, "ann_10y": 0.342, "vol": 0.41, "currency": "JPY"},
        {"ticker": "6920.T", "name": "Lasertec Corp.", "category": "Japan", "price": 22400.00, "ann_10y": 0.485, "vol": 0.48, "currency": "JPY"},
        {"ticker": "7735.T", "name": "SCREEN Holdings", "category": "Japan", "price": 9800.00, "ann_10y": 0.221, "vol": 0.38, "currency": "JPY"},
        {"ticker": "6525.T", "name": "Kokusai Electric", "category": "Japan", "price": 3100.00, "ann_10y": 0.165, "vol": 0.35, "currency": "JPY"},
        {"ticker": "285A.T", "name": "Kioxia Holdings", "category": "Japan", "price": 2850.00, "ann_10y": 0.112, "vol": 0.43, "currency": "JPY"},
        {"ticker": "6723.T", "name": "Renesas Electronics", "category": "Japan", "price": 2450.00, "ann_10y": 0.154, "vol": 0.32, "currency": "JPY"},
        {"ticker": "4062.T", "name": "Ibiden Co.", "category": "Japan", "price": 4800.00, "ann_10y": 0.132, "vol": 0.33, "currency": "JPY"},
        {"ticker": "6963.T", "name": "ROHM Co.", "category": "Japan", "price": 1850.00, "ann_10y": 0.084, "vol": 0.29, "currency": "JPY"},
        
        # --- South Korea ---
        {"ticker": "005930.KS", "name": "Samsung Electronics", "category": "South Korea", "price": 68500.00, "ann_10y": 0.112, "vol": 0.31, "currency": "KRW"},
        {"ticker": "000660.KS", "name": "SK Hynix", "category": "South Korea", "price": 165000.00, "ann_10y": 0.214, "vol": 0.42, "currency": "KRW"},
        
        # --- Europe ---
        {"ticker": "ASML", "name": "ASML Holding N.V.", "category": "Europe", "price": 820.10, "ann_10y": 0.225, "vol": 0.28, "currency": "USD"},
        {"ticker": "IFX", "name": "Infineon Technologies", "category": "Europe", "price": 34.20, "ann_10y": 0.145, "vol": 0.33, "currency": "EUR"},
        
        # --- HKEX / China Nodes ---
        {"ticker": "0981.HK", "name": "SMIC", "category": "HKEX / China Nodes", "price": 22.40, "ann_10y": 0.125, "vol": 0.45, "currency": "HKD"},
        {"ticker": "1347.HK", "name": "Hua Hong Semi", "category": "HKEX / China Nodes", "price": 18.50, "ann_10y": 0.091, "vol": 0.41, "currency": "HKD"},
        {"ticker": "1385.HK", "name": "Shanghai Fudan Micro", "category": "HKEX / China Nodes", "price": 14.20, "ann_10y": 0.154, "vol": 0.48, "currency": "HKD"},
        {"ticker": "2577.HK", "name": "InnoScience Tech", "category": "HKEX / China Nodes", "price": 8.50, "ann_10y": 0.050, "vol": 0.50, "currency": "HKD"},
        {"ticker": "6082.HK", "name": "Shanghai Biren Tech", "category": "HKEX / China Nodes", "price": 12.10, "ann_10y": 0.060, "vol": 0.55, "currency": "HKD"},
        {"ticker": "9903.HK", "name": "Shanghai Iluvatar CoreX", "category": "HKEX / China Nodes", "price": 9.40, "ann_10y": 0.045, "vol": 0.58, "currency": "HKD"}
    ]
    return assets_data

@st.cache_data(ttl=3600)
def load_live_market_data():
    raw_universe = get_definitive_global_universe()
    enriched_data = []
    for item in raw_universe:
        ticker_symbol = item["ticker"]
        last_price = item["price"]
        try:
            ticker_obj = yf.Ticker(ticker_symbol)
            history = ticker_obj.history(period="1d")
            if history is not None and not history.empty:
                last_price = float(history['Close'].iloc[-1])
        except Exception:
            pass
        enriched_item = item.copy()
        enriched_item["price"] = last_price
        enriched_data.append(enriched_item)
    return enriched_data

with st.spinner("Streaming live price quotes directly from global tech terminals..."):
    LIVE_DATA = load_live_market_data()

# 3. GLOBAL APPLICATION INTERACTIVE STATE STORE ENGINE
if "df_portfolio" not in st.session_state:
    base_df = pd.DataFrame(LIVE_DATA)
    base_df.insert(0, "SELECT", False)
    base_df["ALLOCATION %"] = 0
    st.session_state.df_portfolio = base_df

st.title("📊 JASMINE'S LIVE PORTFOLIO PANEL")

st.subheader("📂 Global Asset Ledger Matrix")
categories = ["All", "Magnificent Seven", "SOXX Top 15 Holdings", "Taiwan", "Japan", "South Korea", "Europe", "HKEX / China Nodes"]
selected_cat = st.selectbox("Filter Active Assets Region", options=categories, index=0)

if selected_cat == "All":
    filtered_view = st.session_state.df_portfolio
else:
    filtered_view = st.session_state.df_portfolio[st.session_state.df_portfolio["category"] == selected_cat]

col_btn1, col_btn2 = st.columns(2)
if col_btn1.button("🎚️ EQUAL WEIGHT DISTRIBUTE (CHECKED STOCKS ONLY)", use_container_width=True):
