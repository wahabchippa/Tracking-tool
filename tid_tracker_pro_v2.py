import streamlit as st
import pandas as pd
import requests
from io import StringIO
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# ═══════════════════════════════════════════════════════════════════════════════
# 🎨 PAGE CONFIG & CLASSY THEME
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="TrackMaster Pro",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Classy Theme
CUSTOM_CSS = """
<style>
/* Import Premium Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* Root Variables - Classy Dark Theme */
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
    --accent-cyan: #22d3ee;
}

/* Global Background */
.stApp {
    background: var(--bg-primary);
    background-image: 
        radial-gradient(ellipse at 20% 20%, rgba(99, 102, 241, 0.06) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 80%, rgba(168, 85, 247, 0.06) 0%, transparent 50%);
    font-family: 'Inter', sans-serif;
}

/* Hide Streamlit Defaults */
#MainMenu, footer, header {visibility: hidden;}
.stDeployButton {display: none;}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--bg-secondary) 0%, var(--bg-primary) 100%);
    border-right: 1px solid var(--border-color);
}

section[data-testid="stSidebar"] .stRadio > div > label {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 10px;
    padding: 12px 16px !important;
    margin: 4px 0;
    color: var(--text-primary) !important;
    transition: all 0.3s ease;
}

section[data-testid="stSidebar"] .stRadio > div > label:hover {
    background: var(--bg-hover);
    border-color: var(--accent-blue);
    transform: translateX(4px);
    box-shadow: 0 0 20px rgba(99, 102, 241, 0.2);
}

/* Text Area */
.stTextArea textarea {
    background: var(--bg-card) !important;
    border: 2px solid var(--border-color) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
    font-family: 'JetBrains Mono', monospace !important;
    padding: 14px 18px !important;
    transition: all 0.3s ease !important;
}

.stTextArea textarea:focus {
    border-color: var(--accent-blue) !important;
    box-shadow: 0 0 25px rgba(99, 102, 241, 0.25) !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%) !important;
    border: none !important;
    border-radius: 12px !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 12px 28px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 20px rgba(99, 102, 241, 0.3) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) scale(1.02) !important;
    box-shadow: 0 6px 30px rgba(168, 85, 247, 0.4) !important;
}

/* Metrics - Glass Effect */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 18px 22px;
}

[data-testid="stMetricLabel"] {
    color: var(--text-secondary) !important;
}

[data-testid="stMetricValue"] {
    color: var(--text-primary) !important;
    background: linear-gradient(135deg, #6366f1, #a855f7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* DataFrames */
.stDataFrame {
    border-radius: 12px;
    border: 1px solid var(--border-color);
}

/* Text Input */
.stTextInput input {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    padding: 10px 14px !important;
}

.stTextInput input:focus {
    border-color: var(--accent-blue) !important;
    box-shadow: 0 0 15px rgba(99, 102, 241, 0.2) !important;
}

/* Download Button */
.stDownloadButton > button {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    color: var(--text-primary) !important;
}

.stDownloadButton > button:hover {
    border-color: var(--accent-green) !important;
    box-shadow: 0 0 15px rgba(16, 185, 129, 0.3) !important;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}

::-webkit-scrollbar-track {
    background: var(--bg-primary);
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, var(--accent-blue), var(--accent-purple));
    border-radius: 3px;
}

/* Alerts */
.stAlert {
    border-radius: 12px !important;
}

/* Divider */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border-color), transparent);
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 🎯 PREMIUM HEADER
# ═══════════════════════════════════════════════════════════════════════════════

def render_header():
    """Render premium animated header"""
    header_html = """
    <style>
    .main-header {
        text-align: center;
        padding: 20px 0 30px 0;
    }
    
    .header-icon {
        font-size: 3.5rem;
        display: inline-block;
        animation: float 3s ease-in-out infinite;
        filter: drop-shadow(0 0 15px rgba(99, 102, 241, 0.5));
    }
    
    .header-title {
        font-family: 'Inter', sans-serif;
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 35%, #ec4899 70%, #22d3ee 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 10px 0 0 0;
        letter-spacing: -1px;
    }
    
    .header-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        color: #9898b0;
        margin-top: 8px;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    
    .header-line {
        width: 100px;
        height: 3px;
        background: linear-gradient(90deg, #6366f1, #a855f7, #ec4899);
        border-radius: 2px;
        margin: 20px auto 0 auto;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
    }
    </style>
    
    <div class="main-header">
        <div class="header-icon">🔎</div>
        <h1 class="header-title">TrackMaster Pro</h1>
        <p class="header-subtitle">Intelligent Shipment Tracking</p>
        <div class="header-line"></div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)


def render_sidebar_header():
    """Render compact sidebar header"""
    sidebar_html = """
    <style>
    .sidebar-header {
        text-align: center;
        padding: 10px 0 15px 0;
    }
    
    .sidebar-icon {
        font-size: 2rem;
        filter: drop-shadow(0 0 10px rgba(99, 102, 241, 0.4));
    }
    
    .sidebar-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6366f1, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 5px 0 0 0;
    }
    </style>
    
    <div class="sidebar-header">
        <div class="sidebar-icon">🔎</div>
        <div class="sidebar-title">TrackMaster Pro</div>
    </div>
    """
    st.markdown(sidebar_html, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# 🗃️ DATA SOURCES CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

DATA_SOURCES = {
    "🟠 ECL QC Center": {
        "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSCiZ1MdPMyVAzBqmBmp3Ch8sfefOp_kfPk2RSfMv3bxRD_qccuwaoM7WTVsieKJbA3y3DF41tUxb3T/pub?gid=0&single=true&output=csv",
        "order_col": "Fleek ID",
        "partner": "ECL",
        "type": "QC Center",
        "icon": "🟠"
    },
    "🟠 ECL Zone": {
        "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSCiZ1MdPMyVAzBqmBmp3Ch8sfefOp_kfPk2RSfMv3bxRD_qccuwaoM7WTVsieKJbA3y3DF41tUxb3T/pub?gid=928309568&single=true&output=csv",
        "order_col": 0,
        "partner": "ECL",
        "type": "Zone",
        "icon": "🟠"
    },
    "🔵 GE QC Center": {
        "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQjCPd8bUpx59Sit8gMMXjVKhIFA_f-W9Q4mkBSWulOTg4RGahcVXSD4xZiYBAcAH6eO40aEQ9IEEXj/pub?gid=710036753&single=true&output=csv",
        "order_col": "Order Num",
        "partner": "GE",
        "type": "QC Center",
        "icon": "🔵"
    },
    "🔵 GE Zone": {
        "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQjCPd8bUpx59Sit8gMMXjVKhIFA_f-W9Q4mkBSWulOTg4RGahcVXSD4xZiYBAcAH6eO40aEQ9IEEXj/pub?gid=10726393&single=true&output=csv",
        "order_col": 0,
        "partner": "GE",
        "type": "Zone",
        "icon": "🔵"
    },
    "🟣 APX": {
        "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRDEzAMUwnFZ7aoThGoMERtxxsll2kfEaSpa9ksXIx6sqbdMncts6Go2d5mKKabepbNXDSoeaUlk-mP/pub?gid=0&single=true&output=csv",
        "order_col": "Fleek ID",
        "partner": "APX",
        "type": "Warehouse",
        "icon": "🟣"
    },
    "🟢 Kerry": {
        "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vTZyLyZpVJz9sV5eT4Srwo_KZGnYggpRZkm2ILLYPQKSpTKkWfP9G5759h247O4QEflKCzlQauYsLKI/pub?gid=0&single=true&output=csv",
        "order_col": "_Order",
        "partner": "Kerry",
        "type": "Logistics",
        "icon": "🟢"
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
# 📋 DISPLAY FIELDS (Pieces REMOVED)
# ═══════════════════════════════════════════════════════════════════════════════

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

# ═══════════════════════════════════════════════════════════════════════════════
# ⚙️ DATA LOADING FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def fetch_single_source(name, config, timeout=120):
    """Fetch a single data source"""
    for attempt in range(3):
        try:
            response = requests.get(config["url"], timeout=timeout)
            response.raise_for_status()
            df = pd.read_csv(StringIO(response.text))
            
            order_col = config["order_col"]
            if isinstance(order_col, int):
                order_col = df.columns[order_col]
            
            df["_search_col"] = df[order_col].astype(str).str.lower().str.strip()
            
            return {
                "name": name,
                "df": df,
                "order_col": order_col,
                "partner": config["partner"],
                "type": config["type"],
                "icon": config["icon"],
                "error": None
            }
        except Exception as e:
            if attempt == 2:
                return {"name": name, "df": None, "error": str(e)}
            time.sleep(1)


def load_all_data():
    """Load all data sources in parallel"""
    results = {}
    errors = []
    
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {executor.submit(fetch_single_source, name, config): name 
                   for name, config in DATA_SOURCES.items()}
        
        for future in as_completed(futures):
            result = future.result()
            if result["error"]:
                errors.append(f"{result['name']}: {result['error']}")
            else:
                results[result["name"]] = result
    
    return results, errors


def initialize_data():
    """Initialize data into session state"""
    if "data_loaded" not in st.session_state:
        st.session_state.data_loaded = False
    
    if not st.session_state.data_loaded:
        with st.spinner("🚀 Loading data..."):
            data, errors = load_all_data()
            st.session_state.all_data = data
            st.session_state.load_errors = errors
            st.session_state.total_rows = sum(len(d["df"]) for d in data.values() if d.get("df") is not None)
            st.session_state.data_loaded = True


# ═══════════════════════════════════════════════════════════════════════════════
# 🔍 SEARCH & HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def parse_order_ids(input_text):
    """Parse multiple order IDs"""
    import re
    order_ids = re.split(r'[,\n\t\s]+', input_text.strip())
    return [oid.strip() for oid in order_ids if oid.strip()]


def is_valid(val):
    """Check if value is valid"""
    if val is None or pd.isna(val):
        return False
    str_val = str(val).strip().lower()
    return str_val not in ["", "nan", "none", "na", "n/a", "-", "null"]


def get_field_value(data, aliases):
    """Get field value by aliases"""
    data_lower = {k.lower().strip(): v for k, v in data.items()}
    for alias in aliases:
        if alias.lower() in data_lower:
            val = data_lower[alias.lower()]
            if is_valid(val):
                return str(val)
    return None


def get_live_status_from_kerry(order_id):
    """Fetch live status from Kerry sheet for ANY order"""
    kerry_data = st.session_state.all_data.get("🟢 Kerry")
    if kerry_data is None or kerry_data.get("df") is None:
        return None
    
    df = kerry_data["df"]
    search_term = order_id.lower().strip()
    matches = df[df["_search_col"] == search_term]
    
    if len(matches) > 0:
        row = matches.iloc[0]
        status_aliases = ["latest status", "latest_status", "live status", "current status", "status update", "delivery status"]
        for alias in status_aliases:
            for col in df.columns:
                if col.lower().strip() == alias:
                    val = row[col]
                    if is_valid(val):
                        return str(val)
    return None


def instant_search(order_ids):
    """Search all loaded data"""
    results = []
    
    for order_id in order_ids:
        search_term = order_id.lower().strip()
        
        for source_name, source_data in st.session_state.all_data.items():
            df = source_data.get("df")
            if df is None:
                continue
            
            matches = df[df["_search_col"] == search_term]
            
            for _, row in matches.iterrows():
                # Get live status from Kerry for ALL orders
                live_status = get_live_status_from_kerry(order_id)
                
                results.append({
                    "source": source_name,
                    "partner": source_data["partner"],
                    "type": source_data["type"],
                    "icon": source_data["icon"],
                    "order_id": order_id,
                    "data": row.to_dict(),
                    "live_status": live_status
                })
    
    return results


# ═══════════════════════════════════════════════════════════════════════════════
# 🎨 RESULT CARD RENDERING (Original Style with Classy Colors)
# ═══════════════════════════════════════════════════════════════════════════════

def get_partner_color(partner):
    """Get color for partner"""
    colors = {
        "ECL": "#f97316",
        "GE": "#6366f1", 
        "APX": "#a855f7",
        "Kerry": "#10b981"
    }
    return colors.get(partner, "#6366f1")


def render_result_card(result):
    """Render result card using native Streamlit"""
    data = result["data"]
    partner = result["partner"]
    source = result["source"]
    order_id = result["order_id"]
    icon = result["icon"]
    live_status = result.get("live_status")
    color = get_partner_color(partner)
    
    # Card Header
    header_html = f"""
    <div style="
        background: linear-gradient(135deg, {color}dd, {color}99);
        border-radius: 12px 12px 0 0;
        padding: 16px 20px;
        margin-top: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    ">
        <div style="display: flex; align-items: center; gap: 12px;">
            <span style="font-size: 1.8rem;">{icon}</span>
            <div>
                <div style="color: white; font-weight: 700; font-size: 1.2rem;">{partner}</div>
                <div style="color: rgba(255,255,255,0.8); font-size: 0.85rem;">{source}</div>
            </div>
        </div>
        <div style="
            background: rgba(255,255,255,0.2);
            padding: 8px 16px;
            border-radius: 8px;
            color: white;
            font-family: monospace;
            font-weight: 600;
        ">#{order_id}</div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)
    
    # Card Body
    with st.container():
        body_style = """
        <style>
        .card-body-container {
            background: #16161f;
            border: 1px solid #2a2a3d;
            border-top: none;
            border-radius: 0 0 12px 12px;
            padding: 20px;
            margin-bottom: 16px;
        }
        </style>
        """
        st.markdown(body_style, unsafe_allow_html=True)
        
        # Render sections
        for section_name, fields in DISPLAY_FIELDS.items():
            section_values = []
            for field in fields:
                value = get_field_value(data, field["aliases"])
                if value:
                    section_values.append((field["name"], value, field["style"]))
            
            if section_values:
                st.markdown(f"**{section_name}**")
                cols = st.columns(2)
                for idx, (name, value, style) in enumerate(section_values):
                    with cols[idx % 2]:
                        if style == "highlight":
                            st.markdown(f"<small style='color:#6b6b82;'>{name}</small>", unsafe_allow_html=True)
                            st.code(value, language=None)
                        elif style == "tracking":
                            st.markdown(f"<small style='color:#6b6b82;'>{name}</small>", unsafe_allow_html=True)
                            st.success(value)
                        else:
                            st.markdown(f"<small style='color:#6b6b82;'>{name}</small>", unsafe_allow_html=True)
                            st.text(value)
                st.markdown("---")
        
        # Live Status Section (from Kerry for ALL orders)
        if live_status:
            st.markdown("**📡 Live Status**")
            cols = st.columns(2)
            with cols[0]:
                st.markdown(f"<small style='color:#6b6b82;'>Latest Status</small>", unsafe_allow_html=True)
                st.info(live_status)
            with cols[1]:
                st.markdown(f"<small style='color:#6b6b82;'>Source</small>", unsafe_allow_html=True)
                st.text("Kerry Logistics")


# ═══════════════════════════════════════════════════════════════════════════════
# 🏠 MAIN PAGES
# ═══════════════════════════════════════════════════════════════════════════════

def render_home_page():
    """Render home/search page"""
    render_header()
    
    # Stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Total Records", f"{st.session_state.total_rows:,}")
    with col2:
        st.metric("🔗 Data Sources", len(st.session_state.all_data))
    with col3:
        st.metric("⚡ Speed", "< 50ms")
    
    st.markdown("---")
    
    # Search
    search_input = st.text_area(
        "🔍 Enter Order IDs",
        placeholder="Enter order IDs (comma or newline separated)...",
        height=100
    )
    
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        search_btn = st.button("🚀 Search", use_container_width=True)
    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.session_state.data_loaded = False
            st.rerun()
    
    if search_btn and search_input.strip():
        order_ids = parse_order_ids(search_input)
        if order_ids:
            start = time.time()
            results = instant_search(order_ids)
            elapsed = (time.time() - start) * 1000
            
            st.markdown("---")
            
            if results:
                st.success(f"✨ Found **{len(results)}** result(s) in **{elapsed:.1f}ms**")
                for result in results:
                    render_result_card(result)
            else:
                st.warning("🔍 No results found.")
    
    if st.session_state.load_errors:
        with st.expander("⚠️ Load Warnings"):
            for err in st.session_state.load_errors:
                st.warning(err)


def render_data_page(source_name):
    """Render data source page"""
    source_data = st.session_state.all_data.get(source_name)
    
    if not source_data or source_data.get("df") is None:
        st.error(f"❌ Data not available for {source_name}")
        return
    
    df = source_data["df"]
    partner = source_data["partner"]
    color = get_partner_color(partner)
    
    # Header
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {color}dd, {color}99);
        border-radius: 12px;
        padding: 20px 28px;
        margin-bottom: 20px;
    ">
        <h2 style="color: white; margin: 0;">{source_data["icon"]} {partner} - {source_data["type"]}</h2>
        <p style="color: rgba(255,255,255,0.8); margin: 5px 0 0 0;">Data Management</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📋 Records", f"{len(df):,}")
    with col2:
        st.metric("📊 Columns", len(df.columns))
    with col3:
        st.metric("🔗 Partner", partner)
    
    # Filter
    filter_text = st.text_input("🔍 Filter...", placeholder="Type to filter...")
    
    if filter_text:
        mask = df.astype(str).apply(lambda x: x.str.contains(filter_text, case=False, na=False)).any(axis=1)
        filtered_df = df[mask]
    else:
        filtered_df = df
    
    # Table
    display_df = filtered_df.drop(columns=["_search_col"], errors="ignore")
    st.dataframe(display_df, use_container_width=True, height=500)
    
    # Download
    csv = display_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV", csv, f"{partner}_{source_data['type']}.csv", "text/csv", use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# 🚀 MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    initialize_data()
    
    with st.sidebar:
        render_sidebar_header()
        st.markdown("---")
        
        nav_options = ["🏠 Global Search"] + list(DATA_SOURCES.keys())
        selected = st.radio("Navigation", nav_options, label_visibility="collapsed")
    
    if selected == "🏠 Global Search":
        render_home_page()
    else:
        render_data_page(selected)


if __name__ == "__main__":
    main()
