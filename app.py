import streamlit as st
import pandas as pd
import numpy as np
import datetime

# 1. CORE VISUAL CANVAS CONTEXT CONFIGURATION
st.set_page_config(layout="wide", page_title="Portfolio Testing Panel")

# 2. SEED PIPELINE DATASET GENERATOR
@st.cache_data
def get_clean_universe():
    raw_lines = [
        "Magnificent Seven|Nvidia Corp. (NASDAQ: NVDA)|NVDA|USD|135.50|0.125|0.452|3.33T|0.44|AI Compute / GPUs|USA|0.15|1.22|0.75|0.61|26.4B|3.9B|0.96|0.89",
        "Magnificent Seven|Microsoft Corp. (NASDAQ: MSFT)|MSFT|USD|420.10|0.082|0.245|3.12T|0.22|Enterprise Software / Cloud|USA|0.04|0.16|0.70|0.43|21.0B|14.2B|0.95|0.99",
        "Magnificent Seven|Apple Inc. (NASDAQ: AAPL)|AAPL|USD|225.40|0.061|0.221|3.45T|0.20|Consumer Hardware / Mobile|USA|0.02|0.05|0.46|0.31|23.2B|2.1B|0.92|0.98",
        "Magnificent Seven|Alphabet Inc. (NASDAQ: GOOGL)|GOOGL|USD|175.60|0.114|0.195|2.18T|0.24|Digital Advertising / AI|USA|0.05|0.14|0.57|0.32|15.4B|12.0B|0.90|0.99",
        "Magnificent Seven|Amazon.com Inc. (NASDAQ: AMZN)|AMZN|USD|185.30|0.131|0.212|1.92T|0.28|E-Commerce / Cloud Infrastructure|USA|0.06|0.12|0.41|0.11|17.1B|11.5B|0.88|0.99",
        "Magnificent Seven|Meta Platforms Inc. (NASDAQ: META)|META|USD|495.20|0.242|0.228|1.25T|0.36|Digital Advertising / Metaverse|USA|0.07|0.22|0.81|0.38|12.5B|8.4B|0.94|0.99",
        "Magnificent Seven|Tesla Inc. (NASDAQ: TSLA)|TSLA|USD|210.50|-0.115|0.384|672.0B|0.52|Automotive / Energy Storage|USA|0.02|0.08|0.18|0.06|1.2B|2.8B|0.84|0.95",
        "SOXX Top 15 Holdings|Advanced Micro Devices, Inc. (NASDAQ: AMD)|AMD|USD|154.40|-0.042|0.315|249.6B|0.42|AI Compute / CPUs|USA|0.10|0.18|0.48|0.19|3.1B|1.2B|0.86|0.83",
        "SOXX Top 15 Holdings|Micron Technology, Inc. (NASDAQ: MU)|MU|USD|94.50|0.091|0.198|104.2B|0.49|Memory (HBM / DRAM)|USA|0.22|0.92|0.42|0.21|2.1B|9.2B|0.81|0.76",
        "SOXX Top 15 Holdings|Broadcom Inc. (NASDAQ: AVGO)|AVGO|USD|164.80|0.221|0.294|766.4B|0.27|Networking / ASICs|USA|0.05|0.47|0.62|0.44|18.2B|1.0B|0.84|0.81",
        "SOXX Top 15 Holdings|Applied Materials, Inc. (NASDAQ: AMAT)|AMAT|USD|192.40|0.181|0.264|158.2B|0.34|Wafer Fab Equipment|USA|0.05|0.14|0.47|0.29|5.9B|1.1B|0.89|0.97",
        "SOXX Top 15 Holdings|Intel Corporation (NASDAQ: INTC)|INTC|USD|28.10|-0.154|0.012|119.8B|0.39|IDM / Foundry Transition|USA|-0.01|0.04|0.39|0.08|-3.4B|21.5B|0.74|0.71",
        "SOXX Top 15 Holdings|KLA Corporation (NASDAQ: KLAC)|KLAC|USD|685.20|0.145|0.256|91.2B|0.31|Process Diagnostics Equipment|USA|0.03|0.12|0.61|0.37|3.2B|0.4B|0.90|0.99",
        "SOXX Top 15 Holdings|Lam Research Corp.|LRCX|USD|842.50|0.192|0.284|108.5B|0.37|Wafer Fab Equipment|USA|0.06|0.18|0.48|0.30|4.5B|0.6B|0.88|0.96",
        "SOXX Top 15 Holdings|Texas Instruments Inc. (NASDAQ: TXN)|TXN|USD|178.60|0.054|0.142|162.4B|0.23|Analog Nodes / Embedded Chips|USA|0.01|-0.05|0.59|0.34|5.1B|4.8B|0.78|0.94",
        "SOXX Top 15 Holdings|Marvell Technology, Inc. (NASDAQ: MRVL)|MRVL|USD|68.20|0.112|0.201|58.6B|0.41|Networking / Infrastructure|USA|0.04|0.14|0.42|0.12|1.2B|0.3B|0.83|0.82",
        "SOXX Top 15 Holdings|Qualcomm Inc. (NASDAQ: QCOM)|QCOM|USD|168.20|0.142|0.185|187.6B|0.35|Mobile Wireless Edge|USA|0.04|0.12|0.56|0.24|8.5B|1.4B|0.82|0.93",
        "SOXX Top 15 Holdings|Monolithic Power Systems, Inc. (NASDAQ: MPWR)|MPWR|USD|720.40|0.214|0.312|34.5B|0.33|Analog Nodes / Power Systems|USA|0.05|0.22|0.55|0.26|0.8B|0.1B|0.86|0.95",
        "SOXX Top 15 Holdings|NXP Semiconductors N.V. (NASDAQ: NXPI)|NXPI|USD|265.22|0.227|0.161|68.3B|0.26|Analog Nodes / Embedded Chips|Netherlands|0.02|0.08|0.56|0.28|2.6B|1.0B|0.81|0.94",
        "SOXX Top 15 Holdings|Analog Devices, Inc. (NASDAQ: ADI)|ADI|USD|210.50|0.062|0.164|104.5B|0.25|Analog Nodes / Signal Processing|USA|0.02|-0.02|0.60|0.28|2.9B|0.8B|0.79|0.95",
        "Taiwan|TSMC (TWSE: 2330 / NYSE: TSM)|TSM|USD|178.20|0.385|0.261|924.5B|0.33|Pure-Play Foundry|Taiwan|0.09|0.36|0.53|0.42|19.1B|30.5B|0.93|0.87",
        "Taiwan|United Microelectronics Corporation (UMC) (TWSE: 2303)|UMC|USD|7.80|0.021|0.114|19.5B|0.36|Pure-Play Foundry|Taiwan|0.01|0.06|0.32|0.20|1.4B|3.2B|0.78|0.89"
    ]
    compiled = []
    for line in raw_lines:
        parts = line.split("|")
        # FIXED: Explicit indices used for every column field to prevent unparsed list generation errors
        compiled.append({
            "category": parts[0], "name": parts[1], "ticker": parts[2], "currency": parts[3], "price": float(parts[4]), 
            "ytd": float(parts[5]), "ann_10y": float(parts[6]), "mcap": parts[7], "vol": float(parts[8]), "industry": parts[9], "geo": parts[10],
            "qoq_rev": float(parts[11]), "yoy_rev": float(parts[12]), "gross_margin": float(parts[13]), "op_margin": float(parts[14]), 
            "fcf": parts[15], "capex": parts[16], "utilization": float(parts[17]), "yield_rate": float(parts[18])
        })
    return pd.DataFrame(compiled)

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
    
    categories = ["All", "Magnificent Seven", "SOXX Top 15 Holdings", "Taiwan"]
    selected_cat = st.selectbox("Filter Active Assets Region", options=categories, index=0)
    
    ch1, ch2, ch3, ch4 = st.columns([0.6, 2.4, 1.2, 1.2])
    ch1.markdown("**TICK**")
    ch2.markdown("**STOCK ASSET LIST**")
    ch3.markdown("**ALLOCATION %**")
    ch4.markdown("**PRICE**")
    
    for idx, row in df_universe.iterrows():
        if selected_cat != "All" and row["category"] != selected_cat:
            continue
            
        r1, r2, r3, r4 = st.columns([0.6, 2.4, 1.2, 1.2])
        ticker = row["ticker"]
        name = row["name"]
        
        is_checked = r1.checkbox("", value=(st.session_state.portfolio_weights[ticker] > 0), key=f"cb_{ticker}_{idx}", label_visibility="collapsed")
        
        if r2.button(f"🔗 {ticker} | {name[:18]}", key=f"lk_{ticker}_{idx}"):
            st.session_state.focused_key = ticker
            st.rerun()
            
        if is_checked:
            old_val = st.session_state.portfolio_weights[ticker]
            initial_val = int(old_val) if old_val > 0 else 0
            new_alloc = r3.number_input("", min_value=0, max_value=100, value=initial_val, step=5, key=f"al_{ticker}_{idx}", label_visibility="collapsed")
            st.session_state.portfolio_weights[ticker] = new_alloc
        else:
            st.session_state.portfolio_weights[ticker] = 0
            r3.write("MUTED")
            
        r4.write(f"{row['currency']} {row['price']:,.2f}")

    st.write("")
    
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
        # FIXED: Handled row selection via pure series mapping to remove list lookup bugs down-line
        f_row = matched_rows.iloc[0].to_dict()
        
        st.subheader(f"📊 Data Profile: {f_row['ticker']}")
        st.text(f"{f_row['name']} ({f_row['category']})")
        st.markdown("---")
        
        met1, met2 = st.columns(2)
        met1.metric("LAST PRICE", f"{f_row['currency']} {f_row['price']:,.2f}")
        met2.metric("MARKET CAP", f_row['mcap'])
        
        met3, met4 = st.columns(2)
        met3.metric("YTD RETURN", f"{f_row['ytd']*100:+.1f}%")
        met4.metric("10Y COMP. RATE", f"{f_row['ann_10y']*100:.1f}%")
        
        st.markdown("---")
        st.subheader("🔬 Foundry Fabrication Telemetry")
        
        st.write(f"- **Revenue Growth Trend:** QoQ: **{f_row['qoq_rev']*100:+.1f}%** | YoY: **{f_row['yoy_rev']*100:+.1f}%**")
        st.write(f"- **Gross Profit Margin:** **{f_row['gross_margin']*100:.1f}%**")
        st.write(f"- **Operating Margin:** **{f_row['op_margin']*100:.1f}%**")
        st.write(f"- **Free Cash Flow:** {f_row['currency']} **{f_row['fcf']}**")
        st.write(f"- **Capex Investments:** {f_row['currency']} **{f_row['capex']}**")
        st.write(f"- **Yield Rate Efficiency:** **{f_row['yield_rate']*100:.1f}%**")
        st.write(f"- **Wafer Fab Utilization:** **{f_row['utilization']*100:.1f}%**")
    else:
        st.write("Select an active asset to load data parameters.")

# 4. BACKTEST RUNTIME CALCULATION MATRIX
if execute_backtest:
    total_alloc = sum(st.session_state.portfolio_weights.values())
    if total_alloc != 100:
        st.error(f"❌ COMPLIANCE REJECTION: Allocation must total exactly 100%. Current sum: {total_alloc}%")
    else:
        st.markdown("---")
        st.subheader("🎯 Backtest Performance Simulation Results")
        
        months_total = int((current_year - entry_year) * 12)
        if months_total <= 0:
            months_total = 12
            
        timeline = np.linspace(entry_year, current_year, months_total)
        portfolio_curve = np.zeros_like(timeline)
        table_summary = []
        
        for ticker, weight in st.session_state.portfolio_weights.items():
            if weight <= 0:
                continue
                
            r_rows = df_universe[df_universe["ticker"] == ticker]












            

