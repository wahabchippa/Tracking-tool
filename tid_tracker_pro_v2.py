import streamlit as st
import pandas as pd
import requests
from io import StringIO
import concurrent.futures
import time
import re
from datetime import datetime, timedelta

st.set_page_config(
    page_title="TrackMaster Pro",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# THEME
# =============================================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    .stApp {
        background: linear-gradient(180deg, #0a0a0f 0%, #0f0f15 50%, #0a0a0f 100%);
        font-family: 'Inter', sans-serif;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0a12 0%, #05050a 100%);
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    
    /* HERO */
    .hero-container { text-align: center; padding: 30px 20px 20px 20px; }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
    }
    
    .hero-subtitle { font-size: 0.9rem; color: #666; margin-bottom: 20px; }
    
    /* STATS CARDS */
    .stats-container {
        display: flex;
        gap: 12px;
        margin-bottom: 20px;
    }
    .stat-card {
        flex: 1;
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 16px;
        text-align: center;
    }
    .stat-card:hover { border-color: rgba(255,255,255,0.1); }
    .stat-icon { font-size: 1.5rem; margin-bottom: 4px; }
    .stat-value { font-size: 1.5rem; font-weight: 700; color: #6366f1; }
    .stat-value-orange { color: #f97316; }
    .stat-value-green { color: #10b981; }
    .stat-value-purple { color: #a855f7; }
    .stat-value-blue { color: #6366f1; }
    .stat-label { font-size: 0.7rem; color: #666; text-transform: uppercase; letter-spacing: 1px; }
    
    /* SEARCH BOX */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 10px !important;
        color: #fff !important;
        padding: 12px 16px !important;
        font-size: 0.95rem !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: rgba(99, 102, 241, 0.5) !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.1) !important;
    }
    .stTextInput > div > div > input::placeholder { color: #555 !important; }
    
    /* BUTTONS */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
    }
    .stButton > button:hover { transform: translateY(-2px) !important; }
    
    /* PARTNER CARDS */
    .partner-card {
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 16px;
        text-align: center;
    }
    .partner-card:hover { border-color: rgba(255,255,255,0.1); }
    
    .partner-icon { font-size: 1.5rem; margin-bottom: 6px; }
    .partner-name { font-size: 0.85rem; font-weight: 600; color: #fff; }
    .partner-count { font-size: 1.3rem; font-weight: 700; margin: 4px 0; }
    .partner-count-ecl { color: #f97316; }
    .partner-count-ge { color: #6366f1; }
    .partner-count-apx { color: #a855f7; }
    .partner-count-kerry { color: #10b981; }
    .partner-label { font-size: 0.7rem; color: #555; }
    
    /* RESULT CARDS */
    .result-card {
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        border-left: 3px solid;
    }
    .result-card-ecl { border-left-color: #f97316; }
    .result-card-ge { border-left-color: #6366f1; }
    .result-card-apx { border-left-color: #a855f7; }
    .result-card-kerry { border-left-color: #10b981; }
    
    .result-partner { font-size: 0.65rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }
    .result-partner-ecl { color: #f97316; }
    .result-partner-ge { color: #6366f1; }
    .result-partner-apx { color: #a855f7; }
    .result-partner-kerry { color: #10b981; }
    .result-source { font-size: 1rem; font-weight: 600; color: #fff; margin: 2px 0; }
    .result-order { font-size: 0.8rem; color: #666; font-family: monospace; }
    
    /* SECTION & FIELDS */
    .section-title {
        font-size: 0.65rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #6366f1;
        margin: 16px 0 8px 0;
        padding-bottom: 6px;
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    
    .field-label { font-size: 0.65rem; font-weight: 600; text-transform: uppercase; color: #555; margin-bottom: 2px; }
    .field-value {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 6px;
        padding: 8px 12px;
        color: #ddd;
        font-size: 0.85rem;
        margin-top: 2px;
    }
    .field-value-empty { color: #444; font-style: italic; }
    .field-value-highlight {
        background: rgba(99, 102, 241, 0.1);
        border-color: rgba(99, 102, 241, 0.2);
        color: #818cf8;
        font-weight: 600;
    }
    .field-value-tracking {
        background: rgba(16, 185, 129, 0.1);
        border-color: rgba(16, 185, 129, 0.2);
        color: #34d399;
        font-family: monospace;
    }
    .field-value-status {
        background: rgba(236, 72, 153, 0.1);
        border-color: rgba(236, 72, 153, 0.2);
        color: #f472b6;
        font-weight: 600;
    }
    
    [data-testid="stMetricValue"] { color: #fff !important; font-size: 1.2rem !important; }
    [data-testid="stMetricLabel"] { color: #666 !important; font-size: 0.7rem !important; }
    
    .stSuccess, .stError, .stInfo { border-radius: 8px !important; }
    .search-hint { text-align: center; color: #444; font-size: 0.75rem; margin-top: 8px; }
    hr { border-color: rgba(255,255,255,0.05) !important; margin: 16px 0 !important; }
    
    /* DATE PICKER */
    .stDateInput > div > div > input {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 8px !important;
        color: #fff !important;
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

KERRY_STATUS_TAB_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTZyLyZpVJz9sV5eT4Srwo_KZGnYggpRZkm2ILLYPQKSpTKkWfP9G5759h247O4QEflKCzlQauYsLKI/pub?gid=2121564686&single=true&output=csv"

# =============================================================================
# DISPLAY FIELDS
# =============================================================================

DISPLAY_FIELDS = {
    "📡 Live Status": [
        {"label": "Latest Status", "aliases": ["_live_status_from_kerry", "latest_status", "status", "current_status"], "type": "status"},
    ],
    "📋 Order Information": [
        {"label": "Order Number", "aliases": ["order#", "order", "fleek id", "_order", "order no", "order num", "order_num", "order number", "ordernumber", "fleek_id", "fleekid"], "type": "highlight"},
        {"label": "Handover Date", "aliases": ["date", "fleek handover date", "airport handover date", "handover date", "ge entry date", "handover_date"], "type": "normal"},
        {"label": "Service", "aliases": ["services", "service", "partner", "3pl", "sea / air", "sea/air"], "type": "normal"},
        {"label": "QC Status", "aliases": ["qc status", "qc_status", "qcstatus"], "type": "normal"},
    ],
    "📦 Shipment Details": [
        {"label": "Boxes", "aliases": ["box_count", "boxes", "box count", "no of boxes", "n.o of boxes", "no. of boxes", "boxcount", "total_boxes"], "type": "normal"},
        {"label": "Weight (kg)", "aliases": ["weight_kgs", "weight (kg)", "weight", "order net weight", "chargeable weight", "order's net weight (kg)", "weight_kg", "weightkg", "total_weight", "net_weight", "gross_weight", "wt", "wt.", "wt (kg)", "weight(kg)"], "type": "normal"},
    ],
    "🚚 Tracking & Delivery": [
        {"label": "AWB", "aliases": ["airway_bill", "awb", "hawb", "mawb", "apx awb number", "kerry awb number", "ge awb", "awb_number", "awbnumber"], "type": "highlight"},
        {"label": "Tracking ID", "aliases": ["courier_tracking_ids", "tracking id", "tracking_id", "tracking", "ge comment / tracking", "trackingid", "tracking_number"], "type": "tracking"},
        {"label": "Courier", "aliases": ["courier_service", "courier", "carrier", "courier_name"], "type": "normal"},
    ],
    "👤 Customer Info": [
        {"label": "Customer Name", "aliases": ["consignee", "customer name", "customer_name", "customer", "name", "cust_name", "custname"], "type": "normal"},
        {"label": "Destination", "aliases": ["destination", "country", "city", "dest", "destination_city"], "type": "normal"},
    ],
}

# =============================================================================
# DATA LOADING
# =============================================================================

def fetch_single_source(source_name):
    try:
        config = DATA_SOURCES[source_name]
        response = requests.get(config["url"], timeout=120)
        response.raise_for_status()
        df = pd.read_csv(StringIO(response.text))
        
        order_col = config["order_col"]
        if isinstance(order_col, int):
            order_col = df.columns[order_col] if order_col < len(df.columns) else None
        
        return source_name, df, order_col, None
    except Exception as e:
        return source_name, pd.DataFrame(), None, str(e)

def fetch_kerry_status_tab():
    try:
        response = requests.get(KERRY_STATUS_TAB_URL, timeout=120)
        response.raise_for_status()
        df = pd.read_csv(StringIO(response.text))
        return df, None
    except Exception as e:
        return pd.DataFrame(), str(e)

def load_all_data():
    data, errors = {}, []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=7) as executor:
        futures = {executor.submit(fetch_single_source, name): name for name in DATA_SOURCES.keys()}
        status_future = executor.submit(fetch_kerry_status_tab)
        
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            source_name, df, order_col, error = result
            data[source_name] = {"df": df, "order_col": order_col}
            if error:
                errors.append(f"{source_name}: {error}")
        
        status_df, status_error = status_future.result()
        data["_kerry_status_tab"] = {"df": status_df}
        if status_error:
            errors.append(f"Kerry Status Tab: {status_error}")
    
    return data, errors

def initialize_data():
    if "data_loaded" not in st.session_state:
        st.session_state.all_data, st.session_state.load_errors = load_all_data()
        st.session_state.data_loaded = True
        st.session_state.total_rows = sum(
            len(d["df"]) for name, d in st.session_state.all_data.items() 
            if name != "_kerry_status_tab"
        )

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_latest_status_from_kerry(order_id):
    try:
        status_data = st.session_state.all_data.get("_kerry_status_tab", {})
        df = status_data.get("df", pd.DataFrame())
        
        if df.empty or "fleek_id" not in df.columns:
            return None
        
        search_term = str(order_id).lower().strip()
        df_search = df["fleek_id"].astype(str).str.lower().str.strip()
        matches = df[df_search == search_term]
        
        if matches.empty:
            return None
        
        if "latest_status" in df.columns:
            val = matches.iloc[0].get("latest_status")
            if pd.notna(val) and str(val).strip():
                return str(val).strip()
        
        return None
    except:
        return None

def is_valid(val):
    if val is None:
        return False
    s = str(val).lower().strip()
    return s not in ['', 'nan', 'none', 'n/a', '#n/a', 'na', '-', 'null', 'nat', 'not applicable']

def get_field_value(data, aliases):
    for key, val in data.items():
        key_lower = key.lower().strip()
        for alias in aliases:
            if key_lower == alias.lower().strip():
                if is_valid(val):
                    return str(val)
    
    for key, val in data.items():
        key_lower = key.lower().strip().replace(" ", "").replace("_", "")
        for alias in aliases:
            alias_clean = alias.lower().strip().replace(" ", "").replace("_", "")
            if key_lower == alias_clean or alias_clean in key_lower or key_lower in alias_clean:
                if is_valid(val):
                    return str(val)
    
    return None

def get_partner_counts():
    counts = {"ECL": 0, "GE": 0, "APX": 0, "Kerry": 0}
    for name, data in st.session_state.all_data.items():
        if name == "_kerry_status_tab":
            continue
        partner = DATA_SOURCES[name]["partner"]
        counts[partner] += len(data["df"])
    return counts

def find_date_column(df):
    """Find the date column in dataframe - IMPROVED"""
    date_keywords = [
        "date", "handover", "entry", "created", "timestamp", 
        "fleek handover", "airport handover", "ge entry"
    ]
    
    for col in df.columns:
        col_lower = col.lower().strip()
        for keyword in date_keywords:
            if keyword in col_lower:
                return col
    
    # Fallback: check first few columns for date-like data
    for col in df.columns[:10]:
        try:
            sample = df[col].dropna().head(5)
            if len(sample) > 0:
                # Check if looks like date
                sample_str = str(sample.iloc[0])
                if any(c in sample_str for c in ['/', '-']) and len(sample_str) >= 8:
                    pd.to_datetime(sample, errors='coerce')
                    return col
        except:
            continue
    
    return None

def smart_parse_date(date_series):
    """Smart date parsing with multiple format attempts"""
    if date_series.empty:
        return pd.Series(dtype='datetime64[ns]')
    
    # Try pandas auto-detect first
    try:
        parsed = pd.to_datetime(date_series, errors='coerce', dayfirst=True)
        if parsed.notna().sum() > len(date_series) * 0.5:  # At least 50% success
            return parsed
    except:
        pass
    
    # Try specific formats
    formats_to_try = [
        "%d/%m/%Y",      # 17/02/2026
        "%d-%m-%Y",      # 17-02-2026
        "%Y-%m-%d",      # 2026-02-17
        "%m/%d/%Y",      # 02/17/2026
        "%d %b %Y",      # 17 Feb 2026
        "%d %B %Y",      # 17 February 2026
        "%Y/%m/%d",      # 2026/02/17
        "%d.%m.%Y",      # 17.02.2026
    ]
    
    for fmt in formats_to_try:
        try:
            parsed = pd.to_datetime(date_series, format=fmt, errors='coerce')
            if parsed.notna().sum() > len(date_series) * 0.3:  # At least 30% success
                return parsed
        except:
            continue
    
    # Last resort: coerce
    return pd.to_datetime(date_series, errors='coerce', dayfirst=True)

def calculate_stats(df, source_name):
    """Calculate boxes and weight stats for a dataframe"""
    total_boxes = 0
    total_weight = 0.0
    
    box_aliases = ["box_count", "boxes", "box count", "no of boxes", "n.o of boxes", "no. of boxes", "boxcount", "total_boxes", "box"]
    weight_aliases = ["weight_kgs", "weight (kg)", "weight", "order net weight", "chargeable weight", "order's net weight (kg)", "weight_kg", "total_weight", "net_weight", "gross_weight", "wt", "wt (kg)", "net weight"]
    
    # Find box column
    box_col = None
    for col in df.columns:
        col_lower = col.lower().strip()
        for alias in box_aliases:
            if alias.lower() == col_lower or alias.lower() in col_lower:
                box_col = col
                break
        if box_col:
            break
    
    # Find weight column
    weight_col = None
    for col in df.columns:
        col_lower = col.lower().strip()
        for alias in weight_aliases:
            if alias.lower() == col_lower or alias.lower() in col_lower:
                weight_col = col
                break
        if weight_col:
            break
    
    if box_col:
        try:
            total_boxes = pd.to_numeric(df[box_col], errors='coerce').sum()
            if pd.isna(total_boxes):
                total_boxes = 0
        except:
            total_boxes = 0
    
    if weight_col:
        try:
            total_weight = pd.to_numeric(df[weight_col], errors='coerce').sum()
            if pd.isna(total_weight):
                total_weight = 0.0
        except:
            total_weight = 0.0
    
    return int(total_boxes), round(total_weight, 2)

# =============================================================================
# SEARCH FUNCTION
# =============================================================================

def instant_search(order_ids):
    results = []
    
    for order_id in order_ids:
        search_term = str(order_id).lower().strip()
        if not search_term:
            continue
        
        for source_name, source_data in st.session_state.all_data.items():
            if source_name == "_kerry_status_tab":
                continue
            
            try:
                df = source_data.get("df", pd.DataFrame())
                order_col = source_data.get("order_col")
                
                if df.empty or order_col is None or order_col not in df.columns:
                    continue
                
                df_search = df[order_col].astype(str).str.lower().str.strip()
                matches = df[df_search == search_term]
                
                if matches.empty:
                    matches = df[df_search.str.contains(search_term, na=False, regex=False)]
                
                for _, row in matches.iterrows():
                    config = DATA_SOURCES[source_name]
                    row_data = row.to_dict()
                    
                    order_value = row.get(order_col)
                    if pd.notna(order_value):
                        row_data["Order Number"] = str(order_value)
                    
                    live_status = get_latest_status_from_kerry(order_id)
                    if live_status:
                        row_data["_live_status_from_kerry"] = live_status
                    
                    results.append({
                        "source": source_name,
                        "partner": config["partner"],
                        "type": config["type"],
                        "icon": config["icon"],
                        "order_id": order_id,
                        "data": row_data
                    })
            except:
                continue
    
    return results

# =============================================================================
# UI COMPONENTS
# =============================================================================

def render_result_card(result):
    partner = result["partner"]
    source_name = result["source"]
    icon = result["icon"]
    data = result["data"]
    order_id = result["order_id"]
    
    st.markdown(f"""
    <div class="result-card result-card-{partner.lower()}">
        <div class="result-partner result-partner-{partner.lower()}">{icon} {partner}</div>
        <div class="result-source">{source_name}</div>
        <div class="result-order">Order: {order_id}</div>
    </div>
    """, unsafe_allow_html=True)
    
    for section_name, fields in DISPLAY_FIELDS.items():
        st.markdown(f"<div class='section-title'>{section_name}</div>", unsafe_allow_html=True)
        
        cols = st.columns(2)
        for i, field in enumerate(fields):
            value = get_field_value(data, field["aliases"])
            with cols[i % 2]:
                st.markdown(f"<div class='field-label'>{field['label']}</div>", unsafe_allow_html=True)
                if value:
                    css_class = {
                        "highlight": "field-value-highlight",
                        "tracking": "field-value-tracking", 
                        "status": "field-value-status"
                    }.get(field["type"], "")
                    if field["type"] == "status":
                        st.markdown(f"<div class='field-value {css_class}'>📡 {value}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div class='field-value {css_class}'>{value}</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='field-value field-value-empty'>—</div>", unsafe_allow_html=True)
    
    st.markdown("---")

def render_sidebar():
    with st.sidebar:
        st.markdown("### 🚀 Navigation")
        st.markdown("")
        
        nav_options = [
            ("🔍 Global Search", "global_search"),
            ("🟠 ECL QC Center", "ECL QC Center"),
            ("🟠 ECL Zone", "ECL Zone"),
            ("🔵 GE QC Center", "GE QC Center"),
            ("🔵 GE Zone", "GE Zone"),
            ("🟣 APX", "APX"),
            ("🟢 Kerry", "Kerry"),
        ]
        
        if "current_page" not in st.session_state:
            st.session_state.current_page = "global_search"
        
        for label, page_key in nav_options:
            is_active = st.session_state.current_page == page_key
            if st.button(
                label, 
                key=f"nav_{page_key}",
                use_container_width=True,
                type="primary" if is_active else "secondary"
            ):
                st.session_state.current_page = page_key
                st.rerun()
        
        st.markdown("---")
        
        if st.session_state.get("data_loaded"):
            sources_ok = sum(1 for name, d in st.session_state.all_data.items() if name != "_kerry_status_tab" and not d["df"].empty)
            status_rows = len(st.session_state.all_data.get("_kerry_status_tab", {}).get("df", []))
            st.success(f"✅ {st.session_state.total_rows:,} rows")
            st.caption(f"{sources_ok}/6 sources | 📡 {status_rows:,} status")
        
        st.markdown("---")
        
        if st.button("🔄 Reload Data", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        if st.session_state.get("load_errors"):
            with st.expander("⚠️ Warnings"):
                for err in st.session_state.load_errors:
                    st.warning(err)
        
        return st.session_state.current_page

def search_page():
    st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">🔎 TrackMaster Pro</h1>
        <p class="hero-subtitle">Track shipments across all partners with live status</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([5, 1])
    with col1:
        search_input = st.text_input(
            "Search",
            placeholder="Enter Order ID (e.g., 122129_34, 129433_54)",
            label_visibility="collapsed",
            key="search_box"
        )
    with col2:
        search_btn = st.button("🔍 Search", use_container_width=True, type="primary")
    
    st.markdown('<p class="search-hint">💡 Multiple orders: comma ya space se separate karein</p>', unsafe_allow_html=True)
    
    if search_input and search_input.strip():
        order_ids = [x.strip() for x in re.split(r'[\n,\t\s]+', search_input) if x.strip()]
        
        if order_ids:
            start = time.time()
            results = instant_search(order_ids)
            search_time = (time.time() - start) * 1000
            
            st.markdown("---")
            
            if results:
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Results", len(results))
                col2.metric("Orders", len(order_ids))
                col3.metric("Sources", len(set(r["source"] for r in results)))
                col4.metric("Speed", f"{search_time:.0f}ms")
                
                st.markdown("---")
                
                for result in results:
                    render_result_card(result)
            else:
                st.error(f"❌ No results for: {', '.join(order_ids)}")
                st.info("💡 Order ID check karein ya different ID try karein")
    else:
        st.markdown("---")
        counts = get_partner_counts()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""<div class="partner-card">
                <div class="partner-icon">🟠</div>
                <div class="partner-name">ECL</div>
                <div class="partner-count partner-count-ecl">{counts['ECL']:,}</div>
                <div class="partner-label">Orders</div>
            </div>""", unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""<div class="partner-card">
                <div class="partner-icon">🔵</div>
                <div class="partner-name">GE</div>
                <div class="partner-count partner-count-ge">{counts['GE']:,}</div>
                <div class="partner-label">Orders</div>
            </div>""", unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""<div class="partner-card">
                <div class="partner-icon">🟣</div>
                <div class="partner-name">APX</div>
                <div class="partner-count partner-count-apx">{counts['APX']:,}</div>
                <div class="partner-label">Orders</div>
            </div>""", unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""<div class="partner-card">
                <div class="partner-icon">🟢</div>
                <div class="partner-name">Kerry</div>
                <div class="partner-count partner-count-kerry">{counts['Kerry']:,}</div>
                <div class="partner-label">+ Status</div>
            </div>""", unsafe_allow_html=True)

def data_page(source_name):
    config = DATA_SOURCES[source_name]
    st.markdown(f"## {config['icon']} {source_name}")
    
    source_data = st.session_state.all_data.get(source_name, {})
    df = source_data.get("df", pd.DataFrame())
    
    if df.empty:
        st.error("No data available")
        return
    
    # =========================================================================
    # FIND DATE COLUMN AUTOMATICALLY
    # =========================================================================
    date_col = find_date_column(df)
    
    # =========================================================================
    # DATE FILTER SECTION
    # =========================================================================
    st.markdown("### 📅 Date Filter")
    
    if date_col:
        st.info(f"📅 Date column detected: **{date_col}**")
        
        # Parse dates
        df["_parsed_date"] = smart_parse_date(df[date_col])
        valid_dates = df["_parsed_date"].dropna()
        
        if len(valid_dates) > 0:
            min_date = valid_dates.min().date()
            max_date = valid_dates.max().date()
            
            col1, col2, col3 = st.columns([2, 2, 2])
            
            with col1:
                start_date = st.date_input(
                    "From Date",
                    value=max(min_date, datetime.now().date() - timedelta(days=30)),
                    min_value=min_date,
                    max_value=max_date,
                    key=f"start_date_{source_name}"
                )
            
            with col2:
                end_date = st.date_input(
                    "To Date",
                    value=max_date,
                    min_value=min_date,
                    max_value=max_date,
                    key=f"end_date_{source_name}"
                )
            
            with col3:
                st.markdown("<br>", unsafe_allow_html=True)
                apply_filter = st.button("🔍 Apply Date Filter", key=f"apply_filter_{source_name}", use_container_width=True)
                clear_filter = st.button("❌ Clear Filter", key=f"clear_filter_{source_name}", use_container_width=True)
            
            # Store filter state
            filter_key = f"date_filter_active_{source_name}"
            if apply_filter:
                st.session_state[filter_key] = True
                st.session_state[f"start_{source_name}"] = start_date
                st.session_state[f"end_{source_name}"] = end_date
            
            if clear_filter:
                st.session_state[filter_key] = False
            
            # Apply filter if active
            display_df = df.copy()
            if st.session_state.get(filter_key, False):
                stored_start = st.session_state.get(f"start_{source_name}", start_date)
                stored_end = st.session_state.get(f"end_{source_name}", end_date)
                
                # Convert to datetime for comparison
                start_datetime = pd.Timestamp(stored_start)
                end_datetime = pd.Timestamp(stored_end) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
                
                mask = (display_df["_parsed_date"] >= start_datetime) & (display_df["_parsed_date"] <= end_datetime)
                display_df = display_df[mask]
                
                st.success(f"✅ Filter Applied: {stored_start} to {stored_end} | Showing {len(display_df):,} of {len(df):,} rows")
            
            # Remove temp column for display
            if "_parsed_date" in display_df.columns:
                display_df = display_df.drop(columns=["_parsed_date"])
        else:
            st.warning("⚠️ Could not parse dates from the date column")
            display_df = df.copy()
    else:
        st.warning("⚠️ No date column found. Available columns: " + ", ".join(df.columns[:10].tolist()))
        display_df = df.copy()
    
    # Remove _parsed_date from original df display
    if "_parsed_date" in df.columns:
        df = df.drop(columns=["_parsed_date"])
    
    st.markdown("---")
    
    # =========================================================================
    # STATS - BOXES & WEIGHT
    # =========================================================================
    total_boxes, total_weight = calculate_stats(display_df, source_name)
    
    st.markdown(f"""
    <div class="stats-container">
        <div class="stat-card">
            <div class="stat-icon">📦</div>
            <div class="stat-value stat-value-orange">{len(display_df):,}</div>
            <div class="stat-label">Total Orders</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon">📦</div>
            <div class="stat-value stat-value-blue">{total_boxes:,}</div>
            <div class="stat-label">Total Boxes</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon">⚖️</div>
            <div class="stat-value stat-value-green">{total_weight:,.2f}</div>
            <div class="stat-label">Total Weight (kg)</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon">📊</div>
            <div class="stat-value stat-value-purple">{len(display_df.columns)}</div>
            <div class="stat-label">Columns</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # =========================================================================
    # SEARCH/FILTER IN TABLE
    # =========================================================================
    filter_text = st.text_input("🔍 Search in table...", key=f"filter_{source_name}")
    
    if filter_text:
        mask = display_df.astype(str).apply(lambda x: x.str.contains(filter_text, case=False, na=False)).any(axis=1)
        display_df = display_df[mask]
    
    st.dataframe(display_df, use_container_width=True, height=400)
    
    st.download_button(
        "📥 Download CSV", 
        display_df.to_csv(index=False), 
        f"{source_name}_{datetime.now().strftime('%Y%m%d')}.csv", 
        "text/csv"
    )

# =============================================================================
# MAIN
# =============================================================================

def main():
    if "data_loaded" not in st.session_state:
        st.markdown("""<div class="hero-container">
            <h1 class="hero-title">🔎 TrackMaster Pro</h1>
            <p class="hero-subtitle">Loading data...</p>
        </div>""", unsafe_allow_html=True)
        
        with st.spinner("Loading 6 sources + Kerry status tab..."):
            initialize_data()
        st.rerun()
    
    page = render_sidebar()
    
    if page == "global_search":
        search_page()
    else:
        data_page(page)

if __name__ == "__main__":
    main()
