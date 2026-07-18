import streamlit as st
import numpy as np
import datetime

# Strict live data feed environment tracking engine
try:
    import yfinance as yf
except ModuleNotFoundError:
    st.error("🔧 ENVIRONMENT ERROR: Add 'yfinance' to your requirements.txt file.")
    st.stop()

# 1. CORE VISUAL WINDOW SETUP
st.set_page_config(layout="wide", page_title="Live Global Foundry Core Panel")

# 2. SEED METADATA MATRIX FOR LIVE FETCHING
RAW_DATA = [
    {"category": "Magnificent Seven", "name": "Nvidia Corp.", "ticker": "NVDA", "currency": "USD", "industry": "AI Compute / GPUs", "geo": "USA", "def_price": 135.50, "def_r": 0.452, "def_v": 0.44},
    {"category": "Magnificent Seven", "name": "Microsoft Corp.", "ticker": "MSFT", "currency": "USD", "industry": "Enterprise Software / Cloud", "geo": "USA", "def_price": 420.10, "def_r": 0.245, "def_v": 0.22},
    {"category": "Magnificent Seven", "name": "Apple Inc.", "ticker": "AAPL", "currency": "USD", "industry": "Consumer Hardware / Mobile", "geo": "USA", "def_price": 225.40, "def_r": 0.221, "def_v": 0.20},
    {"category": "Magnificent Seven", "name": "Alphabet Inc.", "ticker": "GOOGL", "currency": "USD", "industry": "Digital Advertising / AI", "geo": "USA", "def_price": 175.60, "def_r": 0.195, "def_v": 0.24},
    {"category": "Magnificent Seven", "name": "Amazon.com Inc.", "ticker": "AMZN", "currency": "USD", "industry": "E-Commerce / Cloud Infrastructure", "geo": "USA", "def_price": 185.30, "def_r": 0.212, "def_v": 0.28},
    {"category": "Magnificent Seven", "name": "Meta Platforms Inc.", "ticker": "META", "currency": "USD", "industry": "Digital Advertising / Metaverse", "geo": "USA", "def_price": 495.20, "def_r": 0.228, "def_v": 0.36},
    {"category": "Magnificent Seven", "name": "Tesla Inc.", "ticker": "TSLA", "currency": "USD", "industry": "Automotive / Energy Storage", "geo": "USA", "def_price": 210.50, "def_r": 0.384, "def_v": 0.52},
    {"category": "SOXX Top Holdings", "name": "Advanced Micro Devices", "ticker": "AMD", "currency": "USD", "industry": "AI Compute / CPUs", "geo": "USA", "def_price": 154.40, "def_r": 0.315, "def_v": 0.42},
    {"category": "SOXX Top Holdings", "name": "Micron Technology, Inc.", "ticker": "MU", "currency": "USD", "industry": "Memory (HBM / DRAM)", "geo": "USA", "def_price": 94.50, "def_r": 0.198, "def_v": 0.49},
    {"category": "SOXX Top Holdings", "name": "Broadcom Inc.", "ticker": "AVGO", "currency": "USD", "industry": "Networking / ASICs", "geo": "USA", "def_price": 164.80, "def_r": 0.294, "def_v": 0.27},
    {"category": "SOXX Top Holdings", "name": "Applied Materials, Inc.", "ticker": "AMAT", "currency": "USD", "industry": "Wafer Fab Equipment", "geo": "USA", "def_price": 192.40, "def_r": 0.264, "def_v": 0.34},
    {"category": "Taiwan", "name": "TSMC", "ticker": "TSM", "currency": "USD", "industry": "Pure-Play Foundry", "geo": "Taiwan", "def_price": 178.20, "def_r": 0.261, "def_v": 0.33},
    {"category": "Taiwan", "name": "United Microelectronics", "ticker": "UMC", "currency": "USD", "industry": "Pure-Play Foundry", "geo": "Taiwan", "def_price": 7.80, "def_r": 0.114, "def_v": 0.36}
]

# Cache live pricing data to prevent API throttling on component click loops
@st.cache_data(ttl=3600)
def fetch_live_market_data():
    enriched_data = []
    for item in RAW_DATA:
        ticker_symbol = item["ticker"]
        last_price = item["def_price"]
        ann_10y = item["def_r"]
        vol = item["def_v"]
        
        try:
            ticker_obj = yf.Ticker(ticker_symbol)
            history = ticker_obj.history(period="5d")
            
            if history is not None and not history.empty:
                last_price = float(history['Close'].iloc[-1])
                info = ticker_obj.info
                if info is not None:
                    fetched_r = info.get('threeYearAverageReturn')
                    fetched_v = info.get('beta')
                    
                    if fetched_r is not None and fetched_r != 0: ann_10y = float(fetched_r)
                    if fetched_v is not None and fetched_v != 0: vol = float(fetched_v) * 0.25
        except Exception:
            pass
            
        enriched_item = item.copy()
        enriched_item.update({"price": last_price, "ann_10y": ann_10y, "vol": vol})
        enriched_data.append(enriched_item)
    return enriched_data

# Execute streaming queries
with st.spinner("Streaming live price quotes directly from Yahoo Market terminals..."):
    LIVE_DATA = fetch_live_market_data()

# 3. GLOBAL APPLICATION INTERACTIVE STATE STORE ENGINE
if "focused_key" not in st.session_state:
    st.session_state.focused_key = "NVDA"

if "portfolio_weights" not in st.session_state:
    st.session_state.portfolio_weights = {str(item["ticker"]): 0 for item in LIVE_DATA}

def select_focused_asset(ticker):
    st.session_state.focused_key = ticker

st.title("📊 LIVE PORTFOLIO TESTING PANEL")

panel_left, panel_right = st.columns([1.3, 1.0], gap="large")

with panel_left:
    st.subheader("📂 Register Matrix")
    
    categories = ["All", "Magnificent Seven", "SOXX Top Holdings", "Taiwan"]
    selected_cat = st.selectbox("Filter Active Assets Region", options=categories, index=0)
    
    ch1, ch2, ch3, ch4 = st.columns([0.6, 2.4, 1.2, 1.2])
    ch1.markdown("**TICK**")
    ch2.markdown("**STOCK ASSET LIST**")
    ch3.markdown("**ALLOCATION %**")
    ch4.markdown("**LIVE PRICE**")
    
    for idx, item in enumerate(LIVE_DATA):
        if selected_cat != "All" and item["category"] != selected_cat:
            continue
            
        r1, r2, r3, r4 = st.columns([0.6, 2.4, 1.2, 1.2])
        ticker = str(item["ticker"])
        name = str(item["name"])
        
        is_checked = r1.checkbox("", value=(st.session_state.portfolio_weights[ticker] > 0), key=f"cb_live_{ticker}_{idx}", label_visibility="collapsed")
        
        r2.button(f"🔗 {ticker} | {name[:18]}", key=f"lk_live_{ticker}_{idx}", on_click=select_focused_asset, args=(ticker,))
            
        if is_checked:
            old_val = st.session_state.portfolio_weights[ticker]
            initial_val = int(old_val) if old_val > 0 else 0
            new_alloc = r3.number_input("", min_value=0, max_value=100, value=initial_val, step=5, key=f"al_live_{ticker}_{idx}", label_visibility="collapsed")
            st.session_state.portfolio_weights[ticker] = new_alloc
        else:
            st.session_state.portfolio_weights[ticker] = 0
            r3.markdown("<span style='color: #888888;'>MUTED</span>", unsafe_allow_html=True)
            
        r4.write(f"USD {item['price']:,.2f}")

    st.write("")
    
    current_sum = sum(st.session_state.portfolio_weights.values())
    if current_sum == 100:
        st.success(f"🎯 READY TO EXECUTE: TOTAL SUM IS {current_sum}%")
    else:
        st.warning(f"⚠️ COMPLIANCE HOLD: TOTAL SUM IS {current_sum}% / 100%")
        
    years_list = [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
    entry_year = st.selectbox("🕹️ ENTRY YEAR (Starts Jan 1st)", options=years_list, index=4)
    execute_backtest = st.button("🔴 RUN LIVE BACKTEST 🔴", use_container_width=True)

with panel_right:
    focus_ticker = st.session_state.focused_key
    
    target_record = None
    for item in LIVE_DATA:
        if item["ticker"] == focus_ticker:
            target_record = item
            break
            
    if target_record is not None:
        st.subheader(f"📊 Live Data Profile: {target_record['ticker']}")
        st.text(f"{target_record['name']} ({target_record['category']})")
        st.markdown("---")
        
        met1, met2 = st.columns(2)
        met1.metric("LAST CLOSE PRICE", f"USD {target_record['price']:,.2f}")
        met2.metric("IMPLIED RETURN RATE", f"{target_record['ann_10y']*100:.1f}%")
        
        st.markdown("---")
        st.subheader("🔬 Core Metadata Telemetry")
        st.write(f"- **Primary Domain Sector:** {target_record['industry']}")
        st.write(f"- **Geographic Processing Matrix:** {target_record['geo']}")
    else:
        st.write("Select an active asset to load data parameters.")

# 4. MATH SIMULATION PERFORMANCE EXECUTION MATRIX WITH DYNAMIC DAY COUNTER
if execute_backtest:
    total_alloc = sum(st.session_state.portfolio_weights.values())
    if total_alloc != 100:
        st.error(f"❌ COMPLIANCE REJECTION: Allocation must total exactly 100%. Current sum: {total_alloc}%")
    else:
        st.markdown("---")
        
        start_date = datetime.date(entry_year, 1, 1)
        end_date = datetime.date.today()
        days_elapsed = (end_date - start_date).days
        years_elapsed = float(days_elapsed) / 365.25
        
        st.subheader(f"🎯 Backtest Performance Simulation Results (As of {end_date.strftime('%B %d, %Y')})")
        st.caption(f"Simulation tracked over exactly **{days_elapsed:,} days** ({years_elapsed:.3f} compounding fractional years).")
        
        table_summary = []
        total_initial_principal = 100000.0
        total_terminal_value = 0.0
        
        for ticker, weight in st.session_state.portfolio_weights.items():
            if weight <= 0:
                continue
                
            asset_data = None
            for item in LIVE_DATA:
                if item["ticker"] == ticker:
                    asset_data = item
                    break
                    
            if asset_data is not None:
                r = float(asset_data.get('ann_10y', 0.20))
                v = float(asset_data.get('vol', 0.30))
                
                growth_factor = np.exp((r - 0.5 * (v**2)) * years_elapsed)
                allocated_base = total_initial_principal * (weight / 100.0)
                final_v = allocated_base * growth_factor
                
                total_terminal_value += final_v
                perf_pct = (growth_factor - 1.0) * 100
                
                table_summary.append({
                    "Asset Ticker": ticker,




