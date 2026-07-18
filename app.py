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
    "    font-size: 20px !important;"
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
    "    font-size: 12px !important;"
    "    padding: 10px 20px !important;"
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

# 2. SEED SYSTEM INSTITUTIONAL DATASET (ALL 42 RECONSTRUCTED ASSETS DETAILED ACCURATELY)
@st.cache_data
def get_clean_universe():
    raw_assets = [
        # Magnificent Seven
        {"cat": "Magnificent Seven", "name": "Nvidia Corp.", "tk": "NVDA", "cur": "USD", "p": 135.50, "ind": "AI Compute / GPUs", "geo": "USA", "vol": 0.44},
        {"cat": "Magnificent Seven", "name": "Microsoft Corp.", "tk": "MSFT", "cur": "USD", "p": 420.10, "ind": "Enterprise Software", "geo": "USA", "vol": 0.22},
        {"cat": "Magnificent Seven", "name": "Apple Inc.", "tk": "AAPL", "cur": "USD", "p": 225.40, "ind": "Consumer Hardware", "geo": "USA", "vol": 0.20},
        {"cat": "Magnificent Seven", "name": "Alphabet Inc.", "tk": "GOOGL", "cur": "USD", "p": 175.60, "ind": "Digital Advertising", "geo": "USA", "vol": 0.24},
        {"cat": "Magnificent Seven", "name": "Amazon.com Inc.", "tk": "AMZN", "cur": "USD", "p": 185.30, "ind": "Cloud Infrastructure", "geo": "USA", "vol": 0.28},
        {"cat": "Magnificent Seven", "name": "Meta Platforms Inc.", "tk": "META", "cur": "USD", "p": 495.20, "ind": "Digital Advertising", "geo": "USA", "vol": 0.36},
        {"cat": "Magnificent Seven", "name": "Tesla Inc.", "tk": "TSLA", "cur": "USD", "p": 210.50, "ind": "Automotive / Energy", "geo": "USA", "vol": 0.52},
        # SOXX Top 15 Holdings
        {"cat": "SOXX Top 15 Holdings", "name": "Advanced Micro Devices", "tk": "AMD", "cur": "USD", "p": 154.40, "ind": "AI Compute / CPUs", "geo": "USA", "vol": 0.42},
        {"cat": "SOXX Top 15 Holdings", "name": "Micron Technology", "tk": "MU", "cur": "USD", "p": 94.50, "ind": "Memory (HBM / DRAM)", "geo": "USA", "vol": 0.49},
        {"cat": "SOXX Top 15 Holdings", "name": "Broadcom Inc.", "tk": "AVGO", "cur": "USD", "p": 164.80, "ind": "Networking / ASICs", "geo": "USA", "vol": 0.27},
        {"cat": "SOXX Top 15 Holdings", "name": "Applied Materials Inc.", "tk": "AMAT", "cur": "USD", "p": 192.40, "ind": "Wafer Fab Equipment", "geo": "USA", "vol": 0.34},
        {"cat": "SOXX Top 15 Holdings", "name": "Intel Corporation", "tk": "INTC", "cur": "USD", "p": 28.10, "ind": "IDM Foundry", "geo": "USA", "vol": 0.39},
        {"cat": "SOXX Top 15 Holdings", "name": "KLA Corporation", "tk": "KLAC", "cur": "USD", "p": 685.20, "ind": "Process Diagnostics", "geo": "USA", "vol": 0.31},
        {"cat": "SOXX Top 15 Holdings", "name": "Lam Research Corp.", "tk": "LRCX", "cur": "USD", "p": 842.50, "ind": "Wafer Fab Equipment", "geo": "USA", "vol": 0.37},
        {"cat": "SOXX Top 15 Holdings", "name": "Texas Instruments Inc.", "tk": "TXN", "cur": "USD", "p": 178.60, "ind": "Analog Nodes", "geo": "USA", "vol": 0.23},
        {"cat": "SOXX Top 15 Holdings", "name": "Marvell Technology", "tk": "MRVL", "cur": "USD", "p": 68.20, "ind": "Networking Modules", "geo": "USA", "vol": 0.41},
        {"cat": "SOXX Top 15 Holdings", "name": "Qualcomm Inc.", "tk": "QCOM", "cur": "USD", "p": 168.20, "ind": "Mobile Wireless Edge", "geo": "USA", "vol": 0.35},
        {"cat": "SOXX Top 15 Holdings", "name": "Monolithic Power Systems", "tk": "MPWR", "cur": "USD", "p": 720.40, "ind": "Analog Power Node", "geo": "USA", "vol": 0.33},
        {"cat": "SOXX Top 15 Holdings", "name": "Analog Devices Inc.", "tk": "ADI", "cur": "USD", "p": 210.50, "ind": "Analog Power Node", "geo": "USA", "vol": 0.25},
        # Taiwan
        {"cat": "Taiwan", "name": "TSMC", "tk": "TSM", "cur": "USD", "p": 178.20, "ind": "Pure-Play Foundry", "geo": "Taiwan", "vol": 0.33},
        {"cat": "Taiwan", "name": "United Microelectronics", "tk": "UMC", "cur": "USD", "p": 7.80, "ind": "Pure-Play Foundry", "geo": "Taiwan", "vol": 0.36},
        {"cat": "Taiwan", "name": "Vanguard International", "tk": "5347.TW", "cur": "TWD", "p": 112.50, "ind": "Pure-Play Foundry", "geo": "Taiwan", "vol": 0.32},
        {"cat": "Taiwan", "name": "MediaTek", "tk": "2454.TW", "cur": "TWD", "p": 1240.00, "ind": "Mobile Wireless Edge", "geo": "Taiwan", "vol": 0.38},
        {"cat": "Taiwan", "name": "Novatek Microelectronics", "tk": "3034.TW", "cur": "TWD", "p": 510.00, "ind": "Display Drivers", "geo": "Taiwan", "vol": 0.30},
        {"cat": "Taiwan", "name": "Realtek Semiconductor", "tk": "2379.TW", "cur": "TWD", "p": 485.00, "ind": "Networking Components", "geo": "Taiwan", "vol": 0.34},
        {"cat": "Taiwan", "name": "Alchip Technologies", "tk": "3661.TW", "cur": "TWD", "p": 2450.00, "ind": "Networking / ASICs", "geo": "Taiwan", "vol": 0.55},
        {"cat": "Taiwan", "name": "ASE Technology Holding", "tk": "ASX", "cur": "USD", "p": 14.50, "ind": "Advanced Packaging", "geo": "Taiwan", "vol": 0.29},
        # Japan
        {"cat": "Japan", "name": "Tokyo Electron", "tk": "8035.T", "cur": "JPY", "p": 24500.00, "ind": "Wafer Fab Equipment", "geo": "Japan", "vol": 0.36},
        {"cat": "Japan", "name": "Advantest Corp.", "tk": "6857.T", "cur": "JPY", "p": 5800.00, "ind": "Process Diagnostics", "geo": "Japan", "vol": 0.39},
        {"cat": "Japan", "name": "Disco Corp.", "tk": "6146.T", "cur": "JPY", "p": 41200.00, "ind": "Wafer Fab Equipment", "geo": "Japan", "vol": 0.41},
        {"cat": "Japan", "name": "Lasertec Corp.", "tk": "6920.T", "cur": "JPY", "p": 22400.00, "ind": "Process Diagnostics", "geo": "Japan", "vol": 0.48},
        {"cat": "Japan", "name": "SCREEN Holdings", "tk": "7735.T", "cur": "JPY", "p": 9800.00, "ind": "Wafer Fab Equipment", "geo": "Japan", "vol": 0.38},
        {"cat": "Japan", "name": "Kokusai Electric", "tk": "6525.T", "cur": "JPY", "p": 3100.00, "ind": "Wafer Fab Equipment", "geo": "Japan", "vol": 0.35},
        {"cat": "Japan", "name": "Kioxia Holdings", "tk": "285A.T", "cur": "JPY", "p": 2850.00, "ind": "Memory (HBM / DRAM)", "geo": "Japan", "vol": 0.43},
        {"cat": "Japan", "name": "Renesas Electronics", "tk": "6723.T", "cur": "JPY", "p": 2450.00, "ind": "Embedded Chips", "geo": "Japan", "vol": 0.32},
        {"cat": "Japan", "name": "Ibiden Co.", "tk": "4062.T", "cur": "JPY", "p": 4800.00, "ind": "Advanced Packaging", "geo": "Japan", "vol": 0.33},
        {"cat": "Japan", "name": "ROHM Co.", "tk": "6963.T", "cur": "JPY", "p": 1850.00, "ind": "Analog Power Node", "geo": "Japan", "vol": 0.29},
        # South Korea
        {"cat": "South Korea", "name": "Samsung Electronics", "tk": "005930.KS", "cur": "KRW", "p": 68500.00, "ind": "IDM Conglomerate", "geo": "South Korea", "vol": 0.31},
        {"cat": "South Korea", "name": "SK Hynix", "tk": "000660.KS", "cur": "KRW", "p": 165000.00, "ind": "Memory (HBM / DRAM)", "geo": "South Korea", "vol": 0.42},
        # Europe
        {"cat": "Europe", "name": "ASML Holding N.V.", "tk": "ASML", "cur": "EUR", "p": 820.10, "ind": "Lithography Equipment", "geo": "Netherlands", "vol": 0.28},
        {"cat": "Europe", "name": "NXP Semiconductors", "tk": "NXPI", "cur": "USD", "p": 265.22, "ind": "Embedded Chips", "geo": "Netherlands", "vol": 0.26},


            

