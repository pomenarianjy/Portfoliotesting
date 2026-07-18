import streamlit as st
import pandas as pd
import numpy as np
import datetime

# Defensive package verification engine
try:
    import plotly.graph_objects as go
    import plotly.express as px
except ModuleNotFoundError:
    st.error("🔧 ENVIRONMENT ERROR: Add 'plotly' to your requirements.txt file.")
    st.stop()

# 1. CORE VISUAL CANVAS CONTEXT CONFIGURATION
st.set_page_config(layout="wide", page_title="Portfolio Testing", page_icon="🎮")

NES_RED = "#E60012"
NES_BLACK = "#000000"
NES_GRAY = "#8C8C8C"
NES_GREEN = "#38D038"
NES_BG = "#F8F8F8"

# Inject style parameters safely via flat string variables to bypass line parsing glitches
style_html = "<style>@import url('https://googleapis.com'); html, body, [data-testid='stAppViewContainer'] { background-color: #F8F8F8; color: #000000; font-family: 'Share Tech Mono', monospace; } .retro-title { font-family: 'Press Start 2P', cursive; color: #E60012; font-size: 26px; text-shadow: 2px 2px 0px #8C8C8C; margin-bottom: 2px; } .retro-subtitle { font-family: 'Share Tech Mono', monospace; color: #000000; font-size: 14px; text-transform: uppercase; letter-spacing: 2px; border-bottom: 3px solid #E60012; padding-bottom: 6px; margin-bottom: 20px; } iframe { display: none; }</style>"
st.components.v1.html(style_html, height=0, width=0)

# 2. HIGH-DENSITY CHIP EQUIPMENT & DESIGNS REGISTER DATA
@st.cache_data
def get_universe_data():
    return {
        "NVIDIA (NVDA)": {
            "name": "NVIDIA Corporation", "ticker": "NVDA", "currency": "USD", "price": 135.50,
            "ytd": 0.125, "ann_10y": 0.452, "mcap": "3.33T", "vol": 0.44, "industry": "AI Compute / GPUs",
            "geo": "USA", "qoq_rev": 0.15, "yoy_rev": 1.22, "gross_margin": 0.75, "op_margin": 0.61,
            "fcf": "26.4B", "capex": "3.9B", "utilization": 0.96, "yield_rate": 0.89
        },
        "TSMC (TSM)": {
            "name": "Taiwan Semiconductor Mfg Co.", "ticker": "TSM", "currency": "USD", "price": 178.20,
            "ytd": 0.385, "ann_10y": 0.241, "mcap": "924.5B", "vol": 0.33, "industry": "Pure-Play Foundry",
            "geo": "Taiwan", "qoq_rev": 0.09, "yoy_rev": 0.36, "gross_margin": 0.53, "op_margin": 0.42,
            "fcf": "19.1B", "capex": "30.5B", "utilization": 0.93, "yield_rate": 0.87
        },
        "ASML (ASML)": {
            "name": "ASML Holding N.V.", "ticker": "ASML", "currency": "EUR", "price": 820.10,
            "ytd": 0.089, "ann_10y": 0.225, "mcap": "322.0B", "vol": 0.28, "industry": "Lithography Equipment",
            "geo": "Netherlands", "qoq_rev": 0.03, "yoy_rev": 0.11, "gross_margin": 0.50, "op_margin": 0.31,
            "fcf": "6.8B", "capex": "2.5B", "utilization": 0.88, "yield_rate": 0.98
        },
        "AMD (AMD)": {
            "name": "Advanced Micro Devices", "ticker": "AMD", "currency": "USD", "price": 154.40,
            "ytd": -0.042, "ann_10y": 0.315, "mcap": "249.6B", "vol": 0.42, "industry": "AI Compute / CPUs",
            "geo": "USA", "qoq_rev": 0.10, "yoy_rev": 0.18, "gross_margin": 0.48, "op_margin": 0.19,
            "fcf": "3.1B", "capex": "1.2B", "utilization": 0.86, "yield_rate": 0.83
        },
        "Broadcom (AVGO)": {
            "name": "Broadcom Inc.", "ticker": "AVGO", "currency": "USD", "price": 164.80,
            "ytd": 0.221, "ann_10y": 0.294, "mcap": "766.4B", "vol": 0.27, "industry": "Networking / ASICs",
            "geo": "USA", "qoq_rev": 0.05, "yoy_rev": 0.47, "gross_margin": 0.62, "op_margin": 0.44,
            "fcf": "18.2B", "capex": "1.0B", "utilization": 0.84, "yield_rate": 0.81
        }
    }

universe = get_universe_data()

# Lock state defaults cleanly to prevent list indexing mapping failures
if "focused_stock" not in st.session_state:
    st.session_state.focused_stock = list(universe.keys())[0]

st.title("PORTFOLIO TESTING")
st.caption("A SINGLE FAMILY OFFICE FRONT PAGE PANEL")

# 3. SPLIT WORKSPACE INTERACTIVE PANELS
panel_left, panel_right = st.columns([1.3, 1.0], gap="large")

with panel_left:
    st.markdown("### 🕹️ TICKETING MATRIX REGISTER")
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
    current_year = datetime.datetime.now().year
    param_col1, param_col2 = st.columns(2)
    entry_year = param_col1.selectbox("🎮 RETRO ENTRY YEAR", options=list(range(2015, current_year)), index=5)
    st.markdown("<div style='padding-top: 10px;'></div>", unsafe_html=True)
    execute_backtest = st.button("🔴 DECIDED 🔴")

with panel_right:
    focus_key = st.session_state.focused_stock
    f_data = universe[focus_key]
    
    st.markdown(f"### 📊 {f_data['ticker']} DATA BLOCK")
    st.text(f_data['name'])
    
    m_col1, m_col2 = st.columns(2)
    m_col1.metric("LAST PRICE", f"{f_data['currency']} {f_data['price']}")
    m_col2.metric("MARKET CAP", f_data['mcap'])
    
    m_col3, m_col4 = st.columns(2)
    m_col3.metric("YTD RETURN", f"{f_data['ytd']*100:+.1f}%")
    m_col4.metric("10Y ANN. RETURN", f"{f_data['ann_10y']*100:.1f}%")
    
    st.markdown("---")
    st.markdown("**FABRICATION NODE ENGINE DATA**")
    
    # Safe decoupled display blocks that bypass strict python string literal filters
    st.write(f"- **Revenue Trend:** QoQ: **{f_data['qoq_rev']*100:+.1f}%** | YoY: **{f_data['yoy_rev']*100:+.1f}%**")
    st.write(f"- **Gross Profit Margin:** **{f_data['gross_margin']*100:.1f}%** (Pricing power scale factor)")
    st.write(f"- **Operating Margin:** **{f_data['op_margin']*100:.1f}%** (Structural overhead leverage)")
    st.write(f"- **Free Cash Flow:** {f_data['currency']} **{f_data['fcf']}**")
    st.write(f"- **Capex Budget:** {f_data['currency']} **{f_data['capex']}**")
    st.write(f"- **Yield Rate Efficiency:** **{f_data['yield_rate']*100:.1f}%**")
    
    util = f_data['utilization'] * 100
    util_color = "red" if util < 80 else "green"
    st.markdown(f"**Wafer Fab Utilization:** :{util_color}[**{util:.1f}%**] (Sub-80% drops crush margins)")
    
    np.random.seed(hash(focus_key) % 500)
    trace = f_data['price'] * np.cumprod(1 + np.random.normal(0.0005, 0.015, 60))
    fig_spark = go.Figure(go.Scatter(x=np.arange(60), y=trace, mode='lines', line=dict(color=NES_RED, width=3)))
    fig_spark.update_layout(height=100, margin=dict(l=0, r=0, t=5, b=5), xaxis_visible=False, yaxis_visible=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_spark, use_container_width=True, config={'displayModeBar': False})

# 4. BACKTEST RUNTIME CALCULATION MATRIX
if execute_backtest:
    total_alloc = sum(allocations.values())
    if total_alloc != 100:
        st.error(f"⚠️ ALLOCATION ERROR: Total weights equal {total_alloc}%. Rebalance values to hit exactly 100%.")
    else:
        st.markdown("---")
        st.success("🎯 MATRIX COMPILATION INGESTION COMPLETED.")
        filtered_positions = {k: v for k, v in allocations.items() if v > 0}
        
        months_total = int((current_year - entry_year) * 12)
        if months_total <= 0:
            months_total = 12
            
        timeline = np.linspace(entry_year, current_year, months_total)
        portfolio_curve = np.zeros_like(timeline) + 100.0
        table_summary = []
        ind_weights = {}
        geo_weights = {}
        
        for asset, weight in filtered_positions.items():
            r = universe[asset]['ann_10y']
            v = universe[asset]['vol']
            ind = universe[asset]['industry']
            geo = universe[asset]['geo']
            
            ind_weights[ind] = ind_weights.get(ind, 0) + weight
            geo_weights[geo] = geo_weights.get(geo, 0) + weight
            
            asset_curve = 100.0 * np.exp((r - 0.5 * (v**2)) * (timeline - entry_year))
            portfolio_curve += (weight / 100.0) * (asset_curve - 100.0)
            final_v = 100000 * (asset_curve[-1] / 100.0)
            
            table_summary.append({
                "Asset": universe[asset]['ticker'],
                "Allocation Mix": f"{weight}%",
                "Principal Balance": "$100,000",
                f"Terminal Value ({current_year})": f"${final_v:,.2f}",
                "Aggregate Return": f"{(asset_curve[-1] - 100.0):+.1f}%"
            })
            
        chart_df = pd.DataFrame({"Timeline Year": timeline, "Portfolio Value ($)": portfolio_curve * 1000})
        fig_main = px.line(chart_df, x="Timeline Year", y="Portfolio Value ($)", title=f"PORTFOLIO PERFORMANCE HISTORICAL PATHWAY (GROWTH BASE TO {current_year})")
        fig_main.update_layout(plot_bgcolor=NES_BLACK, paper_bgcolor='#FFFFFF', font=dict(family="Share Tech Mono", color=NES_BLACK), xaxis=dict(gridcolor="#333333", showgrid=True), yaxis=dict(gridcolor="#333333", showgrid=True))
        fig_main.update_traces(line_color=NES_GREEN, line_width=4)
        st.plotly_chart(fig_main, use_container_width=True)
        


            

