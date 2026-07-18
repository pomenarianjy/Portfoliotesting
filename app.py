import streamlit as st
import pandas as pd
import numpy as np

# 1. EMULATE NATIVE LIGHT THEME SETTINGS (STRICT OVERRIDE)
st.set_page_config(
    layout="wide", 
    page_title="Portfolio Panel",
    initial_sidebar_state="collapsed"
)

# Completely strip dark-mode context by forcing browser variables to light values
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stMain"] {
        background-color: #FFFFFF !important;
        color: #111111 !important;
    }
    h1, h2, h3, h4, h5, h6, label, p, span, div, .stMarkdown {
        color: #111111 !important;
    }
    input, button, select, div[data-baseweb="select"], div[data-baseweb="input"] {
        background-color: #F8F9FA !important;
        color: #111111 !important;
        border: 1px solid #CCCCCC !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. RAW UNIVERSE TEXT MATRICES
RAW_UNIVERSE = [
    "Magnificent Seven|Nvidia Corp.|NVDA|USD|135.50|0.452|0.44|AI GPUs|USA",
    "Magnificent Seven|Microsoft Corp.|MSFT|USD|420.10|0.245|0.22|Cloud Software|USA",
    "Magnificent Seven|Apple Inc.|AAPL|USD|225.40|0.221|0.20|Hardware|USA",
    "SOXX Holdings|Advanced Micro Devices|AMD|USD|154.40|0.315|0.42|AI Processors|USA",
    "SOXX Holdings|Broadcom Inc.|AVGO|USD|164.80|0.294|0.27|ASICs/Networking|USA",
    "Taiwan Foundry|TSMC|TSM|USD|178.20|0.261|0.33|Pure-Play Foundry|Taiwan",
    "Taiwan Foundry|United Microelectronics|UMC|USD|7.80|0.114|0.36|Legacy Foundry|Taiwan"
]

@st.cache_data
def load_fixed_dataframe():
    rows = []
    for item in RAW_UNIVERSE:
        p = item.split("|")
        rows.append({
            "category": p[0], "name": p[1], "ticker": p[2], "currency": p[3],
            "price": float(p[4]), "ann_10y": float(p[5]), "vol": float(p[6]),
            "industry": p[7], "geo": p[8]
        })
    return pd.DataFrame(rows)

df = load_fixed_dataframe()

# Initialize session items without dictionary structures that cause key failures
if "focused_asset" not in st.session_state:
    st.session_state.focused_asset = "NVDA"

if "weights" not in st.session_state:
    st.session_state.weights = {r["ticker"]: 0 for _, r in df.iterrows()}

st.title("📊 PORTFOLIO TESTING PANEL")

col_left, col_right = st.columns([1.3, 1.0], gap="large")

with col_left:
    st.subheader("📂 Register Matrix")
    
    categories = ["All", "Magnificent Seven", "SOXX Holdings", "Taiwan Foundry"]
    selected_cat = st.selectbox("Filter Active Assets Region", options=categories)
    
    # Static column header definitions
    h1, h2, h3, h4 = st.columns([0.6, 2.4, 1.2, 1.2])
    h1.markdown("**TICK**")
    h2.markdown("**STOCK ASSET LIST**")
    h3.markdown("**ALLOCATION %**")
    h4.markdown("**PRICE**")
    
    for idx, row in df.iterrows():
        if selected_cat != "All" and row["category"] != selected_cat:
            continue
            
        tick = row["ticker"]
        r1, r2, r3, r4 = st.columns([0.6, 2.4, 1.2, 1.2])
        
        # Determine if asset checkbox is marked active
        is_active = r1.checkbox("", value=(st.session_state.weights[tick] > 0), key=f"chk_{tick}_{idx}", label_visibility="collapsed")
        
        if r2.button(f"🔗 {tick} | {row['name'][:18]}", key=f"btn_{tick}_{idx}"):
            st.session_state.focused_asset = tick
            st.rerun()
            
        if is_active:
            current_weight = st.session_state.weights[tick]
            start_val = int(current_weight) if current_weight > 0 else 0
            val = r3.number_input("", min_value=0, max_value=100, value=start_val, step=5, key=f"num_{tick}_{idx}", label_visibility="collapsed")
            st.session_state.weights[tick] = val
        else:
            st.session_state.weights[tick] = 0
            r3.markdown("<span style='color: #888888;'>MUTED</span>", unsafe_allow_html=True)
            
        r4.write(f"{row['currency']} {row['price']:,.2f}")

    st.write("")
    total_allocation = sum(st.session_state.weights.values())
    
    if total_allocation == 100:
        st.success(f"🎯 READY TO EXECUTE: TOTAL SUM IS {total_allocation}%")
    else:
        st.warning(f"⚠️ COMPLIANCE HOLD: TOTAL SUM IS {total_allocation}% / 100%")
        
    entry_year = st.selectbox("🕹️ ENTRY YEAR", options=[2016, 2017, 2018, 2019, 2020, 2021], index=2)
    run_backtest = st.button("🔴 RUN BACKTEST 🔴", use_container_width=True)

with col_right:
    active_target = st.session_state.focused_asset
    target_data = df[df["ticker"] == active_target]
    
    if not target_data.empty:
        # FIXED: Pulled out clean basic scalar values without using nested lists or index zero dictionary strings
        f_name = target_data["name"].values[0]
        f_cat = target_data["category"].values[0]
        f_price = target_data["price"].values[0]
        f_curr = target_data["currency"].values[0]
        f_ret = target_data["ann_10y"].values[0]
        f_ind = target_data["industry"].values[0]
        f_geo = target_data["geo"].values[0]
        
        st.subheader(f"📊 Data Profile: {active_target}")
        st.text(f"{f_name} ({f_cat})")
        st.markdown("---")
        
        m1, m2 = st.columns(2)
        m1.metric("LAST PRICE", f"{f_curr} {f_price:,.2f}")
        m2.metric("10Y COMP. RATE", f"{f_ret*100:.1f}%")
        
        st.markdown("---")
        st.markdown(f"- **Primary Sector Domain:** {f_ind}")
        st.markdown(f"- **Geographic Processing Matrix:** {f_geo}")
    else:
        st.write("Select an active asset to load data parameters.")

# 5. SECURE NON-GRAPH PERFORMANCE LEDGER SIMULATION
if run_backtest:
    if total_allocation != 100:
        st.error(f"❌ COMPLIANCE REJECTION: Allocation must total exactly 100%. Current sum: {total_allocation}%")
    else:
        st.markdown("---")
        st.subheader("🎯 Backtest Performance Simulation Results")
        
        table_output = []
        current_year = 2026
        years_elapsed = current_year - entry_year
        
        for ticker, alloc in st.session_state.weights.items():
            if alloc <= 0:
                continue
                
            match = df[df["ticker"] == ticker]
            if not match.empty:
                r_rate = match["ann_10y"].values[0]
                v_rate = match["vol"].values[0]
                
                # Formula simulation calculation engine without plot graphs
                growth_factor = np.exp((r_rate - 0.5 * (v_rate**2)) * years_elapsed)
                allocated_principal = 100000 * (alloc / 100.0)
                terminal_value = allocated_principal * growth_factor
                perf_pct = (growth_factor - 1.0) * 100
                
                table_output.append({
                    "Asset Ticker": ticker,
                    "Allocation Weight": f"{alloc}%",
                    "Principal Base": f"${allocated_principal:,.2f}",
                    f"Terminal Value ({current_year})": f"${terminal_value:,.2f}",
                    "Absolute Performance": f"{perf_pct:+.1f}%"
                })
                
        if table_output:
            st.markdown("### 📋 Position Historical Balances Ledger")
            st.table(pd.DataFrame(table_output))
        else:
            st.error("No active positions selected.")












            

