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
# CSS STYLING
# =============================================================================

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #0f0f1a 100%);
    }
    
    /* Header - TOP LEFT */
    .main-header-container {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        padding: 10px 0 30px 0;
    }
    
    .header-left {
        display: flex;
        flex-direction: column;
    }
    
    .premium-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: -1px;
        margin: 0;
    }
    
    .header-subtitle {
        color: #8892b0;
        font-size: 1rem;
        margin-top: 5px;
    }
    
    .header-right {
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .live-badge {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 8px 16px;
        border-radius: 25px;
        font-size: 0.8rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .live-dot {
        width: 8px;
        height: 8px;
        background: #fff;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* Search Container - BETTER */
    .search-container {
        background: linear-gradient(145deg, #1e1e32 0%, #252540 100%);
        border-radius: 20px;
        padding: 35px;
        border: 1px solid #3d3d5c;
        margin: 20px 0 30px 0;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
    }
    
    .search-label {
        color: #667eea;
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* Quick Tips */
    .tips-container {
        display: flex;
        gap: 15px;
        margin-top: 20px;
        flex-wrap: wrap;
    }
    
    .tip-item {
        background: rgba(102, 126, 234, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.2);
        border-radius: 10px;
        padding: 10px 15px;
        color: #8892b0;
        font-size: 0.8rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .tip-item span {
        color: #667eea;
    }
    
    /* Partner Cards - Homepage */
    .partners-section {
        margin-top: 40px;
    }
    
    .section-title {
        color: #e6f1ff;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .partners-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 15px;
    }
    
    .partner-card {
        background: linear-gradient(145deg, #1e1e32 0%, #252540 100%);
        border-radius: 16px;
        padding: 25px;
        border: 1px solid #3d3d5c;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .partner-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.15);
        border-color: #667eea;
    }
    
    .partner-icon {
        font-size: 2.5rem;
        margin-bottom: 10px;
    }
    
    .partner-name {
        color: #e6f1ff;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 5px;
    }
    
    .partner-count {
        color: #8892b0;
        font-size: 0.85rem;
    }
    
    .partner-ecl { border-top: 3px solid #f59e0b; }
    .partner-ge { border-top: 3px solid #3b82f6; }
    .partner-apx { border-top: 3px solid #8b5cf6; }
    .partner-kerry { border-top: 3px solid #10b981; }
    
    /* Speed badge */
    .speed-badge {
        background: rgba(102, 126, 234, 0.2);
        color: #667eea;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    
    .status-badge {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 10px 20px;
        border-radius: 30px;
        font-weight: 600;
        display: inline-block;
    }
    
    .status-badge.loading {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    }
    
    /* Result Card */
    .result-card {
        background: linear-gradient(145deg, #1e1e32 0%, #252540 100%);
        border-radius: 16px;
        padding: 0;
        margin: 20px 0;
        border: 1px solid #3d3d5c;
        overflow: hidden;
    }
    
    .result-header {
        background: linear-gradient(135deg, #2a2a45 0%, #1e1e32 100%);
        padding: 18px 25px;
        display: flex;
        align-items: center;
        gap: 15px;
        border-bottom: 1px solid #3d3d5c;
    }
    
    .partner-badge {
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .partner-badge-ecl { background: #f59e0b; color: #000; }
    .partner-badge-ge { background: #3b82f6; color: #fff; }
    .partner-badge-apx { background: #8b5cf6; color: #fff; }
    .partner-badge-kerry { background: #10b981; color: #fff; }
    
    .order-number {
        color: #e6f1ff;
        font-size: 1.4rem;
        font-weight: 700;
    }
    
    .source-name {
        color: #8892b0;
        font-size: 0.9rem;
        margin-left: auto;
    }
    
    /* Clean Table Style */
    .data-table {
        width: 100%;
        border-collapse: collapse;
    }
    
    .data-table tr {
        border-bottom: 1px solid #2d2d44;
    }
    
    .data-table tr:last-child {
        border-bottom: none;
    }
    
    .data-table td {
        padding: 14px 25px;
        vertical-align: top;
    }
    
    .data-table td:first-child {
        width: 180px;
        color: #8892b0;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .data-table td:last-child {
        color: #e6f1ff;
        font-size: 1rem;
        font-weight: 500;
    }
    
    .highlight-value {
        background: rgba(102, 126, 234, 0.15);
        padding: 4px 10px;
        border-radius: 6px;
        color: #667eea;
        font-weight: 600;
    }
    
    .tracking-value {
        background: rgba(16, 185, 129, 0.15);
        padding: 4px 10px;
        border-radius: 6px;
        color: #10b981;
        font-family: monospace;
    }
    
    .empty-value {
        color: #4a4a6a;
        font-style: italic;
    }
    
    .section-header {
        background: rgba(255,255,255,0.03);
        padding: 10px 25px;
        color: #667eea;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    
    /* Stats Row */
    .stats-row {
        display: flex;
        gap: 20px;
        margin: 25px 0;
    }
    
    .stat-box {
        background: linear-gradient(145deg, #1e1e32 0%, #252540 100%);
        border-radius: 12px;
        padding: 20px 30px;
        border: 1px solid #3d3d5c;
        text-align: center;
        flex: 1;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    .stat-label {
        color: #8892b0;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 5px;
    }
    
    /* No Results */
    .no-results {
        text-align: center;
        padding: 60px;
        color: #8892b0;
        background: linear-gradient(145deg, #1e1e32 0%, #252540 100%);
        border-radius: 16px;
        border: 1px solid #3d3d5c;
        margin-top: 30px;
    }
    
    .no-results h2 {
        color: #e6f1ff;
        margin-bottom: 10px;
    }
    
    /* Recent searches placeholder */
    .recent-section {
        margin-top: 40px;
    }
    
    .empty-state {
        background: linear-gradient(145deg, #1e1e32 0%, #252540 100%);
        border-radius: 16px;
        border: 1px dashed #3d3d5c;
        padding: 50px;
        text-align: center;
        color: #8892b0;
    }
    
    .empty-state-icon {
        font-size: 3rem;
        margin-bottom: 15px;
        opacity: 0.5;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# DATA SOURCES
# =============================================================================

DATA_SOURCES = {
    "ECL QC Center": {"url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSCiZ1MdPMyVAzBqmBmp3Ch8sfefOp_kfPk2RSfMv3bxRD_qccuwaoM7WTVsieKJbA3y3DF41tUxb3T/pub?gid=0&single=true&output=csv", "order_col": "Fleek ID", "partner": "ECL"},
    "ECL Zone": {"url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSCiZ1MdPMyVAzBqmBmp3Ch8sfefOp_kfPk2RSfMv3bxRD_qccuwaoM7WTVsieKJbA3y3DF41tUxb3T/pub?gid=928309568&single=true&output=csv", "order_col": 0, "partner": "ECL"},
    "GE QC Center": {"url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQjCPd8bUpx59Sit8gMMXjVKhIFA_f-W9Q4mkBSWulOTg4RGahcVXSD4xZiYBAcAH6eO40aEQ9IEEXj/pub?gid=710036753&single=true&output=csv", "order_col": "Order Num", "partner": "GE"},
    "GE Zone": {"url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQjCPd8bUpx59Sit8gMMXjVKhIFA_f-W9Q4mkBSWulOTg4RGahcVXSD4xZiYBAcAH6eO40aEQ9IEEXj/pub?gid=10726393&single=true&output=csv", "order_col": 0, "partner": "GE"},
    "APX": {"url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRDEzAMUwnFZ7aoThGoMERtxxsll2kfEaSpa9ksXIx6sqbdMncts6Go2d5mKKabepbNXDSoeaUlk-mP/pub?gid=0&single=true&output=csv", "order_col": "Fleek ID", "partner": "APX"},
    "Kerry": {"url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vTZyLyZpVJz9sV5eT4Srwo_KZGnYggpRZkm2ILLYPQKSpTKkWfP9G5759h247O4QEflKCzlQauYsLKI/pub?gid=0&single=true&output=csv", "order_col": "_Order", "partner": "Kerry"}
}

# =============================================================================
# DISPLAY FIELDS
# =============================================================================

DISPLAY_FIELDS = [
    {"section": "Order Information", "fields": [
        {"key": "order#", "label": "Order Number", "aliases": ["order#", "order", "fleek id", "_order", "order no", "order no.", "order num"], "highlight": True},
        {"key": "date", "label": "Handover Date", "aliases": ["date", "fleek handover date", "airport handover date", "handover date", "ge entry date"]},
        {"key": "services", "label": "Service", "aliases": ["services", "service", "partner", "3pl"]},
        {"key": "qc_status", "label": "QC Status", "aliases": ["qc status", "qc_status", "status"]},
    ]},
    {"section": "Shipment Details", "fields": [
        {"key": "boxes", "label": "Number of Boxes", "aliases": ["box_count", "boxes", "box count", "no of boxes", "n.o of boxes", "number of boxes"]},
        {"key": "weight", "label": "Weight (kg)", "aliases": ["weight_kgs", "weight (kg)", "weight", "order net weight", "net weight", "chargeable weight"]},
        {"key": "pieces", "label": "Pieces", "aliases": ["n.o of pieces", "pieces", "item count", "items"]},
    ]},
    {"section": "Tracking & Delivery", "fields": [
        {"key": "awb", "label": "Airway Bill (AWB)", "aliases": ["airway_bill", "awb", "hawb", "mawb", "apx awb number", "kerry awb number", "ge awb"], "highlight": True},
        {"key": "tracking", "label": "Tracking ID", "aliases": ["courier_tracking_ids", "tracking id", "tracking_id", "tracking", "ge comment / tracking"], "tracking": True},
        {"key": "courier", "label": "Courier Service", "aliases": ["courier_service", "courier", "carrier"]},
    ]},
    {"section": "Customer & Destination", "fields": [
        {"key": "consignee", "label": "Customer Name", "aliases": ["consignee", "customer name", "customer_name", "customer", "name"]},
        {"key": "destination", "label": "Destination", "aliases": ["destination", "country", "city"]},
    ]},
]

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
                results.append({
                    "source": source_name,
                    "partner": DATA_SOURCES[source_name]["partner"],
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
            return val
    return None

def format_value(val, is_highlight=False, is_tracking=False):
    if not is_valid(val):
        return '<span class="empty-value">—</span>'
    val_str = str(val)
    if is_highlight:
        return f'<span class="highlight-value">{val_str}</span>'
    elif is_tracking:
        return f'<span class="tracking-value">{val_str}</span>'
    return val_str

# =============================================================================
# UI COMPONENTS
# =============================================================================

def render_result_card(result):
    partner = result["partner"]
    data = result["data"]
    
    table_html = ""
    for section in DISPLAY_FIELDS:
        table_html += f'<tr><td colspan="2" class="section-header">{section["section"]}</td></tr>'
        for field in section["fields"]:
            value = get_field_value(data, field["aliases"])
            formatted = format_value(value, is_highlight=field.get("highlight", False), is_tracking=field.get("tracking", False))
            table_html += f'<tr><td>{field["label"]}</td><td>{formatted}</td></tr>'
    
    st.markdown(f"""
    <div class="result-card">
        <div class="result-header">
            <span class="partner-badge partner-badge-{partner.lower()}">{partner}</span>
            <span class="order-number">{result['order_id']}</span>
            <span class="source-name">📍 {result['source']}</span>
        </div>
        <table class="data-table">{table_html}</table>
    </div>
    """, unsafe_allow_html=True)

def render_stats(results, order_count, search_time):
    partners = list(set(r["partner"] for r in results))
    st.markdown(f"""
    <div class="stats-row">
        <div class="stat-box"><div class="stat-number">{len(results)}</div><div class="stat-label">Results</div></div>
        <div class="stat-box"><div class="stat-number">{order_count}</div><div class="stat-label">Searched</div></div>
        <div class="stat-box"><div class="stat-number">{len(partners)}</div><div class="stat-label">Partners</div></div>
        <div class="stat-box"><div class="stat-number">{search_time:.0f}ms</div><div class="stat-label">Speed</div></div>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    with st.sidebar:
        st.markdown("### 🚀 Navigation")
        page = st.radio("View", ["🔍 Global Search", "🟠 ECL QC", "🟠 ECL Zone", "🔵 GE QC", "🔵 GE Zone", "🟣 APX", "🟢 Kerry"], label_visibility="collapsed")
        st.markdown("---")
        if st.session_state.get("data_loaded"):
            sources_ok = sum(1 for d in st.session_state.all_data.values() if not d["df"].empty)
            st.markdown(f'<div class="status-badge">✅ {st.session_state.total_rows:,} rows</div>', unsafe_allow_html=True)
            st.caption(f"{sources_ok}/6 sources")
        st.markdown("---")
        if st.button("🔄 Reload", use_container_width=True):
            if "data_loaded" in st.session_state:
                del st.session_state.data_loaded
            st.rerun()
        if st.session_state.get("load_errors"):
            with st.expander("⚠️ Warnings"):
                for err in st.session_state.load_errors:
                    st.warning(err)
        return page

def get_partner_counts():
    """Get row counts per partner"""
    counts = {"ECL": 0, "GE": 0, "APX": 0, "Kerry": 0}
    for name, data in st.session_state.all_data.items():
        partner = DATA_SOURCES[name]["partner"]
        counts[partner] += len(data["df"])
    return counts

def search_page():
    # Header - TOP LEFT
    st.markdown("""
    <div class="main-header-container">
        <div class="header-left">
            <div class="premium-header">TID Search</div>
            <div class="header-subtitle">Logistics Tracking Intelligence Dashboard</div>
        </div>
        <div class="header-right">
            <div class="live-badge"><div class="live-dot"></div> Live Data</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Search Container
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    st.markdown('<div class="search-label">🔍 Search Orders</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([5, 1])
    with col1:
        search_input = st.text_input("Search", placeholder="Enter order ID (e.g., 122129_34, 122054_98)", label_visibility="collapsed")
    with col2:
        st.button("Search", use_container_width=True, type="primary")
    
    # Tips
    st.markdown("""
    <div class="tips-container">
        <div class="tip-item"><span>💡</span> Multiple orders: separate with comma or space</div>
        <div class="tip-item"><span>⚡</span> Search is instant - results in milliseconds</div>
        <div class="tip-item"><span>📊</span> Searches across all 6 data sources</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # If searching
    if search_input:
        import re
        order_ids = [x.strip() for x in re.split(r'[\n,\t\s]+', search_input) if x.strip()]
        
        if order_ids:
            start = time.time()
            results = instant_search(order_ids)
            search_time = (time.time() - start) * 1000
            
            st.markdown(f'<span class="speed-badge">⚡ {search_time:.1f}ms</span>', unsafe_allow_html=True)
            
            if results:
                render_stats(results, len(order_ids), search_time)
                for result in results:
                    render_result_card(result)
            else:
                st.markdown("""
                <div class="no-results">
                    <h2>🔍 No Results Found</h2>
                    <p>Try a different order ID or check the format</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        # Show partner cards when not searching
        counts = get_partner_counts()
        
        st.markdown("""
        <div class="partners-section">
            <div class="section-title">📦 Connected Data Sources</div>
            <div class="partners-grid">
                <div class="partner-card partner-ecl">
                    <div class="partner-icon">🟠</div>
                    <div class="partner-name">ECL</div>
                    <div class="partner-count">""" + f"{counts['ECL']:,}" + """ orders</div>
                </div>
                <div class="partner-card partner-ge">
                    <div class="partner-icon">🔵</div>
                    <div class="partner-name">GE</div>
                    <div class="partner-count">""" + f"{counts['GE']:,}" + """ orders</div>
                </div>
                <div class="partner-card partner-apx">
                    <div class="partner-icon">🟣</div>
                    <div class="partner-name">APX</div>
                    <div class="partner-count">""" + f"{counts['APX']:,}" + """ orders</div>
                </div>
                <div class="partner-card partner-kerry">
                    <div class="partner-icon">🟢</div>
                    <div class="partner-name">Kerry</div>
                    <div class="partner-count">""" + f"{counts['Kerry']:,}" + """ orders</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Empty state for recent
        st.markdown("""
        <div class="recent-section">
            <div class="section-title">🕐 Recent Searches</div>
            <div class="empty-state">
                <div class="empty-state-icon">🔍</div>
                <div>Your recent searches will appear here</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def data_page(source_name):
    config = DATA_SOURCES[source_name]
    st.markdown(f"## {source_name}")
    
    source_data = st.session_state.all_data.get(source_name, {})
    df = source_data.get("df", pd.DataFrame())
    
    if df.empty:
        st.error("No data")
        return
    
    col1, col2, col3 = st.columns(3)
    col1.metric("📦 Rows", f"{len(df):,}")
    col2.metric("📊 Columns", len(df.columns))
    col3.metric("Partner", config["partner"])
    
    st.markdown("---")
    filter_text = st.text_input("🔍 Filter", key=f"f_{source_name}")
    
    display_df = df.drop(columns=["_search_col"], errors="ignore")
    if filter_text:
        mask = display_df.astype(str).apply(lambda x: x.str.contains(filter_text, case=False, na=False)).any(axis=1)
        display_df = display_df[mask]
    
    st.dataframe(display_df, use_container_width=True, height=500)
    st.download_button("📥 Download", display_df.to_csv(index=False), f"{source_name}.csv", "text/csv")

# =============================================================================
# MAIN
# =============================================================================

def main():
    if "data_loaded" not in st.session_state:
        st.markdown("""
        <div style="text-align: center; padding: 100px;">
            <div class="premium-header">TID Search</div>
            <div class="status-badge loading">🔄 Loading data...</div>
            <p style="color: #8892b0; margin-top: 20px;">Connecting to all sources...</p>
        </div>
        """, unsafe_allow_html=True)
        initialize_data()
        st.rerun()
    
    page = render_sidebar()
    
    page_map = {
        "🔍 Global Search": search_page,
        "🟠 ECL QC": lambda: data_page("ECL QC Center"),
        "🟠 ECL Zone": lambda: data_page("ECL Zone"),
        "🔵 GE QC": lambda: data_page("GE QC Center"),
        "🔵 GE Zone": lambda: data_page("GE Zone"),
        "🟣 APX": lambda: data_page("APX"),
        "🟢 Kerry": lambda: data_page("Kerry"),
    }
    
    page_map.get(page, search_page)()

if __name__ == "__main__":
    main()
