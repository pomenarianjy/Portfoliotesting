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

# Safe programmatic structural injection of global theme overrides to bypass strict text parsers
style_html = "<style>@import url('https://googleapis.com'); html, body, [data-testid='stAppViewContainer'] { background-color: #F8F8F8; color: #000000; font-family: 'Share Tech Mono', monospace; } .retro-title { font-family: 'Press Start 2P', cursive; color: #E60012; font-size: 26px; text-shadow: 2px 2px 0px #8C8C8C; margin-bottom: 2px; } .retro-subtitle { font-family: 'Share Tech Mono', monospace; color: #000000; font-size: 14px; text-transform: uppercase; letter-spacing: 2px; border-bottom: 3px solid #E60012; padding-bottom: 6px; margin-bottom: 20px; } iframe { display: none; }</style>"
st.components.v1.html(style_html, height=0, width=0)

# 2. DEFINED SYSTEM DATASET (42 COMPLETE REQUESTED GLOBAL ASSETS)
@st.cache_data
def get_universe_data():
    return {
        # --- Magnificent Seven ---
        "NVIDIA (NVDA)": {"category": "Magnificent Seven", "name": "NVIDIA Corp.", "ticker": "NVDA", "currency": "USD", "price": 135.50, "ytd": 0.125, "ann_10y": 0.452, "mcap": "3.33T", "vol": 0.44, "industry": "AI Compute / GPUs", "geo": "USA", "qoq_rev": 0.15, "yoy_rev": 1.22, "gross_margin": 0.75, "op_margin": 0.61, "fcf": "26.4B", "capex": "3.9B", "utilization": 0.96, "yield_rate": 0.89},
        "Microsoft (MSFT)": {"category": "Magnificent Seven", "name": "Microsoft Corp.", "ticker": "MSFT", "currency": "USD", "price": 420.10, "ytd": 0.082, "ann_10y": 0.245, "mcap": "3.12T", "vol": 0.22, "industry": "Enterprise Software / Cloud", "geo": "USA", "qoq_rev": 0.04, "yoy_rev": 0.16, "gross_margin": 0.70, "op_margin": 0.43, "fcf": "21.0B", "capex": "14.2B", "utilization": 0.95, "yield_rate": 0.99},
        "Apple (AAPL)": {"category": "Magnificent Seven", "name": "Apple Inc.", "ticker": "AAPL", "currency": "USD", "price": 225.40, "ytd": 0.061, "ann_10y": 0.221, "mcap": "3.45T", "vol": 0.20, "industry": "Consumer Hardware / Mobile", "geo": "USA", "qoq_rev": 0.02, "yoy_rev": 0.05, "gross_margin": 0.46, "op_margin": 0.31, "fcf": "23.2B", "capex": "2.1B", "utilization": 0.92, "yield_rate": 0.98},
        "Alphabet (GOOGL)": {"category": "Magnificent Seven", "name": "Alphabet Inc.", "ticker": "GOOGL", "currency": "USD", "price": 175.60, "ytd": 0.114, "ann_10y": 0.195, "mcap": "2.18T", "vol": 0.24, "industry": "Digital Advertising / AI", "geo": "USA", "qoq_rev": 0.05, "yoy_rev": 0.14, "gross_margin": 0.57, "op_margin": 0.32, "fcf": "15.4B", "capex": "12.0B", "utilization": 0.90, "yield_rate": 0.99},
        "Amazon (AMZN)": {"category": "Magnificent Seven", "name": "Amazon.com Inc.", "ticker": "AMZN", "currency": "USD", "price": 185.30, "ytd": 0.131, "ann_10y": 0.212, "mcap": "1.92T", "vol": 0.28, "industry": "E-Commerce / Cloud Infrastructure", "geo": "USA", "qoq_rev": 0.06, "yoy_rev": 0.12, "gross_margin": 0.41, "op_margin": 0.11, "fcf": "17.1B", "capex": "11.5B", "utilization": 0.88, "yield_rate": 0.99},
        "Meta (META)": {"category": "Magnificent Seven", "name": "Meta Platforms Inc.", "ticker": "META", "currency": "USD", "price": 495.20, "ytd": 0.242, "ann_10y": 0.228, "mcap": "1.25T", "vol": 0.36, "industry": "Digital Advertising / Metaverse", "geo": "USA", "qoq_rev": 0.07, "yoy_rev": 0.22, "gross_margin": 0.81, "op_margin": 0.38, "fcf": "12.5B", "capex": "8.4B", "utilization": 0.94, "yield_rate": 0.99},
        "Tesla (TSLA)": {"category": "Magnificent Seven", "name": "Tesla Inc.", "ticker": "TSLA", "currency": "USD", "price": 210.50, "ytd": -0.115, "ann_10y": 0.384, "mcap": "672.0B", "vol": 0.52, "industry": "Automotive / Energy Storage", "geo": "USA", "qoq_rev": 0.02, "yoy_rev": 0.08, "gross_margin": 0.18, "op_margin": 0.06, "fcf": "1.2B", "capex": "2.8B", "utilization": 0.84, "yield_rate": 0.95},

        # --- SOXX Top 15 Holdings ---
        "AMD (AMD)": {"category": "SOXX Top 15 Holdings", "name": "Advanced Micro Devices, Inc.", "ticker": "AMD", "currency": "USD", "price": 154.40, "ytd": -0.042, "ann_10y": 0.315, "mcap": "249.6B", "vol": 0.42, "industry": "AI Compute / CPUs", "geo": "USA", "qoq_rev": 0.10, "yoy_rev": 0.18, "gross_margin": 0.48, "op_margin": 0.19, "fcf": "3.1B", "capex": "1.2B", "utilization": 0.86, "yield_rate": 0.83},
        "Micron (MU)": {"category": "SOXX Top 15 Holdings", "name": "Micron Technology, Inc.", "ticker": "MU", "currency": "USD", "price": 94.50, "ytd": 0.091, "ann_10y": 0.198, "mcap": "104.2B", "vol": 0.49, "industry": "Memory (HBM / DRAM)", "geo": "USA", "qoq_rev": 0.22, "yoy_rev": 0.92, "gross_margin": 0.42, "op_margin": 0.21, "fcf": "2.1B", "capex": "9.2B", "utilization": 0.81, "yield_rate": 0.76},
        "Broadcom (AVGO)": {"category": "SOXX Top 15 Holdings", "name": "Broadcom Inc.", "ticker": "AVGO", "currency": "USD", "price": 164.80, "ytd": 0.221, "ann_10y": 0.294, "mcap": "766.4B", "vol": 0.27, "industry": "Networking / ASICs", "geo": "USA", "qoq_rev": 0.05, "yoy_rev": 0.47, "gross_margin": 0.62, "op_margin": 0.44, "fcf": "18.2B", "capex": "1.0B", "utilization": 0.84, "yield_rate": 0.81},
        "Applied Materials (AMAT)": {"category": "SOXX Top 15 Holdings", "name": "Applied Materials, Inc.", "ticker": "AMAT", "currency": "USD", "price": 192.40, "ytd": 0.181, "ann_10y": 0.264, "mcap": "158.2B", "vol": 0.34, "industry": "Wafer Fab Equipment", "geo": "USA", "qoq_rev": 0.05, "yoy_rev": 0.14, "gross_margin": 0.47, "op_margin": 0.29, "fcf": "5.9B", "capex": "1.1B", "utilization": 0.89, "yield_rate": 0.97},
        "Intel (INTC)": {"category": "SOXX Top 15 Holdings", "name": "Intel Corporation", "ticker": "INTC", "currency": "USD", "price": 28.10, "ytd": -0.154, "ann_10y": 0.012, "mcap": "119.8B", "vol": 0.39, "industry": "IDM / Foundry Transition", "geo": "USA", "qoq_rev": -0.01, "yoy_rev": 0.04, "gross_margin": 0.39, "op_margin": 0.08, "fcf": "-3.4B", "capex": "21.5B", "utilization": 0.74, "yield_rate": 0.71},
        "KLA Corp (KLAC)": {"category": "SOXX Top 15 Holdings", "name": "KLA Corporation", "ticker": "KLAC", "currency": "USD", "price": 685.20, "ytd": 0.145, "ann_10y": 0.256, "mcap": "91.2B", "vol": 0.31, "industry": "Process Diagnostics Equipment", "geo": "USA", "qoq_rev": 0.03, "yoy_rev": 0.12, "gross_margin": 0.61, "op_margin": 0.37, "fcf": "3.2B", "capex": "0.4B", "utilization": 0.90, "yield_rate": 0.99},
        "Lam Research (LRCX)": {"category": "SOXX Top 15 Holdings", "name": "Lam Research Corp.", "ticker": "LRCX", "currency": "USD", "price": 842.50, "ytd": 0.192, "ann_10y": 0.284, "mcap": "108.5B", "vol": 0.37, "industry": "Wafer Fab Equipment", "geo": "USA", "qoq_rev": 0.06, "yoy_rev": 0.18, "gross_margin": 0.48, "op_margin": 0.30, "fcf": "4.5B", "capex": "0.6B", "utilization": 0.88, "yield_rate": 0.96},
        "Texas Instruments (TXN)": {"category": "SOXX Top 15 Holdings", "name": "Texas Instruments Inc.", "ticker": "TXN", "currency": "USD", "price": 178.60, "ytd": 0.054, "ann_10y": 0.142, "mcap": "162.4B", "vol": 0.23, "industry": "Analog Nodes / Embedded Chips", "geo": "USA", "qoq_rev": 0.01, "yoy_rev": -0.05, "gross_margin": 0.59, "op_margin": 0.34, "fcf": "5.1B", "capex": "4.8B", "utilization": 0.78, "yield_rate": 0.94},
        "Marvell (MRVL)": {"category": "SOXX Top 15 Holdings", "name": "Marvell Technology, Inc.", "ticker": "MRVL", "currency": "USD", "price": 68.20, "ytd": 0.112, "ann_10y": 0.201, "mcap": "58.6B", "vol": 0.41, "industry": "Networking / Infrastructure", "geo": "USA", "qoq_rev": 0.04, "yoy_rev": 0.14, "gross_margin": 0.42, "op_margin": 0.12, "fcf": "1.2B", "capex": "0.3B", "utilization": 0.83, "yield_rate": 0.82},
        "Qualcomm (QCOM)": {"category": "SOXX Top 15 Holdings", "name": "Qualcomm Inc.", "ticker": "QCOM", "currency": "USD", "price": 168.20, "ytd": 0.142, "ann_10y": 0.185, "mcap": "187.6B", "vol": 0.35, "industry": "Mobile Wireless Edge", "geo": "USA", "qoq_rev": 0.04, "yoy_rev": 0.12, "gross_margin": 0.56, "op_margin": 0.24, "fcf": "8.5B", "capex": "1.4B", "utilization": 0.82, "yield_rate": 0.93},
        "Monolithic Power (MPWR)": {"category": "SOXX Top 15 Holdings", "name": "Monolithic Power Systems, Inc.", "ticker": "MPWR", "currency": "USD", "price": 720.40, "ytd": 0.214, "ann_10y": 0.312, "mcap": "34.5B", "vol": 0.33, "industry": "Analog Nodes / Power Systems", "geo": "USA", "qoq_rev": 0.05, "yoy_rev": 0.22, "gross_margin": 0.55, "op_margin": 0.26, "fcf": "0.8B", "capex": "0.1B", "utilization": 0.86, "yield_rate": 0.95},
        "Analog Devices (ADI)": {"category": "SOXX Top 15 Holdings", "name": "Analog Devices, Inc.", "ticker": "ADI", "currency": "USD", "price": 210.50, "ytd": 0.062, "ann_10y": 0.164, "mcap": "104.5B", "vol": 0.25, "industry": "Analog Nodes / Signal Processing", "geo": "USA", "qoq_rev": 0.02, "yoy_rev": -0.02, "gross_margin": 0.60, "op_margin": 0.28, "fcf": "2.9B", "capex": "0.8B", "utilization": 0.79, "yield_rate": 0.95},

        # --- Taiwan ---
        "TSMC (TSM)": {"category": "Taiwan", "name": "Taiwan Semiconductor Manufacturing Co.", "ticker": "TSM", "currency": "USD", "price": 178.20, "ytd": 0.385, "ann_10y": 0.261, "mcap": "924.5B", "vol": 0.33, "industry": "Pure-Play Foundry", "geo": "Taiwan", "qoq_rev": 0.09, "yoy_rev": 0.36, "gross_margin": 0.53, "op_margin": 0.42, "fcf": "19.1B", "capex": "30.5B", "utilization": 0.93, "yield_rate": 0.87},



        


            

