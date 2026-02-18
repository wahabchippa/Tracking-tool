import streamlit as st
import pandas as pd
import requests
from io import StringIO
import concurrent.futures
import time

# Page config
st.set_page_config(
    page_title="TID Search Tool",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# PREMIUM THEME - DECENT & PROFESSIONAL
# =============================================================================

st.markdown("""
<style>
    /* ===== MAIN BACKGROUND - Soft Dark Theme ===== */
    .stApp {
        background: linear-gradient(160deg, #0d1117 0%, #161b22 50%, #0d1117 100%);
    }
    
    /* ===== SIDEBAR - Sleek Dark ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #161b22 0%, #0d1117 100%);
        border-right: 1px solid #30363d;
    }
    
    [data-testid="stSidebar"] .stRadio label {
        color: #c9d1d9 !important;
    }
    
    [data-testid="stSidebar"] .stRadio label:hover {
        color: #58a6ff !important;
    }
    
    /* ===== HEADER STYLING ===== */
    .premium-header {
        background: linear-gradient(135deg, #58a6ff 0%, #a371f7 50%, #f778ba 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    
    .subtitle {
        color: #8b949e;
        font-size: 1rem;
        font-weight: 400;
    }
    
    /* ===== LIVE BADGE ===== */
    .live-badge {
        background: linear-gradient(135deg, #238636 0%, #2ea043 100%);
        color: white;
        padding: 8px 18px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(46, 160, 67, 0.3);
    }
    
    /* ===== CARDS & CONTAINERS ===== */
    .result-header-box {
        background: linear-gradient(145deg, #21262d 0%, #161b22 100%);
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 15px;
        border: 1px solid #30363d;
        border-left: 4px solid;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    .result-header-box:hover {
        box-shadow: 0 8px 30px rgba(0,0,0,0.3);
        transform: translateY(-2px);
    }
    
    .result-header-ecl { border-left-color: #f0883e; }
    .result-header-ge { border-left-color: #58a6ff; }
    .result-header-apx { border-left-color: #a371f7; }
    .result-header-kerry { border-left-color: #3fb950; }
    
    /* ===== PARTNER COLORS ===== */
    .partner-name {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    
    .partner-ecl { color: #f0883e; }
    .partner-ge { color: #58a6ff; }
    .partner-apx { color: #a371f7; }
    .partner-kerry { color: #3fb950; }
    
    .source-name {
        color: #f0f6fc;
        font-size: 1.15rem;
        font-weight: 600;
        margin: 6px 0;
    }
    
    .order-id-display {
        color: #8b949e;
        font-size: 0.9rem;
    }
    
    /* ===== SECTION TITLES ===== */
    .section-title {
        color: #58a6ff;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin: 20px 0 12px 0;
        padding-bottom: 8px;
        border-bottom: 1px solid #30363d;
    }
    
    /* ===== FIELD STYLING ===== */
    .field-label {
        color: #8b949e;
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }
    
    .field-value {
        color: #f0f6fc;
        font-size: 0.95rem;
        font-weight: 500;
        background: #21262d;
        padding: 10px 14px;
        border-radius: 8px;
        margin-top: 4px;
        border: 1px solid #30363d;
    }
    
    .field-value-empty {
        color: #484f58;
        font-style: italic;
        background: #161b22;
    }
    
    .field-value-highlight {
        background: linear-gradient(135deg, rgba(88, 166, 255, 0.15) 0%, rgba(88, 166, 255, 0.05) 100%);
        color: #58a6ff;
        font-weight: 600;
        border: 1px solid rgba(88, 166, 255, 0.3);
    }
    
    .field-value-tracking {
        background: linear-gradient(135deg, rgba(63, 185, 80, 0.15) 0%, rgba(63, 185, 80, 0.05) 100%);
        color: #3fb950;
        font-family: 'SF Mono', 'Consolas', monospace;
        border: 1px solid rgba(63, 185, 80, 0.3);
    }
    
    /* ===== METRICS STYLING ===== */
    [data-testid="stMetricValue"] {
        color: #f0f6fc !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #8b949e !important;
    }
    
    /* ===== INPUT FIELDS ===== */
    .stTextInput > div > div > input {
        background: #21262d !important;
        border: 1px solid #30363d !important;
        border-radius: 10px !important;
        color: #f0f6fc !important;
        padding: 12px 16px !important;
        font-size: 0.95rem !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #58a6ff !important;
        box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.2) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #6e7681 !important;
    }
    
    /* ===== BUTTONS ===== */
    .stButton > button {
        background: linear-gradient(135deg, #238636 0%, #2ea043 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        box-shadow: 0 4px 15px rgba(46, 160, 67, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(46, 160, 67, 0.4) !important;
    }
    
    /* ===== SUCCESS/ERROR/INFO MESSAGES ===== */
    .stSuccess {
        background: rgba(46, 160, 67, 0.15) !important;
        border: 1px solid rgba(46, 160, 67, 0.3) !important;
        color: #3fb950 !important;
    }
    
    .stError {
        background: rgba(248, 81, 73, 0.15) !important;
        border: 1px solid rgba(248, 81, 73, 0.3) !important;
    }
    
    .stInfo {
        background: rgba(88, 166, 255, 0.1) !important;
        border: 1px solid rgba(88, 166, 255, 0.2) !important;
    }
    
    /* ===== EXPANDER ===== */
    .streamlit-expanderHeader {
        background: #21262d !important;
        border: 1px solid #30363d !important;
        border-radius: 10px !important;
        color: #f0f6fc !important;
    }
    
    .streamlit-expanderContent {
        background: #161b22 !important;
        border: 1px solid #30363d !important;
        border-top: none !important;
    }
    
    /* ===== DATAFRAME ===== */
    .stDataFrame {
        border: 1px solid #30363d !important;
        border-radius: 10px !important;
    }
    
    /* ===== CAPTION ===== */
    .stCaption {
        color: #8b949e !important;
    }
    
    /* ===== DIVIDER ===== */
    hr {
        border-color: #30363d !important;
    }
    
    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #161b22;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #30363d;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #484f58;
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
# DISPLAY FIELDS CONFIG
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
        {"label": "Pieces", "aliases": ["n.o of pieces", "pieces", "item count", "items"], "type": "normal"},
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
                results.append({
                    "source": source_name,
                    "partner": config["partner"],
                    "type": config["type"],
                    "icon": config["icon"],
                    "order_id": order_id,
                    "data": row.to_dict()
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
        st.markdown('<p class="premium-header">TID Search</p>', unsafe_allow_html=True)
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
        st.markdown('<p class="premium-header">TID Search</p>', unsafe_allow_html=True)
        
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
