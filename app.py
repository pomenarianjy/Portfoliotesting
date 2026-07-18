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
st.set_page_config(layout="wide", page_title="Portfolio Testing Panel")

# Force explicit clean white canvas overrides safely to bypass strict cloud parsers
style_css = """
<style>
html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background-color: #FFFFFF !important;
    color: #000000 !important;
}
h1, h2, h3, h4, h5, h6, label, p, span, .stMarkdown, .stText {
    color: #000000 !important;
}
iframe { display: none !important; }
</style>
"""
st.components.v1.html(style_css, height=0, width=0)

# 2. SEED PIPELINE DATASET GENERATOR
@st.cache_data
def get_clean_universe():
    raw_lines = [
        "Magnificent Seven|Nvidia Corp. (NASDAQ: NVDA)|NVDA|USD|135.50|AI Compute / GPUs|USA|0.44",
        "Magnificent Seven|Microsoft Corp. (NASDAQ: MSFT)|MSFT|USD|420.10|Enterprise Software|USA|0.22",
        "Magnificent Seven|Apple Inc. (NASDAQ: AAPL)|AAPL|USD|225.40|Consumer Hardware|USA|0.20",
        "Magnificent Seven|Alphabet Inc. (NASDAQ: GOOGL)|GOOGL|USD|175.60|Digital Advertising|USA|0.24",
        "Magnificent Seven|Amazon.com Inc. (NASDAQ: AMZN)|AMZN|USD|185.30|Cloud Infrastructure|USA|0.28",
        "Magnificent Seven|Meta Platforms Inc. (NASDAQ: META)|META|USD|495.20|Digital Advertising|USA|0.36",
        "Magnificent Seven|Tesla Inc. (NASDAQ: TSLA)|TSLA|USD|210.50|Automotive / Energy|USA|0.52",
        "SOXX Top 15 Holdings|Advanced Micro Devices, Inc. (NASDAQ: AMD)|AMD|USD|154.40|AI Compute / CPUs|USA|0.42",
        "SOXX Top 15 Holdings|Micron Technology, Inc. (NASDAQ: MU)|MU|USD|94.50|Memory (HBM / DRAM)|USA|0.49",
        "SOXX Top 15 Holdings|Broadcom Inc. (NASDAQ: AVGO)|AVGO|USD|164.80|Networking / ASICs|USA|0.27",
        "SOXX Top 15 Holdings|Applied Materials, Inc. (NASDAQ: AMAT)|AMAT|USD|192.40|Wafer Fab Equipment|USA|0.34",
        "SOXX Top 15 Holdings|Intel Corporation (NASDAQ: INTC)|INTC|USD|28.10|IDM Foundry|USA|0.39",
        "SOXX Top 15 Holdings|KLA Corporation (NASDAQ: KLAC)|KLAC|USD|685.20|Process Diagnostics|USA|0.31",
        "SOXX Top 15 Holdings|Lam Research Corp.|LRCX|USD|842.50|Wafer Fab Equipment|USA|0.37",
        "SOXX Top 15 Holdings|Texas Instruments Inc. (NASDAQ: TXN)|TXN|USD|178.60|Analog Nodes|USA|0.23",
        "SOXX Top 15 Holdings|Marvell Technology, Inc. (NASDAQ: MRVL)|MRVL|USD|68.20|Networking Modules|USA|0.41",
        "SOXX Top 15 Holdings|Qualcomm Inc. (NASDAQ: QCOM)|QCOM|USD|168.20|Mobile Wireless Edge|USA|0.35",
        "SOXX Top 15 Holdings|Monolithic Power Systems, Inc. (NASDAQ: MPWR)|MPWR|USD|720.40|Analog Power Node|USA|0.33",
        "SOXX Top 15 Holdings|Analog Devices, Inc. (NASDAQ: ADI)|ADI|USD|210.50|Analog Power Node|USA|0.25",
        "Taiwan|TSMC (TWSE: 2330 / NYSE: TSM)|TSM|USD|178.20|Pure-Play Foundry|Taiwan|0.33",
        "Taiwan|United Microelectronics Corporation (UMC) (TWSE: 2303)|UMC|USD|7.80|Pure-Play Foundry|Taiwan|0.36",
        "Taiwan|Vanguard International Semiconductor (VIS)|5347.TW|TWD|112.50|Pure-Play Foundry|Taiwan|0.32",
        "Taiwan|MediaTek (TWSE: 2454)|2454.TW|TWD|1240.00|Mobile Wireless Edge|Taiwan|0.38",
        "Taiwan|Novatek Microelectronics (TWSE: 3034)|3034.TW|TWD|510.00|Display Drivers|Taiwan|0.30",
        "Taiwan|Realtek Semiconductor (TWSE: 2379)|2379.TW|TWD|485.00|Networking Components|Taiwan|0.34",
        "Taiwan|Alchip Technologies (TWSE: 3661)|3661.TW|TWD|2450.00|Networking / ASICs|Taiwan|0.55",
        "Taiwan|ASE Technology Holding (TWSE: 3711)|ASX|USD|14.50|Advanced Packaging|Taiwan|0.29",
        "Japan|Tokyo Electron (TYO: 8035)|8035.T|JPY|24500.00|Wafer Fab Equipment|Japan|0.36",
        "Japan|Advantest Corp. (TYO: 6857)|6857.T|JPY|5800.00|Process Diagnostics|Japan|0.39",
        "Japan|Disco Corp. (TYO: 6146)|6146.T|JPY|41200.00|Wafer Fab Equipment|Japan|0.41",
        "Japan|Lasertec Corp. (TYO: 6920)|6920.T|JPY|22400.00|Process Diagnostics|Japan|0.48",
        "Japan|SCREEN Holdings (TYO: 7735)|7735.T|JPY|9800.00|Wafer Fab Equipment|Japan|0.38",
        "Japan|Kokusai Electric (TYO: 6525)|6525.T|JPY|3100.00|Wafer Fab Equipment|Japan|0.35",
        "Japan|Kioxia Holdings (TYO: 285A)|285A.T|JPY|2850.00|Memory (HBM / DRAM)|Japan|0.43",
        "Japan|Renesas Electronics (TYO: 6723)|6723.T|JPY|2450.00|Embedded Chips|Japan|0.32",
        "Japan|Ibiden Co. (TYO: 4062)|4062.T|JPY|4800.00|Advanced Packaging|Japan|0.33",
        "Japan|ROHM Co. (TYO: 6963)|6963.T|JPY|1850.00|Analog Power Node|Japan|0.29",
        "South Korea|Samsung Electronics (KRX: 005930)|005930.KS|KRW|68500.00|IDM Conglomerate|South Korea|0.31",
        "South Korea|SK Hynix (KRX: 000660)|000660.KS|KRW|165000.00|Memory (HBM / DRAM)|South Korea|0.42",
        "Europe|ASML Holding N.V.|ASML|EUR|820.10|Lithography Equipment|Netherlands|0.28",
        "Europe|NXP Semiconductors N.V.|NXPI|USD|265.22|Embedded Chips|Netherlands|0.26",
        "Europe|Infineon Technologies AG (DAX: IFX)|IFX|EUR|34.20|Analog Power Node|Germany|0.33",
        "Hong Kong Stock Exchange (HKEX)|SMIC (HKEX: 0981)|0981.HK|HKD|22.40|Pure-Play Foundry|China|0.45",
        "Hong Kong Stock Exchange (HKEX)|Hua Hong Semiconductor Ltd (HKEX: 1347)|1347.HK|HKD|18.50|Pure-Play Foundry|China|0.41",
        "Hong Kong Stock Exchange (HKEX)|Shanghai Fudan Micro (HKEX: 1385)|1385.HK|HKD|14.20|Embedded Chips|China|0.48",
        "Hong Kong Stock Exchange (HKEX)|InnoScience Technology (HKEX: 2577)|2577.HK|HKD|8.50|Analog Power Node|China|0.50",
        "Hong Kong Stock Exchange (HKEX)|Shanghai Biren Technology (HKEX: 6082)|6082.HK|HKD|12.10|AI Compute / GPUs|China|0.55",
        "Hong Kong Stock Exchange (HKEX)|Shanghai Iluvatar CoreX (HKEX: 9903)|9903.HK|HKD|9.40|AI Compute / GPUs|China|0.58"
    ]
    compiled = []
    for line in raw_lines:
        p = line.split("|")
        # FIXED: Resolved layout tracking indices explicitly to avoid cell string replication issues
        compiled.append([
            p[0], p[1], p[2], p[3], float(p[4]), 
            0.145, 0.282, "420.5B", float(p[7]), p[5], p[6],
            0.08, 0.34, 0.58, 0.32, "8.4B", "3.2B", 0.89, 0.92
        ])
    cols = ["category", "name", "ticker", "currency", "price", "ytd", "ann_10y", "mcap", "vol", "industry", "geo", "qoq_rev", "yoy_rev", "gross_margin", "op_margin", "fcf", "capex", "utilization", "yield_rate"]
    return pd.DataFrame(compiled, columns=cols)

df_universe = get_clean_universe()

if "focused_key" not in st.session_state:
    st.session_state.focused_key = "NVDA"

if "portfolio_weights" not in st.session_state:
    st.session_state.portfolio_weights = {row["ticker"]: 0 for idx, row in df_universe.iterrows()}

st.title("📊 PORTFOLIO TESTING PANEL")

# 3. SPLIT WORKSPACE INTERACTIVE PANELS
panel_left, panel_right = st.columns([1.3, 1.0], gap="large")

with panel_left:
    st.subheader("📂 Register Matrix")
    
    categories = ["All", "Magnificent Seven", "SOXX Top 15 Holdings", "Taiwan", "Japan", "South Korea", "Europe", "Hong Kong Stock Exchange (HKEX)"]
    selected_cat = st.selectbox("Filter Active Assets Region", options=categories, index=0)
    
    ch1, ch2, ch3, ch4 = st.columns([0.6, 2.4, 1.2, 1.2])
    ch1.markdown("**TICK**")
    ch2.markdown("**STOCK ASSET LIST**")
    ch3.markdown("**ALLOCATION %**")
    ch4.markdown("**PRICE**")
    
    allocations = {}
    active_ticks = {}
    
    for idx, row in df_universe.iterrows():
        if selected_cat != "All" and row["category"] != selected_cat:
            continue
            
        r1, r2, r3, r4 = st.columns([0.6, 2.4, 1.2, 1.2])
        ticker = row["ticker"]
        name = row["name"]
        
        active_ticks[ticker] = r1.checkbox("", value=(st.session_state.portfolio_weights[ticker] >= 0), key=f"cb_{ticker}_{idx}", label_visibility="collapsed")
        
        if r2.button(f"🔗 {ticker} | {name[:18]}", key=f"lk_{ticker}_{idx}"):
            st.session_state.focused_key = ticker
            st.rerun()
            
        if active_ticks[ticker]:
            old_val = st.session_state.portfolio_weights[ticker]
            allocations[ticker] = r3.number_input("", min_value=0, max_value=100, value=old_val, step=5, key=f"al_{ticker}_{idx}", label_visibility="collapsed")
            st.session_state.portfolio_weights[ticker] = allocations[ticker]
        else:
            allocations[ticker] = 0
            st.session_state.portfolio_weights[ticker] = 0
            r3.write("MUTED")
            
        r4.write(f"{row['currency']} {row['price']:,.2f}")

    st.write("")
    
    # Real-Time Monitoring Bar
    current_sum = sum(st.session_state.portfolio_weights.values())
    if current_sum == 100:
        st.success(f"🎯 READY TO EXECUTE: TOTAL SUM IS {current_sum}%")
    else:
        st.warning(f"⚠️ COMPLIANCE HOLD: TOTAL SUM IS {current_sum}% / 100%")
        
    current_year = datetime.datetime.now().year
    p_col1, p_col2 = st.columns(2)
    
    entry_year = p_col1.selectbox("🕹️ ENTRY YEAR", options=list(range(2015, current_year)), index=5)
    execute_backtest = p_col2.button("🔴 RUN BACKTEST 🔴")

with panel_right:
    focus_ticker = st.session_state.focused_key
    matched_rows = df_universe[df_universe["ticker"] == focus_ticker]
    
    if len(matched_rows) > 0:
        # FIXED: Mapped the single data item reference explicitly using zero indices to fix the panel type failure [.iloc[0]]
        f_row = matched_rows.iloc[0]
        
        st.subheader(f"📊 Data Profile: {f_row['ticker']}")
        st.text(f"{f_row['name']} ({f_row['category']})")
        st.markdown("---")
        
        met1, met2 = st.columns(2)
        met1.metric("LAST PRICE", f"{f_row['currency']} {f_row['price']}")







            

