import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as px
import plotly.express as px_exp

# 1. CONFIGURE NINTENDO STYLING & PAGE SETUP
st.set_page_config(layout="wide", page_title="Portfolio Testing", page_icon="🎮")

st.markdown("""
<style>
    @import url('https://googleapis.com');
    
    /* Global Base Text & Theme */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #F8F8F8;
        color: #000000;
        font-family: 'Share Tech Mono', monospace;
    }
    
    /* Retro Nintendo Headers */
    .retro-title {
        font-family: 'Press Start 2P', cursive;
        color: #E60012; /* Nintendo Red */
        font-size: 32px;
        text-shadow: 3px 3px 0px #8C8C8C;
        margin-bottom: 5px;
    }
    .retro-subtitle {
        font-family: 'Share Tech Mono', monospace;
        color: #000000;
        font-size: 18px;
        letter-spacing: 2px;
        text-transform: uppercase;
        border-bottom: 4px solid #E60012;
        padding-bottom: 8px;
        margin-bottom: 25px;
    }
    
    /* Panel Grid Containers */
    .retro-box {
        background-color: #FFFFFF;
        border: 4px solid #000000;
        box-shadow: 5px 5px 0px #8C8C8C;
        padding: 15px;
        margin-bottom: 20px;
    }
    
    /* Customized Buttons */
    .stButton>button {
        font-family: 'Press Start 2P', cursive !important;
        background-color: #38D038 !important; /* Yoshi Green */
        color: #FFFFFF !important;
        border: 4px solid #000000 !important;
        box-shadow: 4px 4px 0px #8C8C8C !important;
        font-size: 16px !important;
        padding: 10px 25px !important;
        width: 100%;
        image-rendering: pixelated;
    }
    .stButton>button:hover {
        background-color: #E60012 !important; /* Turns Mario Red on selection */
        color: #FFFFFF !important;
        cursor: pointer;
    }
    
    /* Metric styling */
    .metric-label {
        font-weight: bold;
        color: #8C8C8C;
        font-size: 12px;
        text-transform: uppercase;
    }
    .metric-val {
        font-size: 20px;
        color: #000000;
        font-family: 'Share Tech Mono', monospace;
        font-weight: bold;
    }
</style>
""", unsafe_html=True)

# 2. SEED INSTITUTIONAL CHIP-SECTOR SPECIFIC DATASET
@st.cache_data
def load_family_office_universe():
    return {
        "NVIDIA (NVDA)": {
            "name": "NVIDIA Corporation", "ticker": "NVDA", "currency": "USD", "price": 203.31,
            "ytd": 0.0927, "ann_10y": 0.5935, "mcap": "4.90T", "vol": 0.48, "industry": "AI Compute / GPUs",
            "geo": "USA", "qoq_rev": 0.18, "yoy_rev": 1.12, "gross_margin": 0.76, "op_margin": 0.62,
            "fcf": "27.2B", "capex": "3.8B", "utilization": 0.95, "yield_rate": 0.91
        },
        "TSMC (TSM)": {
            "name": "Taiwan Semiconductor Manufacturing Co.", "ticker": "TSM", "currency": "USD", "price": 397.62,
            "ytd": 0.3540, "ann_10y": 0.2810, "mcap": "2.10T", "vol": 0.32, "industry": "Pure-Play Foundry",
            "geo": "Taiwan", "qoq_rev": 0.08, "yoy_rev": 0.32, "gross_margin": 0.54, "op_margin": 0.43,
            "fcf": "18.5B", "capex": "32.0B", "utilization": 0.92, "yield_rate": 0.88
        },
        "ASML (ASML)": {
            "name": "ASML Holding N.V.", "ticker": "ASML", "currency": "EUR", "price": 875.40,
            "ytd": 0.1250, "ann_10y": 0.2640, "mcap": "350.2B", "vol": 0.29, "industry": "Lithography Equipment",
            "geo": "Netherlands", "qoq_rev": 0.04, "yoy_rev": 0.15, "gross_margin": 0.51, "op_margin": 0.32,
            "fcf": "7.1B", "capex": "2.8B", "utilization": 0.89, "yield_rate": 0.99
        },
        "AMD (AMD)": {
            "name": "Advanced Micro Devices, Inc.", "ticker": "AMD", "currency": "USD", "price": 168.50,
            "ytd": 1.4953, "ann_10y": 0.4120, "mcap": "272.4B", "vol": 0.45, "industry": "AI Compute / CPUs",
            "geo": "USA", "qoq_rev": 0.11, "yoy_rev": 0.24, "gross_margin": 0.47, "op_margin": 0.18,
            "fcf": "3.2B", "capex": "1.1B", "utilization": 0.88, "yield_rate": 0.84
        },
        "Broadcom (AVGO)": {
            "name": "Broadcom Inc.", "ticker": "AVGO", "currency": "USD", "price": 1720.15,
            "ytd": 0.1134, "ann_10y": 0.3470, "mcap": "802.1B", "vol": 0.26, "industry": "Networking / Custom ASIC",
            "geo": "USA", "qoq_rev": 0.06, "yoy_rev": 0.43, "gross_margin": 0.65, "op_margin": 0.46,
            "fcf": "19.1B", "capex": "0.9B", "utilization": 0.85, "yield_rate": 0.82
        },
        "Micron (MU)": {
            "name": "Micron Technology, Inc.", "ticker": "MU", "currency": "USD", "price": 131.20,
            "ytd": 2.2840, "ann_10y": 0.2150, "mcap": "145.3B", "vol": 0.52, "industry": "Memory (HBM / DRAM)",
            "geo": "USA", "qoq_rev": 0.24, "yoy_rev": 0.86, "gross_margin": 0.39, "op_margin": 0.22,
            "fcf": "-1.4B", "capex": "8.5B", "utilization": 0.78, "yield_rate": 0.74
        },
        "Intel (INTC)": {
            "name": "Intel Corporation", "ticker": "INTC", "currency": "USD", "price": 35.40,
            "ytd": 1.7946, "ann_10y": 0.0240, "mcap": "151.2B", "vol": 0.38, "industry": "IDM / Foundry Transition",
            "geo": "USA", "qoq_rev": -0.02, "yoy_rev": 0.05, "gross_margin": 0.41, "op_margin": 0.09,
            "fcf": "-4.8B", "capex": "24.1B", "utilization": 0.72, "yield_rate": 0.68
        }
    }

universe = load_family_office_universe()

# 3. INTERACTIVE TITLE BANNER
st.markdown('<div class="retro-title">PORTFOLIO TESTING</div>', unsafe_html=True)
st.markdown('<div class="retro-subtitle">A Single Family Office Operations Panel</div>', unsafe_html=True)

# Initialize selected stock view index in state
if "focused_stock" not in st.session_state:
    st.session_state.focused_stock = list(universe.keys())[0]

# 4. TWO-COLUMN SPLIT PANEL VIEW
col_left, col_right = st.columns([3, 2])

with col_left:
    st.markdown('<div class="retro-box"><strong>🕹️ ASSET SELECTION & TICKETING</strong></div>', unsafe_html=True)
    
    allocations = {}
    ticks = {}
    
    # Custom pixel headers
    h_col1, h_col2, h_col3, h_col4 = st.columns([1, 4, 3, 3])
    h_col1.markdown("**TICK**")
    h_col2.markdown("**STOCK ASSET**")
    h_col3.markdown("**ALLOCATION %**")
    h_col4.markdown("**MARKET VALUE**")
    
    # Loop over predefined high-priority equities
    for key, data in universe.items():
        r_col1, r_col2, r_col3, r_col4 = st.columns([1, 4, 3, 3])
        
        # Checkbox for asset gating
        ticks[key] = r_col1.checkbox("", value=True, key=f"tick_{key}", label_visibility="collapsed")
        
        # Link action simulated via text button
        if r_col2.button(f"{data['ticker']} | {data['name']}", key=f"btn_{key}"):
            st.session_state.focused_stock = key
            
        # Target allocation metric input fields
        if ticks[key]:
            allocations[key] = r_col3.number_input("", min_value=0, max_value=100, value=0, step=5, key=f"alloc_{key}", label_visibility="collapsed")
        else:
            allocations[key] = 0
            r_col3.markdown("<span style='color:#8C8C8C;'>---</span>", unsafe_html=True)
            
        r_col4.write(f"{data['currency']} {data['price']:,.2f}")
        
    st.markdown("<br>", unsafe_html=True)
    
    # Portfolio Gating Controls
    c_y1, c_y2 = st.columns(2)
    entry_year = c_y1.selectbox("🎮 SELECT ENTRY YEAR", options=[2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025])
    
    # Decided Launch Mechanism centered at bottom middle
    st.markdown("<div style='text-align: center; margin-top:20px;'>", unsafe_html=True)
    submit_run = st.button("🔴 DECIDED 🔴")
    st.markdown("</div>", unsafe_html=True)

# 5. RIGHT HAND DATA PANEL (METRICS EXPLORER)
with col_right:
    focus_key = st.session_state.focused_stock
    f_data = universe[focus_key]
    
    st.markdown(f'<div class="retro-box" style="border-color:#E60012;">', unsafe_html=True)
    st.subheader(f"📊 MONITOR: {f_data['name']} ({f_data['ticker']})")
    
    m1, m2 = st.columns(2)
    m1.markdown(f'<p class="metric-label">Last Price</p><p class="metric-val">{f_data["currency"]} {f_data["price"]}</p>', unsafe_html=True)
    m2.markdown(f'<p class="metric-label">Market Cap</p><p class="metric-val">{f_data["mcap"]}</p>', unsafe_html=True)
    
    m3, m4 = st.columns(2)
    m3.markdown(f'<p class="metric-label">YTD Return</p><p class="metric-val" style="color:#38D038;">{f_data["ytd"]*100:+.2f}%</p>', unsafe_html=True)
    m4.markdown(f'<p class="metric-label">10Y Annual Return</p><p class="metric-val">{f_data["ann_10y"]*100:.2f}%</p>', unsafe_html=True)
    
    st.markdown("<hr style='border:1px solid #000;'>", unsafe_html=True)
    st.markdown("**ADVANCED NODE FOUNDRY METRICS**")
    
    # Critical structural semiconductor tracking indicators
    st.write(f"📈 **Revenue Growth Trend:** QoQ: **{f_data['qoq_rev']*100:+.1f}%** | YoY: **{f_data['yoy_rev']*100:+.1f}%**")
    st.write(f"🔬 **Gross Profit Margin:** **{f_data['gross_margin']*100:.1f}%** (Advanced node packaging scale factor)")
    st.write(f"💼 **Operating Margin:** **{f_data['op_margin']*100:.1f}%** (R&D scaling structural leverage)")
    st.write(f"💸 **Free Cash Flow:** **USD {f_data['fcf']}** (Post-infrastructure remaining liquidity)")
    st.write(f"🏗️ **Capex Budget:** **USD {f_data['capex']}** (Tooling & greenfield fab expansion signaling)")
    
    # Critical Guardrail Metric Check
    util = f_data['utilization'] * 100
    util_color = "#E60012" if util < 80 else "#38D038"
    st.write(f"⚙️ **Wafer Fab Utilization:** <span style='color:{util_color}; font-weight:bold;'>{util:.1f}%</span> (Sub-80% thresholds significantly compress margins)", unsafe_html=True)
