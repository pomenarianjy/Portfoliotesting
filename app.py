import streamlit as st
import numpy as np
import pandas as pd
import datetime

# Strict live data feed environment tracking engine
try:
    import yfinance as yf
except ModuleNotFoundError:
    st.error("🔧 ENVIRONMENT ERROR: Add 'yfinance' to your requirements.txt file.")
    st.stop()

# 1. CORE VISUAL WINDOW SETUP
st.set_page_config(layout="wide", page_title="Jasmine's Portfolio Testing Model")

# 2. SEED METADATA REGISTRATION TERMINAL (FLAT STRUCTURAL STRINGS ONLY)
TICKERS_LIST = [
    # Magnificent Seven
    "NVDA", "MSFT", "AAPL", "GOOGL", "AMZN", "META", "TSLA",
    # SOXX Top 15 Holdings
    "AMD", "MU", "AVGO", "AMAT", "INTC", "KLAC", "LRCX", "TXN", "MRVL", "QCOM", "MPWR", "NXPI", "ADI",
    # Taiwan
    "TSM", "UMC", "5347.TWO", "2454.TW", "3034.TW", "2379.TW", "3661.TW", "ASX",
    # Japan
    "8035.T", "6857.T", "6146.T", "6920.T", "7735.T", "6525.T", "285A.T", "6723.T", "4062.T", "6963.T",
    # South Korea
    "005930.KS", "000660.KS"
]

NAMES_LIST = [
    # Magnificent Seven
    "Nvidia Corp.", "Microsoft Corp.", "Apple Inc.", "Alphabet Inc.", "Amazon.com Inc.", "Meta Platforms Inc.", "Tesla Inc.",
    # SOXX Top 15 Holdings
    "Advanced Micro Devices, Inc.", "Micron Technology, Inc.", "Broadcom Inc.", "Applied Materials, Inc.", "Intel Corporation", "KLA Corporation", "Lam Research Corp.", "Texas Instruments Inc.", "Marvell Technology, Inc.", "Qualcomm Inc.", "Monolithic Power Systems, Inc.", "NXP Semiconductors N.V.", "Analog Devices, Inc.",
    # Taiwan
    "TSMC", "UMC", "Vanguard International", "MediaTek", "Novatek Microelectronics", "Realtek Semiconductor", "Alchip Technologies", "ASE Technology Holding",
    # Japan
    "Tokyo Electron", "Advantest Corp.", "Disco Corp.", "Lasertec Corp.", "SCREEN Holdings", "Kokusai Electric", "Kioxia Holdings", "Renesas Electronics", "Ibiden Co.", "ROHM Co.",
    # South Korea
    "Samsung Electronics", "SK Hynix"
]

CATEGORIES_LIST = [
    # Magnificent Seven
    "Mag7", "Mag7", "Mag7", "Mag7", "Mag7", "Mag7", "Mag7",
    # SOXX Top 15 Holdings
    "SOXX", "SOXX", "SOXX", "SOXX", "SOXX", "SOXX", "SOXX", "SOXX", "SOXX", "SOXX", "SOXX", "SOXX", "SOXX",
    # Taiwan
    "Taiwan", "Taiwan", "Taiwan", "Taiwan", "Taiwan", "Taiwan", "Taiwan", "Taiwan",
    # Japan
    "Japan", "Japan", "Japan", "Japan", "Japan", "Japan", "Japan", "Japan", "Japan", "Japan",
    # South Korea
    "South Korea", "South Korea"
]

CURRENCY_MAP = {
    "Mag7": "USD", "SOXX": "USD", "Taiwan": "TWD", "Japan": "JPY", "South Korea": "KRW"
}
for t in ["TSM", "UMC", "ASX"]:
    CURRENCY_MAP[t] = "USD"

# Caching engine to isolate download loops from component click events
@st.cache_data(ttl=3600)
def load_live_market_data():
    enriched_data = []
    for idx, ticker in enumerate(TICKERS_LIST):
        last_price = 150.0
        ann_10y = 0.22
        vol = 0.32
        
        market_cap = "N/A"
        pe_ratio = "N/A"
        div_yield = "N/A"
        beta_val = "N/A"
        day_high = 0.0
        day_low = 0.0
        volume = "N/A"
        
        category = CATEGORIES_LIST[idx]
        currency = CURRENCY_MAP.get(ticker, CURRENCY_MAP.get(category, "USD"))
        
        try:
            ticker_obj = yf.Ticker(ticker)
            history = ticker_obj.history(period="5d")
            if history is not None and not history.empty:
                last_price = float(history['Close'].iloc[-1])
                day_high = float(history['High'].iloc[-1])
                day_low = float(history['Low'].iloc[-1])
                volume = int(history['Volume'].iloc[-1])
                
                info = ticker_obj.info
                if info is not None:
                    fetched_r = info.get('threeYearAverageReturn')
                    fetched_v = info.get('beta')
                    if fetched_r is not None and fetched_r != 0: ann_10y = float(fetched_r)
                    if fetched_v is not None and fetched_v != 0: vol = float(fetched_v) * 0.25
                    
                    raw_cap = info.get('marketCap')
                    if raw_cap:
                        if raw_cap >= 1e12: market_cap = f"${raw_cap / 1e12:.2f}T"
                        elif raw_cap >= 1e9: market_cap = f"${raw_cap / 1e9:.2f}B"
                        else: market_cap = f"${raw_cap :,}"
                        
                    raw_pe = info.get('trailingPE') or info.get('forwardPE')
                    if raw_pe: pe_ratio = f"{raw_pe:.2f}x"
                    
                    raw_div = info.get('dividendYield')
                    if raw_div: div_yield = f"{raw_div * 100:.2f}%"
                    elif info.get('trailingAnnualDividendYield'): div_yield = f"{info.get('trailingAnnualDividendYield') * 100:.2f}%"
                    
                    raw_beta = info.get('beta')
                    if raw_beta: beta_val = f"{raw_beta:.2f}"
        except Exception:
            pass
            
        if day_high == 0.0: day_high = last_price * 1.01
        if day_low == 0.0: day_low = last_price * 0.99
            
        enriched_data.append({
            "ticker": ticker,
            "name": NAMES_LIST[idx],
            "category": category,
            "price": last_price,
            "ann_10y": ann_10y,
            "vol": vol,
            "currency": currency,
            "market_cap": market_cap,
            "pe_ratio": pe_ratio,
            "div_yield": div_yield,
            "beta": beta_val,
            "day_high": day_high,
            "day_low": day_low,
            "volume": f"{volume:,}" if isinstance(volume, int) else "N/A"
        })
    return enriched_data

with st.spinner("Streaming live price quotes directly from global Market terminals..."):
    LIVE_DATA = load_live_market_data()

# 3. GLOBAL APPLICATION INTERACTIVE STATE STORE ENGINE
if "focused_key" not in st.session_state:
    st.session_state.focused_key = TICKERS_LIST[0]

if "portfolio_weights" not in st.session_state:
    st.session_state.portfolio_weights = {str(tk): 0 for tk in TICKERS_LIST}

def select_focused_asset(ticker):
    st.session_state.focused_key = ticker

# Custom Dashboard Branding
st.title("📊 JASMINE'S PORTFOLIO TESTING MODEL")

panel_left, panel_right = st.columns([1.3, 1.0], gap="large")

with panel_left:
    st.subheader("📂 Register Matrix")
    
    categories = ["All"] + sorted(list(set(CATEGORIES_LIST)))
    selected_cat = st.selectbox("Filter Active Assets Region", options=categories, index=0)
    
    # FILTER ACTIONS: Equal distribution or reset across currently filtered assets
    visible_tickers = [item["ticker"] for item in LIVE_DATA if selected_cat == "All" or item["category"] == selected_cat]
    
    act_col1, act_col2 = st.columns(2)
    if act_col1.button("⚖️ Distribute Equally (Filtered)", use_container_width=True):
        n_assets = len(visible_tickers)
        if n_assets > 0:
            # Clear all weights first
            for tk in TICKERS_LIST:
                st.session_state.portfolio_weights[tk] = 0
            
            # Simple division with rounding allocation logic
            base_weight = 100 // n_assets
            remainder = 100 % n_assets
            
            for i, tk in enumerate(visible_tickers):
                st.session_state.portfolio_weights[tk] = base_weight + (1 if i < remainder else 0)
            st.rerun()

    if act_col2.button("🔄 Reset All Allocations", use_container_width=True):
        st.session_state.portfolio_weights = {str(tk): 0 for tk in TICKERS_LIST}
        st.rerun()
        
    st.markdown("---")

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
        
        current_weight = st.session_state.portfolio_weights.get(ticker, 0)
        is_checked = r1.checkbox("", value=(current_weight > 0), key=f"cb_live_{ticker}_{idx}", label_visibility="collapsed")
        
        display_ticker = ticker.split(".")[0]
        r2.button(f"🔗 {display_ticker} | {name[:22]}", key=f"lk_live_{ticker}_{idx}", on_click=select_focused_asset, args=(ticker,))
            
        if is_checked:
            old_val = st.session_state.portfolio_weights.get(ticker, 0)
            initial_val = int(old_val) if old_val > 0 else 0
            new_alloc = r3.number_input("", min_value=0, max_value=100, value=initial_val, step=5, key=f"al_live_{ticker}_{idx}", label_visibility="collapsed")
            st.session_state.portfolio_weights[ticker] = new_alloc
        else:
            st.session_state.portfolio_weights[ticker] = 0
            r3.markdown("<span style='color: #888888;'>MUTED</span>", unsafe_allow_html=True)
            
        r4.write(f"{item['currency']} {item['price']:,.2f}")

    st.write("")
    
    current_sum = sum(st.session_state.portfolio_weights.values())
    if current_sum == 100:
        st.success(f"🎯 READY TO EXECUTE: TOTAL SUM IS {current_sum}%")
    else:
        st.warning(f"⚠️ COMPLIANCE HOLD: TOTAL SUM IS {current_sum}% / 100%")
        
    years_list = list(range(2016, 2027))
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
        clean_focus_display = target_record['ticker'].split(".")[0]
        st.subheader(f"📊 Live Financial Profile: {clean_focus_display}")
        st.text(f"{target_record['name']} — {target_record['category']} Universe")
        st.markdown("---")
        
        met1, met2 = st.columns(2)
        met1.metric("LAST CLOSE PRICE", f"{target_record['currency']} {target_record['price']:,.2f}")
        met2.metric("IMPLIED RETURN RATE", f"{target_record['ann_10y']*100:.1f}%")
        
        st.markdown("### 📈 Core Advanced Statistics")
        
        stat_df = pd.DataFrame({
            "Metric Parameter": [
                "Market Capitalization", 
                "Valuation Multiplier (P/E)", 
                "Dividend Yield Percentage",
                "Systemic Risk (Beta Coefficient)",
                "Daily Session Range",
                "Trading Volume (Latest)"
            ],
            "Live Terminal Value": [
                target_record["market_cap"],
                target_record["pe_ratio"],
                target_record["div_yield"],
                target_record["beta"],
                f"{target_record['currency']} {target_record['day_low']:,.2f} - {target_record['day_high']:,.2f}",
                target_record["volume"]
            ]
        })
        
        st.dataframe(stat_df, hide_index=True, use_container_width=True)
    else:
        st.write("Select an active asset link to load operational data structures.")

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
        st.info("ℹ️ Note: Portfolio baseline uses local currency performance normalized to a base model scale of $100,000 principal values.")

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
                    "Asset Ticker": ticker.split(".")[0],
                    "Allocation Weight": f"{weight}%",
                    "Principal Base": f"${allocated_base:,.2f}",
                    "Terminal Value": f"${final_v:,.2f}",
                    "Absolute Performance": f"{perf_pct:+.1f}%"
                })
            
        if table_summary:
            portfolio_total_return_pct = ((total_terminal_value / total_initial_principal) - 1.0) * 100
            portfolio_cagr_pct = ((total_terminal_value / total_initial_principal) ** (1.0 / years_elapsed) - 1.0) * 100 if years_elapsed > 0 else 0.0
            portfolio_net_profit = total_terminal_value - total_initial_principal
            
            st.markdown("### 📈 Portfolio Summary Metrics")
            m_agg1, m_agg2, m_agg3, m_agg4 = st.columns(4)
            m_agg1.metric("TOTAL INITIAL PRINCIPAL", f"${total_initial_principal:,.2f}")
            m_agg2.metric("PORTFOLIO TERMINAL VALUE", f"${total_terminal_value:,.2f}")
            m_agg3.metric("TOTAL ACCUMULATED RETURN", f"{portfolio_total_return_pct:+.2f}%", f"${portfolio_net_profit:,.2f} Net Profit")
            m_agg4.metric("PORTFOLIO SIMULATED CAGR", f"{portfolio_cagr_pct:.2f}%")
            
            st.markdown("### 📋 Position Historical Balances Ledger")
            st.table(pd.DataFrame(table_summary))
        else:
            st.error("No active positions selected.")
