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
        "Taiwan|United Microelectronics Corporation (UMC) (TWSE: 2303)|UMC|USD|7.80|0.021|0.114|19.5B|0.36|Pure-Play Foundry|Taiwan|0.01|0.06|0.32|0.20|1.4B|3.2B|0.78|0.89",
        "Taiwan|Vanguard International Semiconductor (VIS)|5347.TW|TWD|112.50|0.045|0.095|6.2B|0.32|Pure-Play Foundry|Taiwan|0.02|0.08|0.28|0.16|0.4B|0.8B|0.76|0.91",
        "Taiwan|MediaTek (TWSE: 2454)|2454.TW|TWD|1240.00|0.152|0.184|64.2B|0.38|Mobile Wireless Edge|Taiwan|0.04|0.21|0.47|0.22|3.8B|0.5B|0.88|0.94",
        "Taiwan|Novatek Microelectronics (TWSE: 3034)|3034.TW|TWD|510.00|0.061|0.141|10.4B|0.30|Display Driver ICs|Taiwan|0.02|0.07|0.40|0.18|0.9B|0.1B|0.85|0.93",
        "Taiwan|Realtek Semiconductor (TWSE: 2379)|2379.TW|TWD|485.00|0.084|0.162|8.1B|0.34|Networking / Infrastructure|Taiwan|0.03|0.12|0.43|0.14|0.6B|0.2B|0.86|0.92",
        "Taiwan|Alchip Technologies (TWSE: 3661)|3661.TW|TWD|2450.00|0.321|0.412|5.6B|0.55|Networking / ASICs|Taiwan|0.12|0.64|0.35|0.19|0.3B|0.1B|0.92|0.82",
        "Taiwan|ASE Technology Holding (TWSE: 3711)|ASX|USD|14.50|0.092|0.124|31.4B|0.29|Advanced Node OSAT packaging|Taiwan|0.03|0.11|0.16|0.07|1.8B|2.4B|0.80|0.99",
        "Japan|Tokyo Electron (TYO: 8035)|8035.T|JPY|24500.00|0.112|0.231|78.4B|0.36|Wafer Fab Equipment|Japan|0.06|0.21|0.45|0.27|4.2B|0.9B|0.87|0.96",
        "Japan|Advantest Corp. (TYO: 6857)|6857.T|JPY|5800.00|0.184|0.252|32.6B|0.39|Process Diagnostics Equipment|Japan|0.05|0.18|0.52|0.21|1.4B|0.3B|0.89|0.98",
        "Japan|Disco Corp. (TYO: 6146)|6146.T|JPY|41200.00|0.291|0.342|38.2B|0.41|Wafer Fab Equipment|Japan|0.08|0.31|0.58|0.33|1.9B|0.5B|0.91|0.99",
        "Japan|Lasertec Corp. (TYO: 6920)|6920.T|JPY|22400.00|0.052|0.485|18.4B|0.48|Process Diagnostics Equipment|Japan|0.03|0.15|0.64|0.39|0.9B|0.1B|0.93|0.99",
        "Japan|SCREEN Holdings (TYO: 7735)|7735.T|JPY|9800.00|0.141|0.221|11.2B|0.38|Wafer Fab Equipment|Japan|0.04|0.14|0.44|0.17|0.7B|0.2B|0.85|0.95",
        "Japan|Kokusai Electric (TYO: 6525)|6525.T|JPY|3100.00|0.082|0.165|5.4B|0.35|Wafer Fab Equipment|Japan|0.02|0.09|0.41|0.16|0.3B|0.1B|0.84|0.94",
        "Japan|Kioxia Holdings (TYO: 285A)|285A.T|JPY|2850.00|0.021|0.112|12.4B|0.43|Memory (HBM / DRAM)|Japan|0.05|0.22|0.31|0.08|0.5B|1.9B|0.77|0.78",
        "Japan|Renesas Electronics (TYO: 6723)|6723.T|JPY|2450.00|0.064|0.154|34.1B|0.32|Analog Nodes / Embedded Chips|Japan|0.01|0.04|0.52|0.22|2.1B|0.8B|0.81|0.92",
        "Japan|Ibiden Co. (TYO: 4062)|4062.T|JPY|4800.00|-0.041|0.132|5.1B|0.33|Advanced Node OSAT packaging|Japan|0.02|0.06|0.24|0.10|0.3B|0.6B|0.82|0.98",
        "Japan|ROHM Co. (TYO: 6963)|6963.T|JPY|1850.00|-0.092|0.084|4.8B|0.29|Analog Nodes / Power Systems|Japan|0.01|0.02|0.35|0.09|0.2B|0.7B|0.78|0.93",
        "South Korea|Samsung Electronics (KRX: 005930)|005930.KS|KRW|68500.00|0.054|0.112|362.0B|0.31|IDM Conglomerate|South Korea|0.07|0.28|0.36|0.14|4.8B|38.2B *|0.83|0.79",
        "South Korea|SK Hynix (KRX: 000660)|000660.KS|KRW|165000.00|0.284|0.214|94.2B|0.42|Memory (HBM / DRAM)|South Korea|0.18|0.84|0.41|0.24|2.4B|12.4B|0.88|0.75",
        "Europe|ASML Holding N.V.|ASML|EUR|820.10|0.089|0.225|322.0B|0.28|Lithography Equipment|Netherlands|0.03|0.11|0.50|0.31|6.8B|2.5B|0.88|0.98",
        "Europe|Infineon Technologies AG (DAX: IFX)|IFX|EUR|34.20|0.041|0.145|48.2B|0.33|Analog Nodes / Power Systems|Germany|0.01|0.05|0.43|0.22|1.8B|2.1B|0.79|0.93",
        "Hong Kong Stock Exchange (HKEX)|SMIC (HKEX: 0981)|0981.HK|HKD|22.40|0.142|0.125|28.5B|0.45|Pure-Play Foundry|China|0.05|0.22|0.21|0.11|0.8B|7.5B|0.80|0.74",
        "Hong Kong Stock Exchange (HKEX)|Hua Hong Semiconductor Ltd (HKEX: 1347)|1347.HK|HKD|18.50|0.052|0.091|4.2B|0.41|Pure-Play Foundry|China|0.02|0.11|0.22|0.09|0.3B|2.1B|0.77|0.78",
        "Hong Kong Stock Exchange (HKEX)|Shanghai Fudan Micro (HKEX: 1385)|1385.HK|HKD|14.20|0.021|0.154|1.8B|0.48|Analog Nodes / Embedded Chips|China|0.01|0.06|0.45|0.12|0.1B|0.2B|0.82|0.81",
        "Hong Kong Stock Exchange (HKEX)|InnoScience Technology (HKEX: 2577)|2577.HK|HKD|8.50|0.000|0.050|0.9B|0.50|Analog Nodes / Power Systems|China|0.03|0.15|0.25|-0.05|-0.1B|0.4B|0.71|0.68",
        "Hong Kong Stock Exchange (HKEX)|Shanghai Biren Technology (HKEX: 6082)|6082.HK|HKD|12.10|0.000|0.060|1.5B|0.55|AI Compute / GPUs|China|0.08|0.45|0.30|-0.12|-0.2B|0.3B|0.74|0.62",
        "Hong Kong Stock Exchange (HKEX)|Shanghai Iluvatar CoreX (HKEX: 9903)|9903.HK|HKD|9.40|0.000|0.045|1.1B|0.58|AI Compute / GPUs|China|0.04|0.35|0.28|-0.15|-0.1B|0.2B|0.72|0.60"
    ]
    compiled = []
    for line in raw_lines:
        parts = line.split("|")
        # Ensure trailing markers don't mutate or cut off data definitions
        compiled.append({
            "category": parts[0], "name": parts[1], "ticker": parts[2], "currency": parts[3], "price": float(parts[4]), 
            "ytd": float(parts[5]), "ann_10y": float(parts[6]), "mcap": parts[7], "vol": float(parts[8]), "industry": parts[9], "geo": parts[10],
            "qoq_rev": float(parts[11]), "yoy_rev": float(parts[12]), "gross_margin": float(parts[13]), "op_margin": float(parts[14]), 
            "fcf": parts[15], "capex": parts[16], "utilization": float(parts[17]), "yield_rate": float(parts[18])
        })
    return pd.DataFrame(compiled)

df_universe = get_clean_universe()










            

