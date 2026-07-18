import streamlit as st
import numpy as np

# 1. VISUAL WORKSPACE AND LAYOUT CANVAS CONFIGURATION
st.set_page_config(layout="wide", page_title="Global Foundry Core Panel")

# 2. STRUCTURAL DATA UNIVERSE Matrix
RAW_DATA = [
    {"category": "Magnificent Seven", "name": "Nvidia Corp.", "ticker": "NVDA", "currency": "USD", "price": 135.50, "ann_10y": 0.452, "vol": 0.44, "industry": "AI Compute / GPUs", "geo": "USA"},
    {"category": "Magnificent Seven", "name": "Microsoft Corp.", "ticker": "MSFT", "currency": "USD", "price": 420.10, "ann_10y": 0.245, "vol": 0.22, "industry": "Enterprise Software / Cloud", "geo": "USA"},
    {"category": "Magnificent Seven", "name": "Apple Inc.", "ticker": "AAPL", "currency": "USD", "price": 225.40, "ann_10y": 0.221, "vol": 0.20, "industry": "Consumer Hardware / Mobile", "geo": "USA"},
    {"category": "Magnificent Seven", "name": "Alphabet Inc.", "ticker": "GOOGL", "currency": "USD", "price": 175.60, "ann_10y": 0.195, "vol": 0.24, "industry": "Digital Advertising / AI", "geo": "USA"},
    {"category": "Magnificent Seven", "name": "Amazon.com Inc.", "ticker": "AMZN", "currency": "USD", "price": 185.30, "ann_10y": 0.212, "vol": 0.28, "industry": "E-Commerce / Cloud Infrastructure", "geo": "USA"},
    {"category": "Magnificent Seven", "name": "Meta Platforms Inc.", "ticker": "META", "currency": "USD", "price": 495.20, "ann_10y": 0.228, "vol": 0.36, "industry": "Digital Advertising / Metaverse", "geo": "USA"},
    {"category": "Magnificent Seven", "name": "Tesla Inc.", "ticker": "TSLA", "currency": "USD", "price": 210.50, "ann_10y": 0.384, "vol": 0.52, "industry": "Automotive / Energy Storage", "geo": "USA"},
    {"category": "SOXX Top 15 Holdings", "name": "Advanced Micro Devices", "ticker": "AMD", "currency": "USD", "price": 154.40, "ann_10y": 0.315, "vol": 0.42, "industry": "AI Compute / CPUs", "geo": "USA"},
    {"category": "SOXX Top 15 Holdings", "name": "Micron Technology, Inc.", "ticker": "MU", "currency": "USD", "price": 94.50, "ann_10y": 0.198, "vol": 0.49, "industry": "Memory (HBM / DRAM)", "geo": "USA"},
    {"category": "SOXX Top 15 Holdings", "name": "Broadcom Inc.", "ticker": "AVGO", "currency": "USD", "price": 164.80, "ann_10y": 0.294, "vol": 0.27, "industry": "Networking / ASICs", "geo": "USA"},
    {"category": "SOXX Top 15 Holdings", "name": "Applied Materials, Inc.", "ticker": "AMAT", "currency": "USD", "price": 192.40, "ann_10y": 0.264, "vol": 0.34, "industry": "Wafer Fab Equipment", "geo": "USA"},
    {"category": "SOXX Top 15 Holdings", "name": "Intel Corporation", "ticker": "INTC", "currency": "USD", "price": 28.10, "ann_10y": 0.012, "vol": 0.39, "industry": "IDM / Foundry Transition", "geo": "USA"},
    {"category": "SOXX Top 15 Holdings", "name": "KLA Corporation", "ticker": "KLAC", "currency": "USD", "price": 685.20, "ann_10y": 0.256, "vol": 0.31, "industry": "Process Diagnostics Equipment", "geo": "USA"},
    {"category": "SOXX Top 15 Holdings", "name": "Lam Research Corp.", "ticker": "LRCX", "currency": "USD", "price": 842.50, "ann_10y": 0.284, "vol": 0.37, "industry": "Wafer Fab Equipment", "geo": "USA"},
    {"category": "SOXX Top 15 Holdings", "name": "Texas Instruments Inc.", "ticker": "TXN", "currency": "USD", "price": 178.60, "ann_10y": 0.142, "vol": 0.23, "industry": "Analog Nodes / Embedded Chips", "geo": "USA"},
    {"category": "SOXX Top 15 Holdings", "name": "Marvell Technology, Inc.", "ticker": "MRVL", "currency": "USD", "price": 68.20, "ann_10y": 0.201, "vol": 0.41, "industry": "Networking / Infrastructure", "geo": "USA"},
    {"category": "SOXX Top 15 Holdings", "name": "Qualcomm Inc.", "ticker": "QCOM", "currency": "USD", "price": 168.20, "ann_10y": 0.185, "vol": 0.35, "industry": "Mobile Wireless Edge", "geo": "USA"},
    {"category": "SOXX Top 15 Holdings", "name": "Monolithic Power Systems", "ticker": "MPWR", "currency": "USD", "price": 720.40, "ann_10y": 0.312, "vol": 0.33, "industry": "Analog Nodes / Power Systems", "geo": "USA"},
    {"category": "SOXX Top 15 Holdings", "name": "NXP Semiconductors N.V.", "ticker": "NXPI", "currency": "USD", "price": 265.22, "ann_10y": 0.161, "vol": 0.26, "industry": "Analog Nodes / Embedded Chips", "geo": "Netherlands"},
    {"category": "SOXX Top 15 Holdings", "name": "Analog Devices, Inc.", "ticker": "ADI", "currency": "USD", "price": 210.50, "ann_10y": 0.164, "vol": 0.25, "industry": "Analog Nodes / Signal Processing", "geo": "USA"},
    {"category": "Taiwan", "name": "TSMC", "ticker": "TSM", "currency": "USD", "price": 178.20, "ann_10y": 0.261, "vol": 0.33, "industry": "Pure-Play Foundry", "geo": "Taiwan"},
    {"category": "Taiwan", "name": "United Microelectronics", "ticker": "UMC", "currency": "USD", "price": 7.80, "ann_10y": 0.114, "vol": 0.36, "industry": "Pure-Play Foundry", "geo": "Taiwan"}
]

# 3. CONTEXT STATE MANAGEMENT
if "focused_key" not in st.session_state:
    st.session_state.focused_key = "NVDA"

if "portfolio_weights" not in st.session_state:
    st.session_state.portfolio_weights = {str(item["ticker"]): 0 for item in RAW_DATA}

st.title("📊 PORTFOLIO TESTING PANEL")

panel_left, panel_right = st.columns([1.3, 1.0], gap="large")

with panel_left:
    st.subheader("📂 Register Matrix")
    
    categories = ["All", "Magnificent Seven", "SOXX Top 15 Holdings", "Taiwan"]
    selected_cat = st.selectbox("Filter Active Assets Region", options=categories, index=0)
    
    ch1, ch2, ch3, ch4 = st.columns([0.6, 2.4, 1.2, 1.2])
    ch1.markdown("**TICK**")
    ch2.markdown("**STOCK ASSET LIST**")
    ch3.markdown("**ALLOCATION %**")
    ch4.markdown("**PRICE**")
    
    for idx, item in enumerate(RAW_DATA):
        if selected_cat != "All" and item["category"] != selected_cat:
            continue
            
        r1, r2, r3, r4 = st.columns([0.6, 2.4, 1.2, 1.2])
        ticker = str(item["ticker"])
        name = str(item["name"])
        
        is_checked = r1.checkbox("", value=(st.session_state.portfolio_weights[ticker] > 0), key=f"cb_v3_{ticker}_{idx}", label_visibility="collapsed")
        
        # FIXED: Safe, reactive rerun structure configuration
        if r2.button(f"🔗 {ticker} | {name[:18]}", key=f"lk_v3_{ticker}_{idx}"):
            st.session_state.focused_key = ticker
            st.rerun()
            
        if is_checked:
            old_val = st.session_state.portfolio_weights[ticker]
            initial_val = int(old_val) if old_val > 0 else 0
            new_alloc = r3.number_input("", min_value=0, max_value=100, value=initial_val, step=5, key=f"al_v3_{ticker}_{idx}", label_visibility="collapsed")
            st.session_state.portfolio_weights[ticker] = new_alloc
        else:
            st.session_state.portfolio_weights[ticker] = 0
            r3.markdown("<span style='color: #888888;'>MUTED</span>", unsafe_allow_html=True)
            
        r4.write(f"{item['currency']} {item['price']:,.2f}")

    st.write("")
    
    current_sum = sum(st.session_state.portfolio_weights.values())
    if current_sum == 100:
        st.success(f"🎯 READY TO EXECUTE: TOTAL SUM IS {current_sum}%")
    else:
        st.warning(f"⚠️ COMPLIANCE HOLD: TOTAL SUM IS {current_sum}% / 100%")
        
    entry_year = st.selectbox("🕹️ ENTRY YEAR", options=[2016, 2017, 2018, 2019, 2020, 2021, 2022], index=4)
    execute_backtest = st.button("🔴 RUN BACKTEST 🔴", use_container_width=True)

with panel_right:
    focus_ticker = st.session_state.focused_key
    
    target_record = None
    for item in RAW_DATA:
        if item["ticker"] == focus_ticker:
            target_record = item
            break
            
    if target_record is not None:
        st.subheader(f"📊 Data Profile: {target_record['ticker']}")
        st.text(f"{target_record['name']} ({target_record['category']})")
        st.markdown("---")
        
        met1, met2 = st.columns(2)
        met1.metric("LAST PRICE", f"{target_record['currency']} {target_record['price']:,.2f}")
        met2.metric("10Y COMP. RATE", f"{target_record['ann_10y']*100:.1f}%")
        
        st.markdown("---")
        st.subheader("🔬 Core Metadata Telemetry")
        st.write(f"- **Primary Domain Sector:** {target_record['industry']}")
        st.write(f"- **Geographic Processing Matrix:** {target_record['geo']}")
    else:
        st.write("Select an active asset to load data parameters.")

# 4. MATH SIMULATION PERFORMANCE EXECUTION MATRIX
if execute_backtest:
    total_alloc = sum(st.session_state.portfolio_weights.values())
    if total_alloc != 100:
        st.error(f"❌ COMPLIANCE REJECTION: Allocation must total exactly 100%. Current sum: {total_alloc}%")
    else:
        st.markdown("---")
        st.subheader("🎯 Backtest Performance Simulation Results")
        
        table_summary = []
        current_year = 2026
        years_elapsed = current_year - entry_year
        
        for ticker, weight in st.session_state.portfolio_weights.items():
            if weight <= 0:
                continue
                
            asset_data = None
            for item in RAW_DATA:
                if item["ticker"] == ticker:
                    asset_data = item
                    break
                    
            if asset_data is not None:
                r = float(asset_data['ann_10y'])
                v = float(asset_data['vol'])
                
                growth_factor = np.exp((r - 0.5 * (v**2)) * years_elapsed)
                allocated_base = 100000 * (weight / 100.0)
                final_v = allocated_base * growth_factor
                perf_pct = (growth_factor - 1.0) * 100
                
                table_summary.append({
                    "Asset Ticker": ticker,
                    "Allocation Weight": f"{weight}%",
                    "Principal Base": f"${allocated_base:,.2f}",
                    f"Terminal Value ({current_year})": f"${final_v:,.2f}",
                    "Absolute Performance": f"{perf_pct:+.1f}%"
