import streamlit as st
import pandas as pd
import requests
from io import StringIO
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# =============================================================================
# PAGE CONFIG
# =============================================================================

st.set_page_config(
    page_title="TrackMaster Pro",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# 🎨 CLASSY PREMIUM THEME
# =============================================================================

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-primary: #0a0a0f;
    --bg-secondary: #12121a;
    --bg-card: #16161f;
    --bg-hover: #1e1e2a;
    --border-color: #2a2a3d;
    --text-primary: #f4f4f8;
    --text-secondary: #9898b0;
    --text-muted: #6b6b82;
    --accent-blue: #6366f1;
    --accent-purple: #a855f7;
    --accent-pink: #ec4899;
    --accent-green: #10b981;
    --accent-orange: #f97316;
}

.stApp {
    background: var(--bg-primary);
    background-image: 
        radial-gradient(ellipse at 20% 20%, rgba(99, 102, 241, 0.05) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 80%, rgba(168, 85, 247, 0.05) 0%, transparent 50%);
    font-family: 'Inter', sans-serif;
}

#MainMenu, footer, header {visibility: hidden;}
.stDeployButton {display: none;}

.premium-header {
    font-family: 'Inter', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #6366f1 0%, #a855f7 35%, #ec4899 70%, #22d3ee 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center;
    margin: 0;
    padding: 10px 0;
}

.header-icon {
    font-size: 3rem;
    text-align: center;
    display: block;
    margin-bottom: 5px;
    filter: drop-shadow(0 0 15px rgba(99, 102, 241, 0.5));
    animation: float 3s ease-in-out infinite;
}

.header-subtitle {
    text-align: center;
    color: var(--text-secondary);
    font-size: 0.95rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 5px;
}

.header-line {
    width: 80px;
    height: 3px;
    background: linear-gradient(90deg, #6366f1, #a855f7, #ec4899);
    border-radius: 2px;
    margin: 15px auto;
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-6px); }
}

.status-badge {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(34, 211, 238, 0.15));
    border: 1px solid rgba(16, 185, 129, 0.3);
    color: #10b981;
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    display: inline-block;
}

.status-badge.loading {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(168, 85, 247, 0.15));
    border-color: rgba(99, 102, 241, 0.3);
    color: #a5b4fc;
}

.partner-cards {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin: 20px 0;
}

.partner-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 24px 20px;
    text-align: center;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.partner-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 16px 16px 0 0;
}

.partner-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
}

.partner-ecl::before { background: linear-gradient(90deg, #f97316, #fb923c); }
.partner-ecl:hover { border-color: #f97316; }

.partner-ge::before { background: linear-gradient(90deg, #6366f1, #818cf8); }
.partner-ge:hover { border-color: #6366f1; }

.partner-apx::before { background: linear-gradient(90deg, #a855f7, #c084fc); }
.partner-apx:hover { border-color: #a855f7; }

.partner-kerry::before { background: linear-gradient(90deg, #10b981, #34d399); }
.partner-kerry:hover { border-color: #10b981; }

.partner-icon { font-size: 2.5rem; margin-bottom: 12px; }
.partner-name { font-size: 1.1rem; font-weight: 700; color: var(--text-primary); margin-bottom: 4px; }
.partner-count { font-size: 0.85rem; color: var(--text-secondary); }

.recent-section {
    margin-top: 30px;
    padding: 20px;
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 16px;
}

.section-title { font-size: 1rem; font-weight: 600; color: var(--text-primary); margin-bottom: 15px; }

.empty-state { text-align: center; padding: 30px; color: var(--text-muted); }
.empty-state-icon { font-size: 2.5rem; margin-bottom: 10px; opacity: 0.5; }

.speed-badge {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(34, 211, 238, 0.15));
    border: 1px solid rgba(16, 185, 129, 0.3);
    color: #10b981;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 0.8rem;
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
}

.result-header {
    padding: 18px 22px;
    border-radius: 14px 14px 0 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 20px;
}

.result-header-ecl { background: linear-gradient(135deg, #f97316, #fb923c); }
.result-header-ge { background: linear-gradient(135deg, #6366f1, #818cf8); }
.result-header-apx { background: linear-gradient(135deg, #a855f7, #c084fc); }
.result-header-kerry { background: linear-gradient(135deg, #10b981, #34d399); }

.result-partner { display: flex; align-items: center; gap: 12px; color: white; }
.result-partner-icon { font-size: 1.8rem; }
.result-partner-name { font-size: 1.2rem; font-weight: 700; }
.result-partner-type { font-size: 0.8rem; opacity: 0.9; }

.result-order {
    background: rgba(255,255,255,0.2);
    padding: 8px 16px;
    border-radius: 10px;
    color: white;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 600;
}

.result-body {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-top: none;
    border-radius: 0 0 14px 14px;
    padding: 20px;
}

.result-section {
    margin-bottom: 16px;
    padding-bottom: 16px;
    border-bottom: 1px solid var(--border-color);
}

.result-section:last-child { margin-bottom: 0; padding-bottom: 0; border-bottom: none; }

.result-section-title {
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 12px;
}

.field-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }

.field-item {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 10px;
    padding: 12px 14px;
}

.field-label { font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 4px; }
.field-value { color: var(--text-primary); font-size: 0.95rem; word-break: break-all; }

.field-highlight {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(168, 85, 247, 0.1));
    border-color: rgba(99, 102, 241, 0.2);
}
.field-highlight .field-value { color: #a5b4fc; font-family: 'JetBrains Mono', monospace; }

.field-tracking {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(34, 211, 238, 0.1));
    border-color: rgba(16, 185, 129, 0.2);
}
.field-tracking .field-value { color: #6ee7b7; font-family: 'JetBrains Mono', monospace; }

.field-status {
    background: linear-gradient(135deg, rgba(236, 72, 153, 0.1), rgba(168, 85, 247, 0.1));
    border-color: rgba(236, 72, 153, 0.2);
}
.field-status .field-value { color: #f9a8d4; font-weight: 600; }

.no-results { text-align: center; padding: 60px 20px; color: var(--text-muted); }
.no-results h2 { color: var(--text-secondary); margin-bottom: 10px; }

.stTextInput input {
    background: var(--bg-card) !important;
    border: 2px solid var(--border-color) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
    padding: 12px 16px !important;
}

.stTextInput input:focus {
    border-color: var(--accent-blue) !important;
    box-shadow: 0 0 20px rgba(99, 102, 241, 0.2) !important;
}

.stButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%) !important;
    border: none !important;
    border-radius: 12px !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 12px 24px !important;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 25px rgba(168, 85, 247, 0.4) !important;
}

[data-testid="stMetric"] {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 14px;
    padding: 18px 20px;
}

[data-testid="stMetricLabel"] { color: var(--text-secondary) !important; }
[data-testid="stMetricValue"] { color: var(--text-primary) !important; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #12121a 0%, #0a0a0f 100%) !important;
}

[data-testid="stSidebar"] > div:first-child {
    background: transparent !important;
}

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: linear-gradient(180deg, var(--accent-blue), var(--accent-purple)); border-radius: 3px; }

hr { border: none; height: 1px; background: linear-gradient(90deg, transparent, var(--border-color), transparent); margin: 20px 0; }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# =============================================================================
# DATA SOURCES
# =============================================================================

DATA_SOURCES = {
    "ECL QC Center": {
        "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSCiZ1MdPMyVAzBqmBmp3Ch8sfefOp_kfPk2RSfMv3bxRD_qccuwaoM7WTVsieKJbA3y3DF41tUxb3T/pub?gid=0&single=true&output=csv",
        "order_col": "Fleek ID", "partner": "ECL", "type": "QC Center", "icon": "🟠"
    },
    "ECL Zone": {
        "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSCiZ1MdPMyVAzBqmBmp3Ch8sfefOp_kfPk2RSfMv3bxRD_qccuwaoM7WTVsieKJbA3y3DF41tUxb3T/pub?gid=928309568&single=true&output=csv",
        "order_col": 0, "partner": "ECL", "type": "Zone", "icon": "🟠"
    },
    "GE QC Center": {
        "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQjCPd8bUpx59Sit8gMMXjVKhIFA_f-W9Q4mkBSWulOTg4RGahcVXSD4xZiYBAcAH6eO40aEQ9IEEXj/pub?gid=710036753&single=true&output=csv",
        "order_col": "Order Num", "partner": "GE", "type": "QC Center", "icon": "🔵"
    },
    "GE Zone": {
        "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQjCPd8bUpx59Sit8gMMXjVKhIFA_f-W9Q4mkBSWulOTg4RGahcVXSD4xZiYBAcAH6eO40aEQ9IEEXj/pub?gid=10726393&single=true&output=csv",
        "order_col": 0, "partner": "GE", "type": "Zone", "icon": "🔵"
    },
    "APX": {
        "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRDEzAMUwnFZ7aoThGoMERtxxsll2kfEaSpa9ksXIx6sqbdMncts6Go2d5mKKabepbNXDSoeaUlk-mP/pub?gid=0&single=true&output=csv",
        "order_col": "Fleek ID", "partner": "APX", "type": None, "icon": "🟣"
    },
    "Kerry": {
        "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vTZyLyZpVJz9sV5eT4Srwo_KZGnYggpRZkm2ILLYPQKSpTKkWfP9G5759h247O4QEflKCzlQauYsLKI/pub?gid=0&single=true&output=csv",
        "order_col": "_Order", "partner": "Kerry", "type": None, "icon": "🟢"
    }
}

# =============================================================================
# DISPLAY FIELDS (Pieces REMOVED)
# =============================================================================

DISPLAY_FIELDS = {
    "📋 Order Information": [
        {"name": "Order Number", "aliases": ["order#", "order", "fleek id", "_order", "order no", "order num", "order number"], "style": "highlight"},
        {"name": "Handover Date", "aliases": ["date", "fleek handover date", "airport handover date", "ge entry date", "handover date"], "style": "normal"},
        {"name": "Service", "aliases": ["services", "service", "partner", "3pl"], "style": "normal"},
        {"name": "QC Status", "aliases": ["qc status", "qc_status", "status", "qc"], "style": "normal"},
    ],
    "📦 Shipment Details": [
        {"name": "Boxes", "aliases": ["box_count", "boxes", "box count", "no of boxes", "n.o of boxes", "no. of boxes"], "style": "normal"},
        {"name": "Weight (kg)", "aliases": ["weight_kgs", "weight (kg)", "weight", "order net weight", "chargeable weight", "total weight"], "style": "normal"},
    ],
    "🚚 Tracking & Delivery": [
        {"name": "AWB", "aliases": ["airway_bill", "awb", "hawb", "mawb", "apx awb number", "kerry awb number", "ge awb", "awb number"], "style": "highlight"},
        {"name": "Tracking ID", "aliases": ["courier_tracking_ids", "tracking id", "tracking_id", "tracking", "ge comment / tracking", "tracking number"], "style": "tracking"},
        {"name": "Courier", "aliases": ["courier_service", "courier", "carrier", "courier name"], "style": "normal"},
    ],
    "👤 Customer Info": [
        {"name": "Customer Name", "aliases": ["consignee", "customer name", "customer_name", "customer", "name", "receiver"], "style": "normal"},
        {"name": "Destination", "aliases": ["destination", "country", "city", "delivery city", "dest"], "style": "normal"},
    ],
}

# =============================================================================
# DATA FUNCTIONS
# =============================================================================

def fetch_source(name, config, timeout=120):
    for attempt in range(3):
        try:
            resp = requests.get(config["url"], timeout=timeout)
            resp.raise_for_status()
            df = pd.read_csv(StringIO(resp.text))
            order_col = config["order_col"]
            if isinstance(order_col, int):
                order_col = df.columns[order_col]
            df["_search_col"] = df[order_col].astype(str).str.lower().str.strip()
            return {"name": name, "df": df, "order_col": order_col, "partner": config["partner"], "icon": config["icon"], "type": config["type"], "error": None}
        except Exception as e:
            if attempt == 2:
                return {"name": name, "df": pd.DataFrame(), "partner": config["partner"], "icon": config["icon"], "type": config["type"], "error": str(e)}
            time.sleep(1)

def initialize_data():
    results = {}
    errors = []
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {executor.submit(fetch_source, n, c): n for n, c in DATA_SOURCES.items()}
        for future in as_completed(futures):
            res = future.result()
            if res.get("error"):
                errors.append(f"{res['name']}: {res['error']}")
            results[res["name"]] = res
    st.session_state.all_data = results
    st.session_state.load_errors = errors
    st.session_state.total_rows = sum(len(d.get("df", pd.DataFrame())) for d in results.values())
    st.session_state.data_loaded = True

def is_valid(val):
    if val is None or pd.isna(val):
        return False
    return str(val).strip().lower() not in ["", "nan", "none", "na", "n/a", "-", "null"]

def get_field_value(data, aliases):
    data_lower = {k.lower().strip(): v for k, v in data.items()}
    for alias in aliases:
        if alias.lower() in data_lower:
            val = data_lower[alias.lower()]
            if is_valid(val):
                return str(val)
    return None

def get_live_status_from_kerry(order_id):
    kerry = st.session_state.all_data.get("Kerry", {})
    df = kerry.get("df", pd.DataFrame())
    if df.empty:
        return None
    matches = df[df["_search_col"] == order_id.lower().strip()]
    if len(matches) > 0:
        row = matches.iloc[0]
        for alias in ["latest status", "latest_status", "live status", "current status", "delivery status"]:
            for col in df.columns:
                if col.lower().strip() == alias:
                    val = row[col]
                    if is_valid(val):
                        return str(val)
    return None

def instant_search(order_ids):
    results = []
    for oid in order_ids:
        term = oid.lower().strip()
        for name, data in st.session_state.all_data.items():
            df = data.get("df", pd.DataFrame())
            if df.empty:
                continue
            matches = df[df["_search_col"] == term]
            for _, row in matches.iterrows():
                live_status = get_live_status_from_kerry(oid)
                results.append({
                    "source": name,
                    "partner": data.get("partner", "Unknown"),
                    "icon": data.get("icon", "⚪"),
                    "type": data.get("type", ""),
                    "order_id": oid,
                    "data": row.to_dict(),
                    "live_status": live_status
                })
    return results

# =============================================================================
# UI COMPONENTS
# =============================================================================

def render_result_card(result):
    partner = result["partner"]
    icon = result["icon"]
    source = result["source"]
    data = result["data"]
    live_status = result.get("live_status")
    partner_class = partner.lower()
    
    st.markdown(f"""
    <div class="result-header result-header-{partner_class}">
        <div class="result-partner">
            <span class="result-partner-icon">{icon}</span>
            <div>
                <div class="result-partner-name">{partner}</div>
                <div class="result-partner-type">{source}</div>
            </div>
        </div>
        <div class="result-order">#{result['order_id']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    body_html = '<div class="result-body">'
    
    for section_name, fields in DISPLAY_FIELDS.items():
        section_fields = []
        for field in fields:
            val = get_field_value(data, field["aliases"])
            if val:
                section_fields.append((field["name"], val, field["style"]))
        
        if section_fields:
            body_html += f'<div class="result-section"><div class="result-section-title">{section_name}</div><div class="field-grid">'
            for name, val, style in section_fields:
                style_class = f"field-{style}" if style != "normal" else ""
                body_html += f'<div class="field-item {style_class}"><div class="field-label">{name}</div><div class="field-value">{val}</div></div>'
            body_html += '</div></div>'
    
    if live_status:
        body_html += f'''
        <div class="result-section">
            <div class="result-section-title">📡 Live Status</div>
            <div class="field-grid">
                <div class="field-item field-status"><div class="field-label">Latest Status</div><div class="field-value">{live_status}</div></div>
                <div class="field-item"><div class="field-label">Source</div><div class="field-value">Kerry Logistics</div></div>
            </div>
        </div>
        '''
    
    body_html += '</div>'
    st.markdown(body_html, unsafe_allow_html=True)

def search_page():
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <div class="header-icon">🔎</div>
        <div class="premium-header">TrackMaster Pro</div>
        <div class="header-subtitle">Intelligent Shipment Tracking</div>
        <div class="header-line"></div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([5, 1])
    with col1:
        search_input = st.text_input("Search", placeholder="Enter order ID (e.g., 122129_34)", label_visibility="collapsed")
    with col2:
        st.button("Search", use_container_width=True, type="primary")
    
    if search_input:
        import re
        order_ids = [x.strip() for x in re.split(r'[\n,\t\s]+', search_input) if x.strip()]
        if order_ids:
            start = time.time()
            results = instant_search(order_ids)
            elapsed = (time.time() - start) * 1000
            
            st.markdown(f'<span class="speed-badge">⚡ {elapsed:.1f}ms</span>', unsafe_allow_html=True)
            
            if results:
                for result in results:
                    render_result_card(result)
            else:
                st.markdown('<div class="no-results"><h2>🔍 No Results Found</h2><p>Try a different order ID</p></div>', unsafe_allow_html=True)
            return
    
    counts = {"ECL": 0, "GE": 0, "APX": 0, "Kerry": 0}
    for name, data in st.session_state.all_data.items():
        partner = data.get("partner", "")
        if partner in counts:
            counts[partner] += len(data.get("df", pd.DataFrame()))
    
    st.markdown(f"""
    <div class="partner-cards">
        <div class="partner-card partner-ecl"><div class="partner-icon">🟠</div><div class="partner-name">ECL</div><div class="partner-count">{counts['ECL']:,} orders</div></div>
        <div class="partner-card partner-ge"><div class="partner-icon">🔵</div><div class="partner-name">GE</div><div class="partner-count">{counts['GE']:,} orders</div></div>
        <div class="partner-card partner-apx"><div class="partner-icon">🟣</div><div class="partner-name">APX</div><div class="partner-count">{counts['APX']:,} orders</div></div>
        <div class="partner-card partner-kerry"><div class="partner-icon">🟢</div><div class="partner-name">Kerry</div><div class="partner-count">{counts['Kerry']:,} orders</div></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="recent-section">
        <div class="section-title">🕐 Recent Searches</div>
        <div class="empty-state"><div class="empty-state-icon">🔍</div><div>Your recent searches will appear here</div></div>
    </div>
    """, unsafe_allow_html=True)

def data_page(source_name):
    data = st.session_state.all_data.get(source_name, {})
    df = data.get("df", pd.DataFrame())
    partner = data.get("partner", "Unknown")
    icon = data.get("icon", "⚪")
    source_type = data.get("type", "")
    
    st.markdown(f"## {icon} {source_name}")
    if source_type:
        st.caption(f"Partner: {partner} | Type: {source_type}")
    else:
        st.caption(f"Partner: {partner}")
    
    if df.empty:
        st.error("No data available")
        return
    
    col1, col2, col3 = st.columns(3)
    col1.metric("📦 Total Rows", f"{len(df):,}")
    col2.metric("📊 Columns", len(df.columns))
    col3.metric("🏢 Partner", partner)
    
    st.markdown("---")
    
    filter_text = st.text_input("🔍 Filter data...", key=f"filter_{source_name}")
    display_df = df.drop(columns=["_search_col"], errors="ignore")
    
    if filter_text:
        mask = display_df.astype(str).apply(lambda x: x.str.contains(filter_text, case=False, na=False)).any(axis=1)
        display_df = display_df[mask]
    
    st.dataframe(display_df, use_container_width=True, height=500)
    st.download_button("📥 Download CSV", display_df.to_csv(index=False), f"{source_name.replace(' ', '_')}.csv", "text/csv", use_container_width=True)

# =============================================================================
# MAIN
# =============================================================================

def main():
    # Initialize data first if not loaded
    if "data_loaded" not in st.session_state:
        st.markdown("""
        <div style="text-align: center; padding: 100px;">
            <div class="header-icon">🔎</div>
            <div class="premium-header">TrackMaster Pro</div>
            <div class="status-badge loading">🔄 Loading data...</div>
            <p style="color: #8892b0; margin-top: 20px;">Connecting to all sources...</p>
        </div>
        """, unsafe_allow_html=True)
        initialize_data()
        st.rerun()
    
    # SIDEBAR - Always render
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 15px 0;">
            <div style="font-size: 2.5rem;">🔎</div>
            <div style="font-size: 1.3rem; font-weight: 700; background: linear-gradient(135deg, #6366f1, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">TrackMaster Pro</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        page = st.radio(
            "📍 Navigation",
            ["🔍 Global Search", "🟠 ECL QC", "🟠 ECL Zone", "🔵 GE QC", "🔵 GE Zone", "🟣 APX", "🟢 Kerry"],
        )
        
        st.markdown("---")
        
        st.markdown(f'<div class="status-badge">✅ {st.session_state.total_rows:,} rows</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        if st.button("🔄 Reload Data", use_container_width=True):
            del st.session_state.data_loaded
            st.rerun()
        
        if st.session_state.get("load_errors"):
            with st.expander("⚠️ Warnings"):
                for err in st.session_state.load_errors:
                    st.warning(err)
    
    # MAIN CONTENT
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
