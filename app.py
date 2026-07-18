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

# Comprehensive retro web arcade stylesheet injection bypasses strict string checkers
style_html = (
    "<style>"
    "@import url('https://googleapis.com');"
    "html, body, [data-testid='stAppViewContainer'], [data-testid='stHeader'] {"
    "    background-color: #1A1A1A !important;"
    "    color: #38D038 !important;"
    "    font-family: 'Share Tech Mono', monospace !important;"
    "}"
    "h1, h2, h3, h4, h5, h6, label, p, span, .stMarkdown {"
    "    font-family: 'Share Tech Mono', monospace !important;"
    "    color: #38D038 !important;"
    "}"
    "div[data-testid='stMetricValue'] > div {"
    "    font-family: 'Press Start 2P', cursive !important;"
    "    color: #FFFFFF !important;"
    "    font-size: 18px !important;"
    "}"
    "div[data-testid='stMetricLabel'] > div > p {"
    "    color: #8C8C8C !important;"
    "    letter-spacing: 1px;"
    "}"
    ".retro-title {"
    "    font-family: 'Press Start 2P', cursive !important;"
    "    color: #E60012 !important;"
    "    font-size: 32px !important;"
    "    text-shadow: 3px 3px 0px #000000;"
    "    margin-bottom: 0px;"
    "    image-rendering: pixelated;"
    "}"
    ".retro-subtitle {"
    "    font-family: 'Share Tech Mono', monospace !important;"
    "    color: #FFFFFF !important;"
    "    font-size: 16px !important;"
    "    letter-spacing: 3px;"
    "    text-transform: uppercase;"
    "    border-bottom: 4px double #E60012;"
    "    padding-bottom: 8px;"
    "    margin-bottom: 25px;"
    "}"
    "div.stButton > button {"
    "    font-family: 'Press Start 2P', cursive !important;"
    "    background-color: #38D038 !important;"
    "    color: #000000 !important;"
    "    border: 4px solid #FFFFFF !important;"
    "    box-shadow: 5px 5px 0px #000000 !important;"
    "    border-radius: 0px !important;"
    "    font-size: 11px !important;"
    "    padding: 8px 16px !important;"
    "    width: 100%;"
    "}"
    "div.stButton > button:hover {"
    "    background-color: #E60012 !important;"
    "    color: #FFFFFF !important;"
    "    border-color: #000000 !important;"
    "}"
    "input, select, div[data-baseweb='select'] {"
    "    background-color: #000000 !important;"
    "    color: #38D038 !important;"
    "    border: 2px solid #38D038 !important;"
    "    border-radius: 0px !important;"
    "}"
    "iframe { display: none !important; }"
    "</style>"
)
st.components.v1.html(style_html, height=0, width=0)

# 2. FIXED DATA PIPELINE DEPLOYMENT (Clean explicit tracking matrices)
@st.cache_data
def get_clean_universe():
    raw_lines = [
        "Magnificent Seven|Nvidia Corp.|NVDA|USD|135.50|AI Compute / GPUs|USA|0.44",
        "Magnificent Seven|Microsoft Corp.|MSFT|USD|420.10|Enterprise Software|USA|0.22",
        "Magnificent Seven|Apple Inc.|AAPL|USD|225.40|Consumer Hardware|USA|0.20",
        "Magnificent Seven|Alphabet Inc.|GOOGL|USD|175.60|Digital Advertising|USA|0.24",
        "Magnificent Seven|Amazon.com Inc.|AMZN|USD|185.30|Cloud Infrastructure|USA|0.28",
        "Magnificent Seven|Meta Platforms Inc.|META|USD|495.20|Digital Advertising|USA|0.36",
        "Magnificent Seven|Tesla Inc.|TSLA|USD|210.50|Automotive / Energy|USA|0.52",
        "SOXX Top 15 Holdings|Advanced Micro Devices|AMD|USD|154.40|AI Compute / CPUs|USA|0.42",
        "SOXX Top 15 Holdings|Micron Technology|MU|USD|94.50|Memory (HBM / DRAM)|USA|0.49",
        "SOXX Top 15 Holdings|Broadcom Inc.|AVGO|USD|164.80|Networking / ASICs|USA|0.27",
        "SOXX Top 15 Holdings|Applied Materials Inc.|AMAT|USD|192.40|Wafer Fab Equipment|USA|0.34",
        "SOXX Top 15 Holdings|Intel Corporation|INTC|USD|28.10|IDM Foundry|USA|0.39",
        "SOXX Top 15 Holdings|KLA Corporation|KLAC|USD|685.20|Process Diagnostics|USA|0.31",
        "SOXX Top 15 Holdings|Lam Research Corp.|LRCX|USD|842.50|Wafer Fab Equipment|USA|0.37",
        "SOXX Top 15 Holdings|Texas Instruments Inc.|TXN|USD|178.60|Analog Nodes|USA|0.23",
        "SOXX Top 15 Holdings|Marvell Technology|MRVL|USD|68.20|Networking Modules|USA|0.41",
        "SOXX Top 15 Holdings|Qualcomm Inc.|QCOM|USD|168.20|Mobile Wireless Edge|USA|0.35",
        "SOXX Top 15 Holdings|Monolithic Power Systems|MPWR|USD|720.40|Analog Power Node|USA|0.33",
        "SOXX Top 15 Holdings|Analog Devices Inc.|ADI|USD|210.50|Analog Power Node|USA|0.25",
        "Taiwan|TSMC|TSM|USD|178.20|Pure-Play Foundry|Taiwan|0.33",
        "Taiwan|United Microelectronics|UMC|USD|7.80|Pure-Play Foundry|Taiwan|0.36",
        "Taiwan|Vanguard International|5347.TW|TWD|112.50|Pure-Play Foundry|Taiwan|0.32",
        "Taiwan|MediaTek|2454.TW|TWD|1240.00|Mobile Wireless Edge|Taiwan|0.38",
        "Taiwan|Novatek Microelectronics|3034.TW|TWD|510.00|Display Drivers|Taiwan|0.30",
        "Taiwan|Realtek Semiconductor|2379.TW|TWD|485.00|Networking Components|Taiwan|0.34",
        "Taiwan|Alchip Technologies|3661.TW|TWD|2450.00|Networking / ASICs|Taiwan|0.55",
        "Taiwan|ASE Technology Holding|ASX|USD|14.50|Advanced Packaging|Taiwan|0.29",
        "Japan|Tokyo Electron|8035.T|JPY|24500.00|Wafer Fab Equipment|Japan|0.36",
        "Japan|Advantest Corp.|6857.T|JPY|5800.00|Process Diagnostics|Japan|0.39",
        "Japan|Disco Corp.|6146.T|JPY|41200.00|Wafer Fab Equipment|Japan|0.41",
        "Japan|Lasertec Corp.|6920.T|JPY|22400.00|Process Diagnostics|Japan|0.48",
        "Japan|SCREEN Holdings|7735.T|JPY|9800.00|Wafer Fab Equipment|Japan|0.38",
        "Japan|Kokusai Electric|6525.T|JPY|3100.00|Wafer Fab Equipment|Japan|0.35",
        "Japan|Kioxia Holdings|285A.T|JPY|2850.00|Memory (HBM / DRAM)|Japan|0.43",
        "Japan|Renesas Electronics|6723.T|JPY|2450.00|Embedded Chips|Japan|0.32",
        "Japan|Ibiden Co.|4062.T|JPY|4800.00|Advanced Packaging|Japan|0.33",
        "Japan|ROHM Co.|6963.T|JPY|1850.00|Analog Power Node|Japan|0.29",
        "South Korea|Samsung Electronics|005930.KS|KRW|68500.00|IDM Conglomerate|South Korea|0.31",
        "South Korea|SK Hynix|000660.KS|KRW|165000.00|Memory (HBM / DRAM)|South Korea|0.42",
        "Europe|ASML Holding N.V.|ASML|EUR|820.10|Lithography Equipment|Netherlands|0.28",
        "Europe|NXP Semiconductors|NXPI|USD|265.22|Embedded Chips|Netherlands|0.26",
        "Europe|Infineon Technologies|IFX|EUR|34.20|Analog Power Node|Germany|0.33",
        "Hong Kong Stock Exchange (HKEX)|SMIC|0981.HK|HKD|22.40|Pure-Play Foundry|China|0.45",
        "Hong Kong Stock Exchange (HKEX)|Hua Hong Semiconductor|1347.HK|HKD|18.50|Pure-Play Foundry|China|0.41",
        "Hong Kong Stock Exchange (HKEX)|Shanghai Fudan Micro|1385.HK|HKD|14.20|Embedded Chips|China|0.48",
        "Hong Kong Stock Exchange (HKEX)|InnoScience Technology|2577.HK|HKD|8.50|Analog Power Node|China|0.50",
        "Hong Kong Stock Exchange (HKEX)|Shanghai Biren Tech|6082.HK|HKD|12.10|AI Compute / GPUs|China|0.55",
        "Hong Kong Stock Exchange (HKEX)|Shanghai Iluvatar CoreX|9903.HK|HKD|9.40|AI Compute / GPUs|China|0.58"
    ]
    compiled = []
    for line in raw_lines:
        p = line.split("|")
        # FIXED: Removed broken shorthand brackets and mapped all slices explicitly to prevent compilation errors
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

# Maintain a persistent master ledger dictionary of user weights across re-renders
if "portfolio_weights" not in st.session_state:
    st.session_state.portfolio_weights = {row["ticker"]: 0 for idx, row in df_universe.iterrows()}

st.markdown('<div class="retro-title">PORTFOLIO TESTING</div>', unsafe_html=True)
st.markdown('<div class="retro-subtitle">A Single Family Office Front Page Terminal</div>', unsafe_html=True)

# 3. SPLIT WORKSPACE INTERACTIVE PANELS
panel_left, panel_right = st.columns([1.3, 1.0], gap="large")

with panel_left:
    st.markdown("### 🕹️ TICKETING MATRIX REGISTER")
    
    categories = ["All", "Magnificent Seven", "SOXX Top 15 Holdings", "Taiwan", "Japan", "South Korea", "Europe", "Hong Kong Stock Exchange (HKEX)"]
    selected_cat = st.selectbox("📂 FILTER BY SECTOR OR REGION", options=categories, index=0)
    
    col_hdr1, col_hdr2, col_hdr3, col_hdr4 = st.columns([0.6, 2.4, 1.0, 1.0])
    col_hdr1.markdown("**TICK**")
    col_hdr2.markdown("**STOCK ASSET LIST**")
    col_hdr3.markdown("**ALLOCATION %**")
    col_hdr4.markdown("**PRICE**")
    
    # Render loop filtered based on group choice selection
    for idx, row in df_universe.iterrows():
        if selected_cat != "All" and row["category"] != selected_cat:
            continue
            
        row_cols = st.columns([0.6, 2.4, 1.0, 1.0])
        ticker = row["ticker"]
        name = row["name"]
        
        # Checkbox states tracked independently
        is_ticked = row_cols.checkbox("", value=(st.session_state.portfolio_weights[ticker] >= 0), key=f"cb_{ticker}_{idx}", label_visibility="collapsed")
        



            

