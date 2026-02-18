import streamlit as st
import pandas as pd
import requests
from io import StringIO
import concurrent.futures
import time
import re

st.set_page_config(
    page_title="TrackMaster Pro",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# THEME - NORMAL SIZE, SIRF HEADING BADI
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
    
    [data-testid="stSidebar"] .stRadio > div > label {
        background: rgba(255,255,255,0.02) !important;
        border: 1px solid rgba(255,255,255,0.05) !important;
        border-radius: 8px !important;
        padding: 10px 12px !important;
        margin: 2px 0 !important;
        color: #888 !important;
        font-size: 0.85rem !important;
    }
    
    [data-testid="stSidebar"] .stRadio > div > label:hover {
        background: rgba(99, 102, 241, 0.1) !important;
        color: #fff !important;
    }
    
    [data-testid="stSidebar"] .stRadio > div > label[data-checked="true"] {
        background: rgba(99, 102, 241, 0.2) !important;
        border-color: rgba(99, 102, 241, 0.5) !important;
        color: #fff !important;
    }
    
    /* HERO - SIRF HEADING BADI */
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
    
    /* PARTNER CARDS - NORMAL SIZE */
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
    
    /* RESULT CARDS - NORMAL SIZE */
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
    
    /* SECTION & FIELDS - NORMAL SIZE */
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

# Kerry "latest status" TAB URL (gid=2121564686)
KERRY_STATUS_TAB_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTZyLyZpVJz9sV5eT4Srwo_KZGnYggpRZkm2ILLYPQKSpTKkWfP9G5759h247O4QEflKCzlQauYsLKI/pub?gid=2121564686&single=true&output=csv"

# =============================================================================
# DISPLAY FIELDS - PIECES REMOVED
# =============================================================================

DISPLAY_FIELDS = {
    "📋 Order Information": [
        {"label": "Order Number", "aliases": ["order#", "order", "fleek id", "_order", "order no", "order num"], "type": "highlight"},
        {"label": "Handover Date", "aliases": ["date", "fleek handover date", "airport handover date", "handover date", "ge entry date"], "type": "normal"},
        {"label": "Service", "aliases": ["services", "service", "partner", "3pl", "sea / air"], "type": "normal"},
        {"label": "QC Status", "aliases": ["qc status", "qc_status"], "type": "normal"},
    ],
    "📦 Shipment Details": [
        {"label": "Boxes", "aliases": ["box_count", "boxes", "box count", "no of boxes", "n.o of boxes", "no. of boxes"], "type": "normal"},
        {"label": "Weight (kg)", "aliases": ["weight_kgs", "weight (kg)", "weight", "order net weight", "chargeable weight", "order's net weight (kg)"], "type": "normal"},
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
        {"label": "Latest Status", "aliases": ["_live_status_from_kerry"], "type": "status"},
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
# KERRY STATUS TAB SE STATUS FETCH - SAFE (NEVER FAILS)
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

# =============================================================================
# SEARCH FUNCTION - FIXED
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
                
                # Search using order column directly
                df_search = df[order_col].astype(str).str.lower().str.strip()
                
                # Exact match first
                matches = df[df_search == search_term]
                
                # Fallback to contains search
                if matches.empty:
                    matches = df[df_search.str.contains(search_term, na=False, regex=False)]
                
                for _, row in matches.iterrows():
                    config = DATA_SOURCES[source_name]
                    row_data = row.to_dict()
                    
                    # Kerry status fetch - SAFE
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
# HELPER FUNCTIONS
# =============================================================================

def is_valid(val):
    if val is None:
        return False
    s = str(val).lower().strip()
    return s not in ['', 'nan', 'none', 'n/a', '#n/a', 'na', '-', 'null', 'nat', 'not applicable']

def get_field_value(data, aliases):
    for key, val in data.items():
        if key.lower().strip() in [a.lower() for a in aliases]:
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
        page = st.radio(
            "View",
            ["🔍 Global Search", "🟠 ECL QC Center", "🟠 ECL Zone", "🔵 GE QC Center", "🔵 GE Zone", "🟣 APX", "🟢 Kerry"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        if st.session_state.get("data_loaded"):
            sources_ok = sum(1 for name, d in st.session_state.all_data.items() if name != "_kerry_status_tab" and not d["df"].empty)
            status_rows = len(st.session_state.all_data.get("_kerry_status_tab", {}).get("df", []))
            st.success(f"✅ {st.session_state.total_rows:,} rows")
            st.caption(f"{sources_ok}/6 sources | 📡 {status_rows:,} status")
        
        st.markdown("---")
        
        if st.button("🔄 Reload", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        if st.session_state.get("load_errors"):
            with st.expander("⚠️ Warnings"):
                for err in st.session_state.load_errors:
                    st.warning(err)
        
        return page

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
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", f"{len(df):,}")
    col2.metric("Columns", len(df.columns))
    col3.metric("Partner", config["partner"])
    
    st.markdown("---")
    
    filter_text = st.text_input("🔍 Filter...", key=f"filter_{source_name}")
    display_df = df.copy()
    
    if filter_text:
        mask = display_df.astype(str).apply(lambda x: x.str.contains(filter_text, case=False, na=False)).any(axis=1)
        display_df = display_df[mask]
    
    st.dataframe(display_df, use_container_width=True, height=400)
    st.download_button("📥 Download", display_df.to_csv(index=False), f"{source_name}.csv", "text/csv")

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
