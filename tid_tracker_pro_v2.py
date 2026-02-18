import streamlit as st
import pandas as pd
import re
from datetime import datetime

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="TID Tracker Pro",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== EXACT TID COLUMNS (FROM YOUR SCREENSHOT) ====================
TID_REQUIRED_COLUMNS = [
    # Exact columns from your screenshot
    "date",
    "order#",
    "upload date",
    "services",
    "order_id",
    "line_item_batch_id",
    "fulfillment_id",
    "invoice_id",
    "invoice_type",
    "weight_kgs",
    "box_count",
    "airway_bill",
    "courier_service",
    "courier_tracking_ids",
    "reference",
    "shipping_account",
    "consignee",
    "destination",
    
    # Alternative names (for different sheets)
    "fleek id", "_order", "order no", "order no.", "order num", "order",
    "fleek handover date", "airport handover date", "handover date",
    "service", "partner",
    "batch_id",
    "weight (kg)", "weight", "order net weight",
    "boxes", "box count",
    "awb", "hawb", "mawb", "apx awb number", "kerry awb number", "ge awb",
    "courier", "3pl", "carrier",
    "tracking id", "tracking_id", "trackingid", "tracking",
    "ref",
    "shipping account",
    "customer name", "customer_name", "customer", "name",
    "country", "city"
]

# ==================== FIELD ICONS (MATCHING YOUR COLUMNS) ====================
FIELD_ICONS = {
    # Date
    "date": "📅",
    "fleek handover date": "📅",
    "airport handover date": "🛫",
    "handover date": "📅",
    "upload date": "📤",
    
    # Order
    "order#": "🆔",
    "order_id": "🔢",
    "fleek id": "🆔",
    "_order": "🆔",
    "order no": "🆔",
    "order no.": "🆔",
    "order num": "🆔",
    "order": "🆔",
    
    # Services
    "services": "⚙️",
    "service": "⚙️",
    "partner": "🤝",
    
    # IDs
    "line_item_batch_id": "📑",
    "batch_id": "📑",
    "fulfillment_id": "✅",
    "invoice_id": "🧾",
    "invoice_type": "📄",
    
    # Weight & Box
    "weight_kgs": "⚖️",
    "weight (kg)": "⚖️",
    "weight": "⚖️",
    "order net weight": "⚖️",
    "box_count": "📦",
    "boxes": "📦",
    "box count": "📦",
    
    # AWB & Tracking
    "airway_bill": "🎫",
    "awb": "🎫",
    "hawb": "🎫",
    "mawb": "✈️",
    "apx awb number": "🎫",
    "kerry awb number": "🎫",
    "ge awb": "🎫",
    "courier_service": "🚚",
    "courier": "🚚",
    "3pl": "🚛",
    "carrier": "🚛",
    "courier_tracking_ids": "📍",
    "tracking id": "📍",
    "tracking_id": "📍",
    "trackingid": "📍",
    "tracking": "📍",
    
    # Reference & Shipping
    "reference": "🔗",
    "ref": "🔗",
    "shipping_account": "📮",
    "shipping account": "📮",
    
    # Customer & Destination
    "consignee": "👤",
    "customer name": "👤",
    "customer_name": "👤",
    "customer": "👤",
    "name": "👤",
    "destination": "🎯",
    "country": "🌍",
    "city": "🏙️",
}

def get_icon(field_name):
    """Get appropriate icon for a field name"""
    field_lower = field_name.lower().strip()
    
    # Direct match
    if field_lower in FIELD_ICONS:
        return FIELD_ICONS[field_lower]
    
    # Partial match
    for key, icon in FIELD_ICONS.items():
        if key in field_lower or field_lower in key:
            return icon
    
    return "📋"

def is_tid_column(col_name):
    """Check if column is in TID required columns (case-insensitive)"""
    col_lower = col_name.lower().strip()
    tid_lower = [c.lower().strip() for c in TID_REQUIRED_COLUMNS]
    
    # Direct match
    if col_lower in tid_lower:
        return True
    
    # Partial match for flexibility
    for tid_col in tid_lower:
        if tid_col in col_lower or col_lower in tid_col:
            return True
    
    return False

def filter_tid_columns(data_dict):
    """Filter dictionary to only include TID columns"""
    filtered = {}
    for key, val in data_dict.items():
        if is_tid_column(key):
            filtered[key] = val
    return filtered

# ==================== PREMIUM CSS STYLING ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    :root {
        --bg-primary: #0a0a0f;
        --bg-secondary: #12121a;
        --bg-card: rgba(255, 255, 255, 0.03);
        --border-color: rgba(255, 255, 255, 0.08);
        --text-primary: #ffffff;
        --text-secondary: #a0a0b0;
        --accent-orange: #f59e0b;
        --accent-blue: #3b82f6;
        --accent-purple: #8b5cf6;
        --accent-green: #10b981;
        --accent-pink: #ec4899;
        --accent-cyan: #06b6d4;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #0a0a0f 100%);
        font-family: 'Inter', sans-serif;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding: 2rem 3rem !important; max-width: 100% !important;}
    
    .bg-orbs {
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        pointer-events: none;
        z-index: -1;
        overflow: hidden;
    }
    
    .orb {
        position: absolute;
        border-radius: 50%;
        filter: blur(80px);
        opacity: 0.3;
        animation: float 20s ease-in-out infinite;
    }
    
    .orb-1 {
        width: 400px; height: 400px;
        background: linear-gradient(135deg, #f59e0b, #ec4899);
        top: -100px; left: -100px;
    }
    
    .orb-2 {
        width: 300px; height: 300px;
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        top: 50%; right: -50px;
        animation-delay: -5s;
    }
    
    .orb-3 {
        width: 350px; height: 350px;
        background: linear-gradient(135deg, #10b981, #06b6d4);
        bottom: -100px; left: 30%;
        animation-delay: -10s;
    }
    
    @keyframes float {
        0%, 100% { transform: translate(0, 0) rotate(0deg); }
        25% { transform: translate(50px, 50px) rotate(5deg); }
        50% { transform: translate(0, 100px) rotate(0deg); }
        75% { transform: translate(-50px, 50px) rotate(-5deg); }
    }
    
    .premium-header {
        text-align: center;
        padding: 2rem 0 3rem;
    }
    
    .logo-container {
        display: inline-flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    .logo-icon {
        font-size: 3rem;
        background: linear-gradient(135deg, #f59e0b, #ec4899, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { filter: drop-shadow(0 0 20px rgba(245, 158, 11, 0.5)); }
        to { filter: drop-shadow(0 0 30px rgba(139, 92, 246, 0.5)); }
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #a0a0b0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
        margin: 0;
    }
    
    .subtitle {
        font-size: 1.1rem;
        color: var(--text-secondary);
        margin-top: 0.5rem;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .stat-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .stat-icon { font-size: 1.8rem; margin-bottom: 0.5rem; }
    .stat-value { font-size: 1.5rem; font-weight: 700; color: var(--text-primary); }
    .stat-label { font-size: 0.75rem; color: var(--text-secondary); text-transform: uppercase; margin-top: 0.3rem; }
    
    .result-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .result-card:hover {
        border-color: rgba(255,255,255,0.15);
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
    }
    
    .result-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        padding-bottom: 0.8rem;
        border-bottom: 1px solid rgba(255,255,255,0.08);
    }
    
    .order-id { font-size: 1.2rem; font-weight: 700; color: var(--text-primary); }
    
    .lp-badge {
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .badge-ecl { background: linear-gradient(135deg, #f59e0b, #d97706); color: #000; }
    .badge-ge { background: linear-gradient(135deg, #3b82f6, #2563eb); color: #fff; }
    .badge-apx { background: linear-gradient(135deg, #8b5cf6, #7c3aed); color: #fff; }
    .badge-kerry { background: linear-gradient(135deg, #10b981, #059669); color: #fff; }
    
    .result-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 1rem;
    }
    
    .field-item {
        display: flex;
        align-items: flex-start;
        gap: 0.6rem;
        padding: 0.5rem;
        border-radius: 8px;
        background: rgba(255,255,255,0.02);
    }
    
    .field-icon { font-size: 1.1rem; min-width: 24px; text-align: center; }
    .field-content { flex: 1; min-width: 0; }
    .field-label { font-size: 0.7rem; color: var(--text-secondary); text-transform: uppercase; margin-bottom: 0.2rem; }
    .field-value { font-size: 0.9rem; color: var(--text-primary); font-weight: 500; word-break: break-word; }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 10px;
        color: var(--text-secondary);
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255,255,255,0.08);
        color: var(--text-primary);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(245,158,11,0.2), rgba(139,92,246,0.2)) !important;
        border-color: rgba(245,158,11,0.3) !important;
        color: var(--text-primary) !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #f59e0b, #ec4899) !important;
        color: #000 !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 30px rgba(245, 158, 11, 0.3) !important;
    }
    
    .stTextArea textarea, .stTextInput input {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
    }
    
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: rgba(245, 158, 11, 0.5) !important;
        box-shadow: 0 0 20px rgba(245, 158, 11, 0.1) !important;
    }
    
    .stDateInput > div > div > input {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: var(--text-primary) !important;
    }
    
    .no-results {
        text-align: center;
        padding: 3rem;
        color: var(--text-secondary);
    }
    
    .no-results-icon { font-size: 4rem; margin-bottom: 1rem; opacity: 0.5; }
    
    .premium-footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        border-top: 1px solid rgba(255,255,255,0.05);
        color: var(--text-secondary);
    }
    
    .column-badge {
        background: rgba(245, 158, 11, 0.15);
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-radius: 8px;
        padding: 8px 12px;
        margin: 10px 0;
        color: #f59e0b;
        font-size: 0.8rem;
    }
</style>

<div class="bg-orbs">
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>
</div>
""", unsafe_allow_html=True)

# ==================== DATA SOURCES ====================
DATA_SOURCES = {
    "APX": {
        "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRDEzAMUwnFZ7aoThGoMERtxxsll2kfEaSpa9ksXIx6sqbdMncts6Go2d5mKKabepbNXDSoeaUlk-mP/pub?gid=0&single=true&output=csv",
        "order_col": "Fleek ID",
        "date_col": "Fleek Handover Date",
        "partner": "APX",
        "badge_class": "badge-apx"
    },
    "ECL QC Center": {
        "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSCiZ1MdPMyVAzBqmBmp3Ch8sfefOp_kfPk2RSfMv3bxRD_qccuwaoM7WTVsieKJbA3y3DF41tUxb3T/pub?gid=0&single=true&output=csv",
        "order_col": "Fleek ID",
        "date_col": "Fleek Handover Date",
        "partner": "ECL",
        "badge_class": "badge-ecl"
    },
    "ECL Zone": {
        "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSCiZ1MdPMyVAzBqmBmp3Ch8sfefOp_kfPk2RSfMv3bxRD_qccuwaoM7WTVsieKJbA3y3DF41tUxb3T/pub?gid=928309568&single=true&output=csv",
        "order_col": 0,
        "date_col": "Fleek Handover Date",
        "partner": "ECL",
        "badge_class": "badge-ecl"
    },
    "GE QC Center": {
        "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQjCPd8bUpx59Sit8gMMXjVKhIFA_f-W9Q4mkBSWulOTg4RGahcVXSD4xZiYBAcAH6eO40aEQ9IEEXj/pub?gid=710036753&single=true&output=csv",
        "order_col": "Order Num",
        "date_col": "Fleek Handover Date",
        "partner": "GE",
        "badge_class": "badge-ge"
    },
    "GE Zone": {
        "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQjCPd8bUpx59Sit8gMMXjVKhIFA_f-W9Q4mkBSWulOTg4RGahcVXSD4xZiYBAcAH6eO40aEQ9IEEXj/pub?gid=10726393&single=true&output=csv",
        "order_col": 0,
        "date_col": "Airport Handover Date",
        "partner": "GE",
        "badge_class": "badge-ge"
    },
    "Kerry": {
        "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vTZyLyZpVJz9sV5eT4Srwo_KZGnYggpRZkm2ILLYPQKSpTKkWfP9G5759h247O4QEflKCzlQauYsLKI/pub?gid=0&single=true&output=csv",
        "order_col": "_Order",
        "date_col": "Fleek Handover Date",
        "partner": "Kerry",
        "badge_class": "badge-kerry"
    }
}

# ==================== DATA FUNCTIONS ====================
@st.cache_data(ttl=300)
def load_sheet_data(source_name):
    """Load data from published CSV"""
    try:
        config = DATA_SOURCES[source_name]
        df = pd.read_csv(config["url"])
        return df
    except Exception as e:
        st.error(f"Error loading {source_name}: {e}")
        return pd.DataFrame()

def get_order_column(df, order_col_config):
    """Get order column name"""
    if isinstance(order_col_config, int):
        return df.columns[order_col_config] if len(df.columns) > order_col_config else None
    return order_col_config if order_col_config in df.columns else None

def parse_date(date_str):
    """Parse date string"""
    if pd.isna(date_str) or str(date_str).strip() == '':
        return None
    date_str = str(date_str).strip()
    for fmt in ['%d/%m/%Y', '%d/%m/%y', '%Y-%m-%d', '%d-%m-%Y', '%d-%m-%y', '%d-%b-%Y']:
        try:
            return datetime.strptime(date_str, fmt).date()
        except:
            continue
    return None

def parse_orders(input_text):
    """Parse multiple orders"""
    orders = re.split(r'[\n,\t\s]+', input_text.strip())
    return [o.strip() for o in orders if o.strip()]

def search_all_sources(orders):
    """Search across all sources"""
    results = []
    
    for source_name, config in DATA_SOURCES.items():
        df = load_sheet_data(source_name)
        if df.empty:
            continue
        
        order_col = get_order_column(df, config["order_col"])
        if not order_col:
            continue
        
        df[order_col] = df[order_col].astype(str)
        
        for order in orders:
            matches = df[df[order_col].str.contains(order, case=False, na=False)]
            for _, row in matches.iterrows():
                filtered_data = filter_tid_columns(row.to_dict())
                results.append({
                    "source": source_name,
                    "partner": config["partner"],
                    "badge_class": config["badge_class"],
                    "order": row[order_col],
                    "data": filtered_data
                })
    
    return results

def is_valid_value(val):
    """Check if value is valid"""
    if pd.isna(val):
        return False
    val_str = str(val).strip().lower()
    return val_str not in ['#n/a', 'n/a', 'na', 'not applicable', 'none', '', '-', 'nan']

def format_value(val):
    """Format value for display"""
    if not is_valid_value(val):
        return "-"
    return str(val).strip()

def filter_tid_columns_df(df):
    """Filter DataFrame to TID columns only"""
    tid_cols = [col for col in df.columns if is_tid_column(col)]
    if tid_cols:
        return df[tid_cols]
    return df

# ==================== HEADER ====================
st.markdown("""
<div class="premium-header">
    <div class="logo-container">
        <span class="logo-icon">🔍</span>
    </div>
    <h1 class="main-title">TID Tracker Pro</h1>
    <p class="subtitle">Premium Logistics Tracking Intelligence • ECL • GE • APX • Kerry</p>
</div>
""", unsafe_allow_html=True)

# ==================== MAIN TABS ====================
tab_search, tab_ecl_qc, tab_ecl_zone, tab_ge_qc, tab_ge_zone, tab_apx, tab_kerry = st.tabs([
    "🔍 Global Search",
    "🟠 ECL QC",
    "🟠 ECL Zone",
    "🔵 GE QC",
    "🔵 GE Zone",
    "🟣 APX",
    "🟢 Kerry"
])

# ==================== GLOBAL SEARCH TAB ====================
with tab_search:
    col_left, col_center, col_right = st.columns([1, 2, 1])
    
    with col_center:
        search_input = st.text_area(
            "Search",
            placeholder="🔍 Search Orders Across All Partners\n\nEnter one or multiple orders (separated by newlines, commas, or spaces)\n\nExample: 70915_74, 65658_54, 128030_50",
            height=120,
            label_visibility="collapsed"
        )
        
        col_btn1, col_btn2 = st.columns([3, 1])
        with col_btn1:
            search_btn = st.button("🔍 Search", use_container_width=True, type="primary")
        with col_btn2:
            show_valid_only = st.checkbox("Valid only", value=True, help="Hide empty/N/A values")
        
        # Show columns info
        st.markdown("""
        <div class="column-badge">
            📋 <b>Displaying:</b> Date • Order# • Upload Date • Services • order_id • line_item_batch_id • fulfillment_id • invoice_id • invoice_type • weight_kgs • box_count • airway_bill • courier_service • courier_tracking_ids • reference • shipping_account • consignee • destination
        </div>
        """, unsafe_allow_html=True)
    
    if search_btn and search_input:
        orders = parse_orders(search_input)
        
        if orders:
            with st.spinner("🔍 Searching across all logistics partners..."):
                results = search_all_sources(orders)
            
            if results:
                # Stats
                st.markdown(f"""
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-icon">📋</div>
                        <div class="stat-value">{len(orders)}</div>
                        <div class="stat-label">Searched</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon">✅</div>
                        <div class="stat-value">{len(results)}</div>
                        <div class="stat-label">Found</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon">🏢</div>
                        <div class="stat-value">{len(set(r['partner'] for r in results))}</div>
                        <div class="stat-label">Partners</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon">📦</div>
                        <div class="stat-value">{len(set(r['source'] for r in results))}</div>
                        <div class="stat-label">Sources</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Result cards
                for result in results:
                    order_id = result['order']
                    partner = result['partner']
                    badge_class = result['badge_class']
                    data = result['data']
                    source = result['source']
                    
                    fields_html = ""
                    for key, val in data.items():
                        if show_valid_only and not is_valid_value(val):
                            continue
                        icon = get_icon(key)
                        formatted_val = format_value(val)
                        fields_html += f"""
                        <div class="field-item">
                            <span class="field-icon">{icon}</span>
                            <div class="field-content">
                                <div class="field-label">{key}</div>
                                <div class="field-value">{formatted_val}</div>
                            </div>
                        </div>
                        """
                    
                    st.markdown(f"""
                    <div class="result-card">
                        <div class="result-header">
                            <span class="order-id">🆔 {order_id}</span>
                            <div>
                                <span class="lp-badge {badge_class}">{partner}</span>
                                <span style="color: var(--text-secondary); font-size: 0.8rem; margin-left: 0.5rem;">{source}</span>
                            </div>
                        </div>
                        <div class="result-grid">
                            {fields_html}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Download
                st.markdown("---")
                results_df = pd.DataFrame([{**{"Source": r["source"], "Partner": r["partner"]}, **r["data"]} for r in results])
                csv = results_df.to_csv(index=False)
                st.download_button("📥 Download Search Results (CSV)", csv, "search_results.csv", "text/csv", use_container_width=True)
            else:
                st.markdown("""
                <div class="no-results">
                    <div class="no-results-icon">🔍</div>
                    <h3>No Results Found</h3>
                    <p>Try different order numbers or check the spelling</p>
                </div>
                """, unsafe_allow_html=True)

# ==================== DATA TAB HELPER ====================
def render_data_tab(source_name):
    """Render data tab with TID columns"""
    
    config = DATA_SOURCES[source_name]
    df = load_sheet_data(source_name)
    
    if df.empty:
        st.warning(f"Unable to load data for {source_name}")
        return
    
    order_col = get_order_column(df, config["order_col"])
    date_col = config.get("date_col")
    
    if date_col and date_col in df.columns:
        df['_parsed_date'] = df[date_col].apply(parse_date)
    
    # Filter to TID columns
    display_df = filter_tid_columns_df(df)
    
    # Stats
    total_orders = len(df)
    boxes_col = next((c for c in display_df.columns if 'box' in c.lower()), None)
    weight_col = next((c for c in display_df.columns if 'weight' in c.lower()), None)
    country_col = next((c for c in display_df.columns if 'country' in c.lower() or 'destination' in c.lower()), None)
    tracking_col = next((c for c in display_df.columns if 'tracking' in c.lower()), None)
    
    total_boxes = df[boxes_col].sum() if boxes_col and boxes_col in df.columns and pd.api.types.is_numeric_dtype(df[boxes_col]) else 0
    total_weight = df[weight_col].sum() if weight_col and weight_col in df.columns and pd.api.types.is_numeric_dtype(df[weight_col]) else 0
    unique_countries = df[country_col].nunique() if country_col and country_col in df.columns else 0
    with_tracking = df[tracking_col].apply(is_valid_value).sum() if tracking_col and tracking_col in df.columns else 0
    
    st.markdown(f"""
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-icon">📋</div>
            <div class="stat-value">{total_orders:,}</div>
            <div class="stat-label">Total Orders</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon">📦</div>
            <div class="stat-value">{int(total_boxes):,}</div>
            <div class="stat-label">Total Boxes</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon">⚖️</div>
            <div class="stat-value">{total_weight:,.1f}</div>
            <div class="stat-label">Weight (kg)</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon">🌍</div>
            <div class="stat-value">{unique_countries}</div>
            <div class="stat-label">Countries</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon">📍</div>
            <div class="stat-value">{with_tracking:,}</div>
            <div class="stat-label">With Tracking</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Filters
    col1, col2, col3, col4, col5 = st.columns([2, 1.5, 1.5, 1, 1])
    
    with col1:
        search_filter = st.text_input("🔍 Quick Search", placeholder="Search any field...", key=f"search_{source_name}")
    with col2:
        date_from = st.date_input("📅 From Date", value=None, key=f"date_from_{source_name}")
    with col3:
        date_to = st.date_input("📅 To Date", value=None, key=f"date_to_{source_name}")
    with col4:
        valid_only = st.checkbox("Valid Only", value=False, key=f"valid_{source_name}")
    with col5:
        if st.button("🔄 Refresh", key=f"refresh_{source_name}"):
            st.cache_data.clear()
            st.rerun()
    
    # Apply filters
    filtered_df = display_df.copy()
    
    if search_filter:
        mask = filtered_df.astype(str).apply(lambda x: x.str.contains(search_filter, case=False, na=False)).any(axis=1)
        filtered_df = filtered_df[mask]
    
    if date_from and '_parsed_date' in df.columns:
        valid_indices = df[df['_parsed_date'] >= date_from].index
        filtered_df = filtered_df.loc[filtered_df.index.intersection(valid_indices)]
    
    if date_to and '_parsed_date' in df.columns:
        valid_indices = df[df['_parsed_date'] <= date_to].index
        filtered_df = filtered_df.loc[filtered_df.index.intersection(valid_indices)]
    
    if valid_only and tracking_col and tracking_col in df.columns:
        valid_indices = df[df[tracking_col].apply(is_valid_value)].index
        filtered_df = filtered_df.loc[filtered_df.index.intersection(valid_indices)]
    
    # Display
    st.markdown(f"**Showing {len(filtered_df):,} of {len(df):,} records** | **{len(display_df.columns)} TID Columns**")
    st.dataframe(filtered_df, use_container_width=True, height=500)
    
    # Downloads
    col1, col2 = st.columns(2)
    with col1:
        csv = filtered_df.to_csv(index=False)
        st.download_button("📥 Download Filtered (CSV)", csv, f"{source_name.lower().replace(' ', '_')}_filtered.csv", "text/csv", use_container_width=True)
    with col2:
        csv_all = display_df.to_csv(index=False)
        st.download_button("📥 Download All (CSV)", csv_all, f"{source_name.lower().replace(' ', '_')}_all.csv", "text/csv", use_container_width=True)

# ==================== DATA TABS ====================
with tab_ecl_qc:
    st.markdown("### 🟠 ECL QC Center")
    render_data_tab("ECL QC Center")

with tab_ecl_zone:
    st.markdown("### 🟠 ECL Zone")
    render_data_tab("ECL Zone")

with tab_ge_qc:
    st.markdown("### 🔵 GE QC Center")
    render_data_tab("GE QC Center")

with tab_ge_zone:
    st.markdown("### 🔵 GE Zone")
    render_data_tab("GE Zone")

with tab_apx:
    st.markdown("### 🟣 APX Logistics")
    render_data_tab("APX")

with tab_kerry:
    st.markdown("### 🟢 Kerry Logistics")
    render_data_tab("Kerry")

# ==================== FOOTER ====================
st.markdown("""
<div class="premium-footer">
    <p>🚀 TID Tracker Pro • Premium Logistics Intelligence</p>
    <p>ECL • GE • APX • Kerry</p>
</div>
""", unsafe_allow_html=True)
