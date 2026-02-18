import streamlit as st
import pandas as pd
import requests
from io import StringIO
import concurrent.futures
import time

# Page config
st.set_page_config(
    page_title="TrackMaster Pro",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# PREMIUM CLASSY THEME - UPGRADED
# =============================================================================

st.markdown("""
<style>
    /* ===== IMPORTS ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* ===== ROOT VARIABLES ===== */
    :root {
        --bg-primary: #0a0a0f;
        --bg-secondary: #12121a;
        --bg-card: #16161f;
        --bg-elevated: #1a1a24;
        --border-subtle: #232330;
        --border-medium: #2a2a3a;
        --text-primary: #f4f4f8;
        --text-secondary: #9898b0;
        --text-muted: #6b6b82;
        --accent-blue: #6366f1;
        --accent-purple: #a855f7;
        --accent-pink: #ec4899;
        --accent-cyan: #22d3ee;
        --accent-green: #10b981;
        --accent-orange: #f97316;
        --glow-blue: rgba(99, 102, 241, 0.4);
        --glow-purple: rgba(168, 85, 247, 0.4);
        --glow-green: rgba(16, 185, 129, 0.4);
    }
    
    /* ===== MAIN BACKGROUND ===== */
    .stApp {
        background: 
            radial-gradient(ellipse at 0% 0%, rgba(99, 102, 241, 0.08) 0%, transparent 50%),
            radial-gradient(ellipse at 100% 0%, rgba(168, 85, 247, 0.06) 0%, transparent 50%),
            radial-gradient(ellipse at 50% 100%, rgba(236, 72, 153, 0.04) 0%, transparent 50%),
            linear-gradient(180deg, #0a0a0f 0%, #0d0d14 50%, #0a0a0f 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d0d14 0%, #0a0a0f 100%);
        border-right: 1px solid var(--border-subtle);
    }
    
    [data-testid="stSidebar"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 150px;
        background: linear-gradient(180deg, rgba(99, 102, 241, 0.08) 0%, transparent 100%);
        pointer-events: none;
    }
    
    [data-testid="stSidebar"] .stRadio > label {
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stSidebar"] .stRadio > div {
        gap: 4px;
    }
    
    [data-testid="stSidebar"] .stRadio > div > label {
        background: transparent !important;
        border: 1px solid transparent !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
        margin: 2px 0 !important;
        transition: all 0.25s ease !important;
        color: var(--text-secondary) !important;
    }
    
    [data-testid="stSidebar"] .stRadio > div > label:hover {
        background: rgba(99, 102, 241, 0.1) !important;
        border-color: rgba(99, 102, 241, 0.3) !important;
        color: var(--text-primary) !important;
    }
    
    [data-testid="stSidebar"] .stRadio > div > label[data-checked="true"] {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(168, 85, 247, 0.15) 100%) !important;
        border-color: rgba(99, 102, 241, 0.4) !important;
        color: var(--text-primary) !important;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.2) !important;
    }
    
    /* ===== PREMIUM HEADER ===== */
    .premium-header {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 40%, #ec4899 70%, #f97316 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: -1px;
        line-height: 1.1;
        padding-bottom: 8px;
        animation: shimmer 3s ease-in-out infinite;
    }
    
    @keyframes shimmer {
        0%, 100% { filter: brightness(1); }
        50% { filter: brightness(1.2); }
    }
    
    .subtitle {
        color: var(--text-secondary);
        font-size: 1.05rem;
        font-weight: 400;
        letter-spacing: 0.3px;
    }
    
    /* ===== LIVE BADGE ===== */
    .live-badge {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 10px 20px;
        border-radius: 25px;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.4), 0 0 40px rgba(16, 185, 129, 0.2);
        animation: pulse-glow 2s ease-in-out infinite;
        display: inline-block;
    }
    
    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 4px 20px rgba(16, 185, 129, 0.4), 0 0 40px rgba(16, 185, 129, 0.2); }
        50% { box-shadow: 0 4px 30px rgba(16, 185, 129, 0.6), 0 0 60px rgba(16, 185, 129, 0.3); }
    }
    
    /* ===== GLASSMORPHISM CARDS ===== */
    .result-header-box {
        background: linear-gradient(145deg, rgba(22, 22, 31, 0.8) 0%, rgba(18, 18, 26, 0.9) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 16px;
        padding: 20px 24px;
        margin-bottom: 16px;
        border: 1px solid var(--border-subtle);
        border-left: 4px solid;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.03);
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .result-header-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 100%;
        background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.02) 50%, transparent 100%);
        pointer-events: none;
    }
    
    .result-header-box:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.05);
        border-color: var(--border-medium);
    }
    
    .result-header-ecl { 
        border-left-color: #f97316; 
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), 0 0 40px rgba(249, 115, 22, 0.1);
    }
    .result-header-ge { 
        border-left-color: #6366f1; 
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), 0 0 40px rgba(99, 102, 241, 0.1);
    }
    .result-header-apx { 
        border-left-color: #a855f7; 
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), 0 0 40px rgba(168, 85, 247, 0.1);
    }
    .result-header-kerry { 
        border-left-color: #10b981; 
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), 0 0 40px rgba(16, 185, 129, 0.1);
    }
    
    .result-header-ecl:hover { box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4), 0 0 60px rgba(249, 115, 22, 0.15); }
    .result-header-ge:hover { box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4), 0 0 60px rgba(99, 102, 241, 0.15); }
    .result-header-apx:hover { box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4), 0 0 60px rgba(168, 85, 247, 0.15); }
    .result-header-kerry:hover { box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4), 0 0 60px rgba(16, 185, 129, 0.15); }
    
    /* ===== PARTNER STYLING ===== */
    .partner-name {
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .partner-ecl { color: #f97316; text-shadow: 0 0 20px rgba(249, 115, 22, 0.5); }
    .partner-ge { color: #6366f1; text-shadow: 0 0 20px rgba(99, 102, 241, 0.5); }
    .partner-apx { color: #a855f7; text-shadow: 0 0 20px rgba(168, 85, 247, 0.5); }
    .partner-kerry { color: #10b981; text-shadow: 0 0 20px rgba(16, 185, 129, 0.5); }
    
    .source-name {
        color: var(--text-primary);
        font-size: 1.2rem;
        font-weight: 600;
        margin: 8px 0;
    }
    
    .order-id-display {
        color: var(--text-muted);
        font-size: 0.88rem;
        font-family: 'SF Mono', 'Consolas', monospace;
    }
    
    /* ===== SECTION TITLES ===== */
    .section-title {
        color: var(--accent-blue);
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2.5px;
        margin: 24px 0 14px 0;
        padding-bottom: 10px;
        border-bottom: 1px solid var(--border-subtle);
        position: relative;
    }
    
    .section-title::after {
        content: '';
        position: absolute;
        bottom: -1px;
        left: 0;
        width: 40px;
        height: 2px;
        background: linear-gradient(90deg, var(--accent-blue) 0%, var(--accent-purple) 100%);
        border-radius: 2px;
    }
    
    /* ===== FIELD STYLING ===== */
    .field-label {
        color: var(--text-muted);
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 6px;
    }
    
    .field-value {
        color: var(--text-primary);
        font-size: 0.95rem;
        font-weight: 500;
        background: linear-gradient(145deg, var(--bg-elevated) 0%, var(--bg-card) 100%);
        padding: 12px 16px;
        border-radius: 10px;
        margin-top: 4px;
        border: 1px solid var(--border-subtle);
        transition: all 0.25s ease;
    }
    
    .field-value:hover {
        border-color: var(--border-medium);
        transform: translateY(-1px);
    }
    
    .field-value-empty {
        color: var(--text-muted);
        font-style: italic;
        background: var(--bg-secondary);
        border-style: dashed;
    }
    
    .field-value-highlight {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(99, 102, 241, 0.05) 100%);
        color: #818cf8;
        font-weight: 600;
        border: 1px solid rgba(99, 102, 241, 0.3);
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.1);
    }
    
    .field-value-tracking {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(16, 185, 129, 0.05) 100%);
        color: #34d399;
        font-family: 'SF Mono', 'Consolas', monospace;
        font-size: 0.9rem;
        border: 1px solid rgba(16, 185, 129, 0.3);
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.1);
    }
    
    .field-value-status {
        background: linear-gradient(135deg, rgba(236, 72, 153, 0.15) 0%, rgba(168, 85, 247, 0.1) 100%);
        color: #f472b6;
        font-weight: 600;
        border: 1px solid rgba(236, 72, 153, 0.3);
        box-shadow: 0 4px 20px rgba(236, 72, 153, 0.15);
        animation: status-pulse 2s ease-in-out infinite;
    }
    
    @keyframes status-pulse {
        0%, 100% { box-shadow: 0 4px 20px rgba(236, 72, 153, 0.15); }
        50% { box-shadow: 0 4px 30px rgba(236, 72, 153, 0.25); }
    }
    
    /* ===== METRICS ===== */
    [data-testid="stMetricValue"] {
        color: var(--text-primary) !important;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        font-size: 0.75rem !important;
    }
    
    /* ===== INPUT FIELDS ===== */
    .stTextInput > div > div > input {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        padding: 14px 18px !important;
        font-size: 0.95rem !important;
        transition: all 0.25s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--accent-blue) !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2), 0 4px 20px rgba(99, 102, 241, 0.15) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: var(--text-muted) !important;
    }
    
    /* ===== BUTTONS ===== */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-blue) 0%, var(--accent-purple) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 28px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.3px !important;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.3), 0 0 40px rgba(99, 102, 241, 0.1) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(99, 102, 241, 0.4), 0 0 60px rgba(99, 102, 241, 0.2) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* ===== SUCCESS/ERROR/INFO ===== */
    .stSuccess {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(16, 185, 129, 0.05) 100%) !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
        border-radius: 12px !important;
        color: #34d399 !important;
    }
    
    .stError {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(239, 68, 68, 0.05) 100%) !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
        border-radius: 12px !important;
    }
    
    .stInfo {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(99, 102, 241, 0.05) 100%) !important;
        border: 1px solid rgba(99, 102, 241, 0.2) !important;
        border-radius: 12px !important;
    }
    
    /* ===== EXPANDER ===== */
    .streamlit-expanderHeader {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        font-weight: 500 !important;
    }
    
    .streamlit-expanderContent {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-subtle) !important;
        border-top: none !important;
        border-radius: 0 0 12px 12px !important;
    }
    
    /* ===== DATAFRAME ===== */
    .stDataFrame {
        border: 1px solid var(--border-subtle) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }
    
    /* ===== DIVIDER ===== */
    hr {
        border-color: var(--border-subtle) !important;
        margin: 24px 0 !important;
    }
    
    /* ===== CAPTION ===== */
    .stCaption {
        color: var(--text-muted) !important;
    }
    
    /* ===== CUSTOM SCROLLBAR ===== */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-primary);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border-medium);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--text-muted);
    }
    
    /* ===== PARTNER STAT CARDS ===== */
    .partner-card {
        background: linear-gradient(145deg, var(--bg-card) 0%, var(--bg-secondary) 100%);
        border-radius: 16px;
        padding: 20px;
        border: 1px solid var(--border-subtle);
        transition: all 0.3s ease;
    }
    
    .partner-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# DATA SOURCES
# =============================================================================

DATA_SOURCES = {
    "ECL QC Center": {
        "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSCiZ1MdPMyVAzBqmBmp3Ch8sfefOp_kfPk2RSfMv3bxRD_qccuwaoM7WTVsieKJbA3y3DF41tUxb3T/pub?gid=0&single=true&output=csv",
        "order_col": "Fleek ID",
        "partner": "ECL",
        "type": "QC Center",
        "icon": "🟠"
    },
    "ECL Zone": {
        "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSCiZ1MdPMyVAzBqmBmp3Ch8sfefOp_kfPk2RSfMv3bxRD_qccuwaoM7WTVsieKJbA3y3DF41tUxb3T/pub?gid=928309568&single=true&output=csv",
        "order_col": 0,
        "partner": "ECL",
        "type": "Zone",
        "icon": "🟠"
    },
    "GE QC Center": {
        "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQjCPd8bUpx59Sit8gMMXjVKhIFA_f-W9Q4mkBSWulOTg4RGahcVXSD4xZiYBAcAH6eO40aEQ9IEEXj/pub?gid=710036753&single=true&output=csv",
        "order_col": "Order Num",
        "partner": "GE",
        "type": "QC Center",
        "icon": "🔵"
    },
    "GE Zone": {
        "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQjCPd8bUpx59Sit8gMMXjVKhIFA_f-W9Q4mkBSWulOTg4RGahcVXSD4xZiYBAcAH6eO40aEQ9IEEXj/pub?gid=10726393&single=true&output=csv",
        "order_col": 0,
        "partner": "GE",
        "type": "Zone",
        "icon": "🔵"
    },
    "APX": {
        "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRDEzAMUwnFZ7aoThGoMERtxxsll2kfEaSpa9ksXIx6sqbdMncts6Go2d5mKKabepbNXDSoeaUlk-mP/pub?gid=0&single=true&output=csv",
        "order_col": "Fleek ID",
        "partner": "APX",
        "type": "",
        "icon": "🟣"
    },
    "Kerry": {
        "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vTZyLyZpVJz9sV5eT4Srwo_KZGnYggpRZkm2ILLYPQKSpTKkWfP9G5759h247O4QEflKCzlQauYsLKI/pub?gid=0&single=true&output=csv",
        "order_col": "_Order",
        "partner": "Kerry",
        "type": "",
        "icon": "🟢"
    }
}

# =============================================================================
# DISPLAY FIELDS CONFIG - PIECES REMOVED
# =============================================================================

DISPLAY_FIELDS = {
    "📋 Order Information": [
        {"label": "Order Number", "aliases": ["order#", "order", "fleek id", "_order", "order no", "order no.", "order num"], "type": "highlight"},
        {"label": "Handover Date", "aliases": ["date", "fleek handover date", "airport handover date", "handover date", "ge entry date"], "type": "normal"},
        {"label": "Service", "aliases": ["services", "service", "partner", "3pl"], "type": "normal"},
        {"label": "QC Status", "aliases": ["qc status", "qc_status", "status"], "type": "normal"},
    ],
    "📦 Shipment Details": [
        {"label": "Boxes", "aliases": ["box_count", "boxes", "box count", "no of boxes", "n.o of boxes"], "type": "normal"},
        {"label": "Weight (kg)", "aliases": ["weight_kgs", "weight (kg)", "weight", "order net weight", "chargeable weight"], "type": "normal"},
        # REMOVED: Pieces field
    ],
    "🚚 Tracking & Delivery": [
        {"label": "AWB", "aliases": ["airway_bill", "awb", "hawb", "mawb", "apx awb number", "kerry awb number", "ge awb"], "type": "highlight"},
        {"label": "Tracking ID", "aliases": ["courier_tracking_ids", "tracking id", "tracking_id", "tracking", "ge comment / tracking"], "type": "tracking"},
        {"label": "Courier", "aliases": ["courier_service", "courier", "carrier"], "type": "normal"},
    ],
    "👤 Customer Info": [
        {"label": "Customer Name", "aliases": ["consignee", "customer name", "customer_name", "customer", "name"], "type": "normal"},
        {"label": "Destination", "aliases": ["destination", "country", "city"], "type": "normal"},
    ],
    "📡 Live Status": [
        {"label": "Live Status", "aliases": ["live_status"], "type": "status"},
    ],
}

# =============================================================================
# DATA LOADING
# =============================================================================

def fetch_single_source(source_name):
    try:
        config = DATA_SOURCES[source_name]
        response = requests.get(config["url"], timeout=120)
        df = pd.read_csv(StringIO(response.text))
        order_col = config["order_col"]
        if isinstance(order_col, int):
            order_col = df.columns[order_col]
        if order_col in df.columns:
            df["_search_col"] = df[order_col].astype(str).str.lower().str.strip()
        return source_name, df, order_col, None
    except Exception as e:
        return source_name, pd.DataFrame(), None, str(e)

def load_all_data():
    data, errors = {}, []
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        futures = [executor.submit(fetch_single_source, name) for name in DATA_SOURCES.keys()]
        for future in concurrent.futures.as_completed(futures):
            source_name, df, order_col, error = future.result()
            data[source_name] = {"df": df, "order_col": order_col}
            if error:
                errors.append(f"{source_name}: {error}")
    return data, errors

def initialize_data():
    if "data_loaded" not in st.session_state:
        st.session_state.all_data, st.session_state.load_errors = load_all_data()
        st.session_state.data_loaded = True
        st.session_state.total_rows = sum(len(d["df"]) for d in st.session_state.all_data.values())

# =============================================================================
# LIVE STATUS FROM KERRY (FOR ALL ORDERS)
# =============================================================================

def get_live_status_from_kerry(order_id):
    """Fetch live status from Kerry sheet for ANY order"""
    kerry_data = st.session_state.all_data.get("Kerry", {})
    df = kerry_data.get("df", pd.DataFrame())
    
    if df.empty or "_search_col" not in df.columns:
        return None
    
    search_term = order_id.lower().strip()
    matches = df[df["_search_col"] == search_term]
    
    if matches.empty:
        return None
    
    row = matches.iloc[0]
    status_aliases = ["latest status", "latest_status", "live status", "current status", "status update", "delivery status", "status"]
    
    for col in df.columns:
        if col.lower().strip() in status_aliases:
            val = row.get(col)
            if pd.notna(val) and str(val).strip() and str(val).lower() not in ['nan', 'none', 'n/a', '-']:
                return str(val).strip()
    
    return None

# =============================================================================
# SEARCH FUNCTIONS
# =============================================================================

def instant_search(order_ids):
    results = []
    for order_id in order_ids:
        search_term = order_id.lower().strip()
        if not search_term:
            continue
        for source_name, source_data in st.session_state.all_data.items():
            df = source_data["df"]
            if df.empty or "_search_col" not in df.columns:
                continue
            matches = df[df["_search_col"] == search_term]
            for _, row in matches.iterrows():
                config = DATA_SOURCES[source_name]
                row_data = row.to_dict()
                
                # Fetch live status from Kerry for ALL orders
                live_status = get_live_status_from_kerry(order_id)
                if live_status:
                    row_data["live_status"] = live_status
                
                results.append({
                    "source": source_name,
                    "partner": config["partner"],
                    "type": config["type"],
                    "icon": config["icon"],
                    "order_id": order_id,
                    "data": row_data
                })
    return results

def is_valid(val):
    if val is None:
        return False
    s = str(val).lower().strip()
    return s not in ['', 'nan', 'none', 'n/a', '#n/a', 'na', '-', 'null', 'nat']

def get_field_value(data, aliases):
    for key, val in data.items():
        if key.lower().strip() in [a.lower() for a in aliases]:
            if is_valid(val):
                return str(val)
    return None

def get_partner_counts():
    counts = {"ECL": 0, "GE": 0, "APX": 0, "Kerry": 0}
    for name, data in st.session_state.all_data.items():
        partner = DATA_SOURCES[name]["partner"]
        counts[partner] += len(data["df"])
    return counts

# =============================================================================
# UI COMPONENTS
# =============================================================================

def render_result_card(result):
    partner = result["partner"]
    source_type = result["type"]
    source_name = result["source"]
    icon = result["icon"]
    data = result["data"]
    order_id = result["order_id"]
    
    st.markdown(f"""
    <div class="result-header-box result-header-{partner.lower()}">
        <div class="partner-name partner-{partner.lower()}">{icon} {partner}</div>
        <div class="source-name">{source_name}</div>
        <div class="order-id-display">Order: {order_id}</div>
    </div>
    """, unsafe_allow_html=True)
    
    for section_name, fields in DISPLAY_FIELDS.items():
        has_values = any(get_field_value(data, f["aliases"]) for f in fields)
        
        if section_name == "📡 Live Status" and not has_values:
            continue
        
        st.markdown(f"<div class='section-title'>{section_name}</div>", unsafe_allow_html=True)
        
        cols = st.columns(2)
        
        for i, field in enumerate(fields):
            value = get_field_value(data, field["aliases"])
            col_idx = i % 2
            
            with cols[col_idx]:
                st.markdown(f"<div class='field-label'>{field['label']}</div>", unsafe_allow_html=True)
                
                if value:
                    if field["type"] == "highlight":
                        st.markdown(f"<div class='field-value field-value-highlight'>{value}</div>", unsafe_allow_html=True)
                    elif field["type"] == "tracking":
                        st.markdown(f"<div class='field-value field-value-tracking'>{value}</div>", unsafe_allow_html=True)
                    elif field["type"] == "status":
                        st.markdown(f"<div class='field-value field-value-status'>📡 {value}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div class='field-value'>{value}</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='field-value field-value-empty'>—</div>", unsafe_allow_html=True)
    
    st.markdown("---")

def render_sidebar():
    with st.sidebar:
        st.markdown("### 🚀 Navigation")
        page = st.radio(
            "View",
            ["🔍 Global Search", "🟠 ECL QC Center", "🟠 ECL Zone", "🔵 GE QC Center", "🔵 GE Zone", "🟣 APX", "🟢 Kerry"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        if st.session_state.get("data_loaded"):
            sources_ok = sum(1 for d in st.session_state.all_data.values() if not d["df"].empty)
            st.success(f"✅ {st.session_state.total_rows:,} rows loaded")
            st.caption(f"{sources_ok}/6 sources active")
        
        st.markdown("---")
        
        if st.button("🔄 Reload Data", use_container_width=True):
            if "data_loaded" in st.session_state:
                del st.session_state.data_loaded
            st.rerun()
        
        if st.session_state.get("load_errors"):
            with st.expander("⚠️ Warnings"):
                for err in st.session_state.load_errors:
                    st.warning(err)
        
        return page

def search_page():
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown('<p class="premium-header">🔎 TrackMaster Pro</p>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Logistics Tracking Intelligence Dashboard</p>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<br>', unsafe_allow_html=True)
        st.markdown('<span class="live-badge">🟢 Live</span>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("#### 🔍 Search Orders")
    
    col1, col2 = st.columns([5, 1])
    
    with col1:
        search_input = st.text_input(
            "Search",
            placeholder="Enter order ID (e.g., 122129_34, 122054_98)",
            label_visibility="collapsed"
        )
    
    with col2:
        search_clicked = st.button("Search", use_container_width=True, type="primary")
    
    st.caption("💡 Multiple orders: separate with comma or space | ⚡ Instant search | 📊 6 data sources")
    
    st.markdown("---")
    
    if search_input:
        import re
        order_ids = [x.strip() for x in re.split(r'[\n,\t\s]+', search_input) if x.strip()]
        
        if order_ids:
            start = time.time()
            results = instant_search(order_ids)
            search_time = (time.time() - start) * 1000
            
            if results:
                sources_found = list(set(r["source"] for r in results))
                partners_found = list(set(r["partner"] for r in results))
                
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Results", len(results))
                col2.metric("Orders", len(order_ids))
                col3.metric("Sources", len(sources_found))
                col4.metric("Speed", f"{search_time:.0f}ms")
                
                st.markdown("---")
                st.caption(f"📍 Found in: {', '.join(sources_found)}")
                st.markdown("")
                
                for result in results:
                    render_result_card(result)
            else:
                st.error(f"❌ No results found for: {', '.join(order_ids)}")
                st.info("💡 Check order ID format or try a different ID")
    
    else:
        st.markdown("#### 📦 Connected Data Sources")
        
        counts = get_partner_counts()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("### 🟠 ECL")
            st.metric("Orders", f"{counts['ECL']:,}")
            st.caption("QC Center + Zone")
        
        with col2:
            st.markdown("### 🔵 GE")
            st.metric("Orders", f"{counts['GE']:,}")
            st.caption("QC Center + Zone")
        
        with col3:
            st.markdown("### 🟣 APX")
            st.metric("Orders", f"{counts['APX']:,}")
        
        with col4:
            st.markdown("### 🟢 Kerry")
            st.metric("Orders", f"{counts['Kerry']:,}")
            st.caption("+ Live Status")
        
        st.markdown("---")
        
        st.markdown("#### 📊 Source Breakdown")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            for name in ["ECL QC Center", "ECL Zone"]:
                df = st.session_state.all_data.get(name, {}).get("df", pd.DataFrame())
                st.caption(f"🟠 {name}: {len(df):,} rows")
        
        with col2:
            for name in ["GE QC Center", "GE Zone"]:
                df = st.session_state.all_data.get(name, {}).get("df", pd.DataFrame())
                st.caption(f"🔵 {name}: {len(df):,} rows")
        
        with col3:
            for name in ["APX", "Kerry"]:
                df = st.session_state.all_data.get(name, {}).get("df", pd.DataFrame())
                icon = "🟣" if name == "APX" else "🟢"
                st.caption(f"{icon} {name}: {len(df):,} rows")
        
        st.markdown("---")
        
        st.markdown("#### 🕐 Recent Searches")
        st.info("Your recent searches will appear here. Start by searching an order ID above!")

def data_page(source_name):
    config = DATA_SOURCES[source_name]
    
    st.markdown(f"## {config['icon']} {source_name}")
    
    if config["type"]:
        st.caption(f"Partner: {config['partner']} | Type: {config['type']}")
    else:
        st.caption(f"Partner: {config['partner']}")
    
    source_data = st.session_state.all_data.get(source_name, {})
    df = source_data.get("df", pd.DataFrame())
    
    if df.empty:
        st.error("No data available")
        return
    
    col1, col2, col3 = st.columns(3)
    col1.metric("📦 Total Rows", f"{len(df):,}")
    col2.metric("📊 Columns", len(df.columns))
    col3.metric("🏢 Partner", config["partner"])
    
    st.markdown("---")
    
    filter_text = st.text_input("🔍 Filter data...", key=f"filter_{source_name}")
    
    display_df = df.drop(columns=["_search_col"], errors="ignore")
    
    if filter_text:
        mask = display_df.astype(str).apply(
            lambda x: x.str.contains(filter_text, case=False, na=False)
        ).any(axis=1)
        display_df = display_df[mask]
    
    st.dataframe(display_df, use_container_width=True, height=500)
    
    st.download_button(
        "📥 Download CSV",
        display_df.to_csv(index=False),
        f"{source_name.replace(' ', '_')}.csv",
        "text/csv",
        use_container_width=True
    )

# =============================================================================
# MAIN
# =============================================================================

def main():
    if "data_loaded" not in st.session_state:
        st.markdown('<p class="premium-header">🔎 TrackMaster Pro</p>', unsafe_allow_html=True)
        
        with st.spinner("🔄 Loading all data sources..."):
            initialize_data()
        
        st.rerun()
    
    page = render_sidebar()
    
    page_map = {
        "🔍 Global Search": search_page,
        "🟠 ECL QC Center": lambda: data_page("ECL QC Center"),
        "🟠 ECL Zone": lambda: data_page("ECL Zone"),
        "🔵 GE QC Center": lambda: data_page("GE QC Center"),
        "🔵 GE Zone": lambda: data_page("GE Zone"),
        "🟣 APX": lambda: data_page("APX"),
        "🟢 Kerry": lambda: data_page("Kerry"),
    }
    
    page_map.get(page, search_page)()

if __name__ == "__main__":
    main()
