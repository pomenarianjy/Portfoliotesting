import streamlit as st
import pandas as pd
import numpy as np

# Defensive package loading wrapper
try:
    import plotly.graph_objects as go
    import plotly.express as px
except ModuleNotFoundError:
    st.error("🔧 ENVIRONMENT ERROR: Please ensure 'plotly' is written inside your requirements.txt file.")
    st.stop()

# 1. STYLE CONFIGURATION & NES HARDWARE PALETTE
st.set_page_config(layout="wide", page_title="Portfolio Testing", page_icon="🎮")

NES_RED = "#E60012"
NES_BLACK = "#000000"
NES_GRAY = "#8C8C8C"
NES_GREEN = "#38D038"
NES_BG = "#F8F8F8"

st.markdown(f"""
<style>
    @import url('https://googleapis.com');
    
    html, body, [data-testid="stAppViewContainer"] {{
        background-color: {NES_BG};
        color: {NES_BLACK};
        font-family: 'Share Tech Mono', monospace;
    }}
    .retro-title {{
        font-family: 'Press Start 2P', cursive;
        color: {NES_RED};
        font-size: 26px;
        text-shadow: 2px 2px 0px {NES_GRAY};
        margin-bottom: 2px;
    }}
    .retro-subtitle {{
        font-family: 'Share Tech Mono', monospace;
        color: {NES_BLACK};
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 2px;
        border-bottom: 3px solid {NES_RED};
        padding-bottom: 6px;
        margin-bottom: 20px;
    }}
    .retro-card {{
        background-color: #FFFFFF;
        border: 3px solid {NES_BLACK};
        box-shadow: 4px 4px 0px {NES_GRAY};
        padding: 16px;
        margin-bottom: 16px;
        border-radius: 4px;
    }}
    .stButton>button {{
        font-family: 'Press Start 2P', cursive !important;
        background-color: {NES_GREEN} !important;
        color: #FFFFFF !important;
        border: 3px solid {NES_BLACK} !important;
        box-shadow: 3px 3px 0px {NES_GRAY} !important;
        font-size: 13px !important;
        padding: 12px 0px !important;
        width: 100%;
    }}
    .stButton>button:hover {{
        background-color: {NES_RED} !important;
    }}
</style>
""", unsafe_html=True)

# 2. FAMILY OFFICE SEMICONDUCTOR DATASET
@st.cache_data
def get_universe_data():
    return {
        "NVIDIA (NVDA)": {
            "name": "NVIDIA Corporation", "ticker": "NVDA", "currency": "USD", "price": 135.50,
            "ytd": 0.125, "ann_10y": 0.584, "mcap": "3.33T", "vol": 0.44, "industry": "AI Compute / GPUs",
            "geo": "USA", "qoq_rev": 0.15, "yoy_rev": 1.22, "gross_margin": 0.75, "op_margin": 0.61,
            "fcf": "26.4B", "capex": "3.9B", "utilization": 0.96, "yield_rate": 0.89
        },
        "TSMC (TSM)": {
            "name": "Taiwan Semiconductor Mfg Co.", "ticker": "TSM", "currency": "USD", "price": 178.20,
            "ytd": 0.385, "ann_10y": 0.261, "mcap": "924.5B", "vol": 0.33, "industry": "Pure-Play Foundry",
            "geo": "Taiwan", "qoq_rev": 0.09, "yoy_rev": 0.36, "gross_margin": 0.53, "op_margin": 0.42,
            "fcf": "19.1B", "capex": "30.5B", "utilization": 0.93, "yield_rate": 0.87
        },
        "ASML (ASML)": {
            "name": "ASML Holding N.V.", "ticker": "ASML", "currency": "EUR", "price": 820.10,
            "ytd": 0.089, "ann_10y": 0.252, "mcap": "322.0B", "vol": 0.28, "industry": "Lithography Equipment",
            "geo": "Netherlands", "qoq_rev": 0.03, "yoy_rev": 0.11, "gross_margin": 0.50, "op_margin": 0.31,
            "fcf": "6.8B", "capex": "2.5B", "utilization": 0.88, "yield_rate": 0.98
        },
        "AMD (AMD)": {
            "name": "Advanced Micro Devices", "ticker": "AMD", "currency": "USD", "price": 154.40,
            "ytd": -0.042, "ann_10y": 0.395, "mcap": "249.6B", "vol": 0.42, "industry": "AI Compute / CPUs",
            "geo": "USA", "qoq_rev": 0.10, "yoy_rev": 0.18, "gross_margin": 0.48, "op_margin": 0.19,
            "fcf": "3.1B", "capex": "1.2B", "utilization": 0.86, "yield_rate": 0.83
        },
        "Broadcom (AVGO)": {
            "name": "Broadcom Inc.", "ticker": "AVGO", "currency": "USD", "price": 164.80,
            "ytd": 0.221, "ann_10y": 0.332, "mcap": "766.4B", "vol": 0.27, "industry": "Networking / ASICs",
            "geo": "USA", "qoq_rev": 0.05, "yoy_rev": 0.47, "gross_margin": 0.62, "op_margin": 0.44,
            "fcf": "18.2B", "capex": "1.0B", "utilization": 0.84, "yield_rate": 0.81
        }
    }

universe = get_universe_data()

if "focused_stock" not in st.session_state:
    st.session_state.focused_stock = list(universe.keys())[0]

# Banner Elements
st.markdown('<div class="retro-title">PORTFOLIO TESTING</div>', unsafe_html=True)
st.markdown('<div class="retro-subtitle">A Single Family Office Front Page Panel</div>', unsafe_html=True)

# 3. SPLIT PANEL SYSTEM LAYOUT
panel_left, panel_right = st.columns([1.2, 1.0], gap="large")

with panel_left:
    st.markdown('<div class="retro-card"><strong>🕹️ TICKETING MATRIX REGISTER</strong></div>', unsafe_html=True)
    
    header_cols = st.columns([0.6, 2.2, 1.2, 1.2])
    header_cols.markdown("**TICK**")
    header_cols.markdown("**STOCK (ENG / TICKER)**")
    header_cols.markdown("**ALLOCATION %**")
    header_cols.markdown("**LAST PRICE**")
    
    allocations = {}
    active_ticks = {}
    
    for idx, (key, data) in enumerate(universe.items()):
        row_cols = st.columns([0.6, 2.2, 1.2, 1.2])
        
        active_ticks[key] = row_cols.checkbox("", value=True, key=f"tk_{idx}", label_visibility="collapsed")
        
        if row_cols.button(f"🔗 {data['ticker']} | {data['name']}", key=f"lk_{idx}"):
            st.session_state.focused_stock = key
            st.rerun()
            
        if active_ticks[key]:
            allocations[key] = row_cols.number_input("", min_value=0, max_value=100, value=20, step=5, key=f"al_{idx}", label_visibility="collapsed")
        else:
            allocations[key] = 0
            row_cols.markdown("<span style='color:#8C8C8C;'>MUTED</span>", unsafe_html=True)
            
        row_cols.write(f"{data['currency']} {data['price']:,.2f}")
    
    st.markdown("<br>", unsafe_html=True)
    
    param_col1, param_col2 = st.columns(2)
    entry_year = param_col1.selectbox("🎮 RETRO ENTRY YEAR", options=[2016, 2018, 2020, 2022], index=2)
    
    st.markdown("<div style='padding-top: 10px;'></div>", unsafe_html=True)
    execute_backtest = st.button("🔴 DECIDED 🔴")

with panel_right:
    focus_key = st.session_state.focused_stock
    f_data = universe[focus_key]
    
    st.markdown(f'<div class="retro-card" style="border-color: {NES_RED};">', unsafe_html=True)
    st.markdown(f"<h3 style='margin:0;'>{f_data['ticker']} DATA BLOCK</h3>", unsafe_html=True)
    st.caption(f_data['name'])
    st.markdown("<hr style='margin:10px 0; border:1px solid #000;'/>", unsafe_html=True)
    
    m_col1, m_col2 = st.columns(2)
    m_col1.metric("LAST PRICE", f"{f_data['currency']} {f_data['price']}")
    m_col2.metric("MARKET CAP", f_data['mcap'])
    
    m_col3, m_col4 = st.columns(2)
    m_col3.metric("YTD RETURN", f"{f_data['ytd']*100:+.1f}%")
    m_col4.metric("10Y ANN. RETURN", f"{f_data['ann_10y']*100:.1f}%")
    
    st.markdown("<hr style='margin:10px 0; border:1px dashed #8C8C8C;'/>", unsafe_html=True)
    st.markdown("**FABRICATION NODE ENGINE DATA**")
    
    st.markdown(f"""
    * **Revenue Trend:** QoQ: **{f_data['qoq_rev']*100:+.1f}%** | YoY: **{f_data['yoy_rev']*100:+.1f}%**
    * **Gross Profit Margin:** **{f_data['gross_margin']*100:.1f}%** (Advanced Node efficiency)
    * **Operating Margin:** **{f_data['op_margin']*100:.1f}%** (R&D scaling leverage)
    * **Free Cash Flow:** {f_data['currency']} **{f_data['fcf']}**
    * **Capex Budget:** {f_data['currency']} **{f_data['capex']}**
    * **Yield Rate Efficiency:** **{f_data['yield_rate']*100:.1f}%**
    """)
    
    util = f_data['utilization'] * 100
    util_color = "red" if util < 80 else "green"
    st.markdown(f"**Wafer Fab Utilization:** :{util_color}[**{util:.1f}%**] (Sub-80% drops crush margins)")
    
    # Clean programmatic structural chart lines
    np.random.seed(hash(focus_key) % 500)
    trace = f_data['price'] * np.cumprod(1 + np.random.normal(0.001, 0.025, 60))
    fig_spark = go.Figure(go.Scatter(x=np.arange(60), y=trace, mode='lines', line=dict(color=NES_RED, width=3)))
    fig_spark.update_layout(height=100, margin=dict(l=0, r=0, t=5, b=5), xaxis_visible=False, yaxis_visible=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_spark, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown('</div>', unsafe_html=True)

# 4. GRAPH ENGINE SIMULATOR RUNNERS
if execute_backtest:
    total_alloc = sum(allocations.values())
    
    if total_alloc != 100:
        st.error(f"⚠️ ALLOCATION ERROR: Total weights equal {total_alloc}%. Rebalance entries to equal exactly 100%.")
    else:
        st.markdown("<hr style='border:2px solid #000; margin:25px 0;'/>", unsafe_html=True)
        st.success("🎯 SIMULATION COMPLETE. PLOTTING VISUAL CHARTS LOWER ON PAGE.")
        
        filtered_positions = {k: v for k, v in allocations.items() if v > 0}
        timeline = np.linspace(entry_year, 2026, int((2026 - entry_year) * 12))
        portfolio_curve = np.zeros_like(timeline) + 100.0
        table_summary = []
        
        for asset, weight in filtered_positions.items():
            r = universe[asset]['ann_10y']
            v = universe[asset]['vol']
            
            asset_curve = 100.0 * np.exp((r - 0.5 * v**2) * (timeline - entry_year))
            portfolio_curve += (weight / 100.0) * (asset_curve - 100.0)
            
            final_v = 100000 * (asset_curve[-1] / 100.0)
            table_summary.append({
                "Asset": universe[asset]['ticker'],
                "Weight": f"{weight}%",
                "Principal": "$100,000",
                "Value (2026)": f"${final_v:,.2f}",
                "Growth": f"{(asset_curve[-1] - 100.0):+.1f}%"
            })
            

