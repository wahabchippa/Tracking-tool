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
# PREMIUM CSS STYLING
# =============================================================================

st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    /* Hide default header */
    header[data-testid="stHeader"] {
        background: transparent;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #0f0f1a 100%);
        border-right: 1px solid #2d2d44;
    }
    
    /* Premium Header */
    .premium-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem;
        font-weight: 800;
        text-align: right;
        padding: 10px 0;
        letter-spacing: -1px;
    }
    
    .header-subtitle {
        color: #8892b0;
        font-size: 1rem;
        text-align: right;
        margin-top: -10px;
        padding-bottom: 20px;
    }
    
    /* Search container */
    .search-container {
        background: linear-gradient(145deg, #1e1e32 0%, #2a2a40 100%);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid #3d3d5c;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        margin: 20px 0;
    }
    
    .search-title {
        color: #a8b2d1;
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 15px;
    }
    
    /* Stats cards */
    .stats-container {
        display: flex;
        gap: 15px;
        margin: 25px 0;
    }
    
    .stat-card {
        background: linear-gradient(145deg, #1e1e32 0%, #252540 100%);
        border-radius: 16px;
        padding: 20px 25px;
        border: 1px solid #3d3d5c;
        flex: 1;
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.2);
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .stat-label {
        color: #8892b0;
        font-size: 0.85rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 5px;
    }
    
    /* Result cards */
    .result-card {
        background: linear-gradient(145deg, #1e1e32 0%, #252540 100%);
        border-radius: 16px;
        padding: 25px;
        margin: 15px 0;
        border-left: 4px solid #667eea;
        border-top: 1px solid #3d3d5c;
        border-right: 1px solid #3d3d5c;
        border-bottom: 1px solid #3d3d5c;
    }
    
    .result-header {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 20px;
        padding-bottom: 15px;
        border-bottom: 1px solid #3d3d5c;
    }
    
    .partner-badge {
        padding: 8px 16px;
        border-radius: 25px;
        font-weight: 600;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .partner-ecl { background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white; }
    .partner-ge { background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white; }
    .partner-apx { background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); color: white; }
    .partner-kerry { background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; }
    
    .order-id-display {
        color: #e6f1ff;
        font-size: 1.3rem;
        font-weight: 600;
    }
    
    .source-tag {
        color: #8892b0;
        font-size: 0.9rem;
        margin-left: auto;
    }
    
    /* Field grid */
    .field-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 15px;
    }
    
    .field-item {
        background: rgba(255,255,255,0.03);
        border-radius: 12px;
        padding: 15px;
        border: 1px solid #2d2d44;
    }
    
    .field-label {
        color: #8892b0;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    .field-value {
        color: #e6f1ff;
        font-size: 1rem;
        font-weight: 500;
        word-break: break-word;
    }
    
    .field-value.empty {
        color: #4a4a6a;
        font-style: italic;
    }
    
    /* Data status badge */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 10px 20px;
        border-radius: 30px;
        font-weight: 600;
        font-size: 0.9rem;
        margin: 10px 0;
    }
    
    .status-badge.loading {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    }
    
    /* Speed badge */
    .speed-badge {
        background: rgba(102, 126, 234, 0.2);
        color: #667eea;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }
    
    /* Sidebar menu */
    .sidebar-menu {
        padding: 10px 0;
    }
    
    .menu-item {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 15px 20px;
        margin: 5px 0;
        border-radius: 12px;
        color: #8892b0;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .menu-item:hover, .menu-item.active {
        background: rgba(102, 126, 234, 0.15);
        color: #667eea;
    }
    
    .menu-icon {
        font-size: 1.2rem;
    }
    
    /* Custom input styling */
    .stTextInput > div > div > input {
        background: #1a1a2e !important;
        border: 2px solid #3d3d5c !important;
        border-radius: 12px !important;
        color: #e6f1ff !important;
        padding: 15px 20px !important;
        font-size: 1rem !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 15px 30px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* No results message */
    .no-results {
        text-align: center;
        padding: 60px;
        color: #8892b0;
    }
    
    .no-results-icon {
        font-size: 4rem;
        margin-bottom: 20px;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(145deg, #1e1e32 0%, #252540 100%) !important;
        border-radius: 12px !important;
        border: 1px solid #3d3d5c !important;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Tabs styling override */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.05);
        border-radius: 10px;
        padding: 10px 20px;
        color: #8892b0;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
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
        "partner": "ECL"
    },
    "ECL Zone": {
        "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSCiZ1MdPMyVAzBqmBmp3Ch8sfefOp_kfPk2RSfMv3bxRD_qccuwaoM7WTVsieKJbA3y3DF41tUxb3T/pub?gid=928309568&single=true&output=csv",
        "order_col": 0,
        "partner": "ECL"
    },
    "GE QC Center": {
        "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQjCPd8bUpx59Sit8gMMXjVKhIFA_f-W9Q4mkBSWulOTg4RGahcVXSD4xZiYBAcAH6eO40aEQ9IEEXj/pub?gid=710036753&single=true&output=csv",
        "order_col": "Order Num",
        "partner": "GE"
    },
    "GE Zone": {
        "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQjCPd8bUpx59Sit8gMMXjVKhIFA_f-W9Q4mkBSWulOTg4RGahcVXSD4xZiYBAcAH6eO40aEQ9IEEXj/pub?gid=10726393&single=true&output=csv",
        "order_col": 0,
        "partner": "GE"
    },
    "APX": {
        "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRDEzAMUwnFZ7aoThGoMERtxxsll2kfEaSpa9ksXIx6sqbdMncts6Go2d5mKKabepbNXDSoeaUlk-mP/pub?gid=0&single=true&output=csv",
        "order_col": "Fleek ID",
        "partner": "APX"
    },
    "Kerry": {
        "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vTZyLyZpVJz9sV5eT4Srwo_KZGnYggpRZkm2ILLYPQKSpTKkWfP9G5759h247O4QEflKCzlQauYsLKI/pub?gid=0&single=true&output=csv",
        "order_col": "_Order",
        "partner": "Kerry"
    }
}

COLUMN_ALIASES = {
    "date": ["date", "fleek handover date", "airport handover date", "handover date"],
    "order#": ["order#", "order", "fleek id", "_order", "order no", "order no.", "order num", "order_id"],
    "services": ["services", "service", "partner", "3pl"],
    "weight_kgs": ["weight_kgs", "weight (kg)", "weight", "order net weight", "net weight"],
    "box_count": ["box_count", "boxes", "box count", "no of boxes"],
    "airway_bill": ["airway_bill", "awb", "hawb", "mawb", "apx awb number", "kerry awb number", "ge awb"],
    "courier_service": ["courier_service", "courier", "carrier"],
    "courier_tracking_ids": ["courier_tracking_ids", "tracking id", "tracking_id", "tracking"],
    "consignee": ["consignee", "customer name", "customer_name", "customer", "name"],
    "destination": ["destination", "country", "city"]
}

FIELD_ICONS = {
    "date": "📅", "order#": "🆔", "services": "⚙️", "weight_kgs": "⚖️",
    "box_count": "📦", "airway_bill": "🎫", "courier_service": "🚚",
    "courier_tracking_ids": "📍", "consignee": "👤", "destination": "🎯"
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
    data = {}
    errors = []
    
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
        total = sum(len(d["df"]) for d in st.session_state.all_data.values())
        st.session_state.total_rows = total

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

def get_standard_name(col):
    col_lower = col.lower().strip()
    for std, aliases in COLUMN_ALIASES.items():
        if col_lower in aliases:
            return std
    return None

def filter_tid_data(data):
    filtered = {}
    for col, val in data.items():
        if col == "_search_col":
            continue
        std = get_standard_name(col)
        if std:
            filtered[std] = val
        elif len(filtered) < 15:
            filtered[col] = val
    return filtered

def is_valid(val):
    if val is None:
        return False
    s = str(val).lower().strip()
    return s not in ['', 'nan', 'none', 'n/a', '#n/a', 'na', '-', 'null']

# =============================================================================
# UI COMPONENTS
# =============================================================================

def render_header():
    """Render premium header"""
    col1, col2 = st.columns([2, 1])
    
    with col2:
        st.markdown('<div class="premium-header">TID Search</div>', unsafe_allow_html=True)
        st.markdown('<div class="header-subtitle">Logistics Tracking Intelligence Dashboard</div>', unsafe_allow_html=True)

def render_stats(results, order_count, search_time):
    """Render stats cards"""
    partners = list(set(r["partner"] for r in results))
    sources = list(set(r["source"] for r in results))
    
    st.markdown(f"""
    <div class="stats-container">
        <div class="stat-card">
            <div class="stat-value">{len(results)}</div>
            <div class="stat-label">Results Found</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{order_count}</div>
            <div class="stat-label">Orders Searched</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{len(partners)}</div>
            <div class="stat-label">Partners Matched</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{len(sources)}</div>
            <div class="stat-label">Sources Found</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_result_card(result, valid_only):
    """Render a beautiful result card"""
    partner = result["partner"]
    data = filter_tid_data(result["data"])
    partner_class = f"partner-{partner.lower()}"
    
    fields = [(k, v) for k, v in data.items() if not valid_only or is_valid(v)]
    
    # Build fields HTML
    fields_html = ""
    for name, val in fields[:12]:  # Limit to 12 fields
        icon = FIELD_ICONS.get(name, "📌")
        val_display = str(val)[:40] if is_valid(val) else "—"
        val_class = "" if is_valid(val) else "empty"
        fields_html += f"""
        <div class="field-item">
            <div class="field-label">{icon} {name}</div>
            <div class="field-value {val_class}">{val_display}</div>
        </div>
        """
    
    st.markdown(f"""
    <div class="result-card">
        <div class="result-header">
            <span class="partner-badge {partner_class}">{partner}</span>
            <span class="order-id-display">{result['order_id']}</span>
            <span class="source-tag">📍 {result['source']}</span>
        </div>
        <div class="field-grid">
            {fields_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render sidebar navigation"""
    with st.sidebar:
        st.markdown("### 🚀 Navigation")
        
        # Menu items using radio
        page = st.radio(
            "Select View",
            ["🔍 Global Search", "🟠 ECL QC Center", "🟠 ECL Zone", 
             "🔵 GE QC Center", "🔵 GE Zone", "🟣 APX", "🟢 Kerry"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Data status
        if st.session_state.get("data_loaded"):
            sources_ok = sum(1 for d in st.session_state.all_data.values() if not d["df"].empty)
            st.markdown(f"""
            <div class="status-badge">
                ✅ {st.session_state.total_rows:,} rows loaded
            </div>
            """, unsafe_allow_html=True)
            st.caption(f"{sources_ok}/6 sources active")
        
        st.markdown("---")
        
        # Refresh button
        if st.button("🔄 Reload Data", use_container_width=True):
            if "data_loaded" in st.session_state:
                del st.session_state.data_loaded
            st.rerun()
        
        # Errors
        if st.session_state.get("load_errors"):
            with st.expander("⚠️ Warnings"):
                for err in st.session_state.load_errors:
                    st.warning(err, icon="⚠️")
        
        return page

def search_page():
    """Main search page"""
    render_header()
    
    st.markdown("---")
    
    # Search container
    st.markdown('<div class="search-title">🔍 Search Orders</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([5, 1, 1])
    
    with col1:
        search_input = st.text_input(
            "Enter Order IDs",
            placeholder="Enter order IDs separated by comma, space or newline...",
            label_visibility="collapsed"
        )
    
    with col2:
        search_btn = st.button("🔍 Search", use_container_width=True, type="primary")
    
    with col3:
        valid_only = st.checkbox("Valid only", value=False)
    
    # Process search
    if search_input:
        import re
        order_ids = [x.strip() for x in re.split(r'[\n,\t\s]+', search_input) if x.strip()]
        
        if order_ids:
            start = time.time()
            results = instant_search(order_ids)
            search_time = (time.time() - start) * 1000
            
            # Speed badge
            st.markdown(f"""
            <div class="speed-badge">⚡ Search completed in {search_time:.1f}ms</div>
            """, unsafe_allow_html=True)
            
            if results:
                render_stats(results, len(order_ids), search_time)
                
                st.markdown("---")
                st.markdown(f"### 📋 Results ({len(results)})")
                
                for result in results:
                    render_result_card(result, valid_only)
            else:
                st.markdown("""
                <div class="no-results">
                    <div class="no-results-icon">🔍</div>
                    <h3>No Results Found</h3>
                    <p>Try a different order ID or check the format</p>
                </div>
                """, unsafe_allow_html=True)

def data_page(source_name):
    """Data view page"""
    config = DATA_SOURCES[source_name]
    
    st.markdown(f"## {source_name}")
    st.caption(f"Partner: {config['partner']}")
    
    source_data = st.session_state.all_data.get(source_name, {})
    df = source_data.get("df", pd.DataFrame())
    
    if df.empty:
        st.error("No data available")
        return
    
    # Stats
    col1, col2, col3 = st.columns(3)
    col1.metric("📦 Total Rows", f"{len(df):,}")
    col2.metric("📊 Columns", len(df.columns))
    col3.metric("📁 Partner", config["partner"])
    
    st.markdown("---")
    
    # Filter
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
        f"{source_name}.csv",
        "text/csv"
    )

# =============================================================================
# MAIN
# =============================================================================

def main():
    # Initialize data with loading screen
    if "data_loaded" not in st.session_state:
        st.markdown("""
        <div style="text-align: center; padding: 100px;">
            <div class="premium-header">TID Search</div>
            <div class="status-badge loading">🔄 Loading all data sources...</div>
            <p style="color: #8892b0; margin-top: 20px;">This may take a moment on first load</p>
        </div>
        """, unsafe_allow_html=True)
        
        initialize_data()
        st.rerun()
    
    # Sidebar navigation
    page = render_sidebar()
    
    # Route to correct page
    if page == "🔍 Global Search":
        search_page()
    elif page == "🟠 ECL QC Center":
        data_page("ECL QC Center")
    elif page == "🟠 ECL Zone":
        data_page("ECL Zone")
    elif page == "🔵 GE QC Center":
        data_page("GE QC Center")
    elif page == "🔵 GE Zone":
        data_page("GE Zone")
    elif page == "🟣 APX":
        data_page("APX")
    elif page == "🟢 Kerry":
        data_page("Kerry")

if __name__ == "__main__":
    main()
