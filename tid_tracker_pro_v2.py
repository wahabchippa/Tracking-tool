import streamlit as st
import pandas as pd
import requests
from io import StringIO
from datetime import datetime

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="TID Tracking Tool",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    /* Hide Streamlit defaults */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Main container */
    .main-header {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 100%);
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 25px;
        color: white;
        text-align: center;
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.2rem;
        font-weight: 700;
    }
    
    .main-header p {
        margin: 10px 0 0 0;
        opacity: 0.9;
        font-size: 1rem;
    }
    
    /* Result cards */
    .result-card {
        background: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: all 0.2s ease;
    }
    
    .result-card:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    
    /* Partner badges */
    .badge {
        display: inline-block;
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        color: white;
        margin-bottom: 15px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .badge-ecl { background: linear-gradient(135deg, #f39c12, #e67e22); }
    .badge-ge { background: linear-gradient(135deg, #3498db, #2980b9); }
    .badge-apx { background: linear-gradient(135deg, #9b59b6, #8e44ad); }
    .badge-kerry { background: linear-gradient(135deg, #27ae60, #229954); }
    .badge-ups { background: linear-gradient(135deg, #6c4f3d, #5a3d2b); }
    .badge-royal { background: linear-gradient(135deg, #c0392b, #a93226); }
    
    /* Card header with order ID */
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
        padding-bottom: 12px;
        border-bottom: 2px solid #f0f0f0;
    }
    
    .order-id {
        font-size: 1.3rem;
        font-weight: 700;
        color: #1e3a5f;
    }
    
    /* Field grid */
    .fields-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 12px;
    }
    
    .field-item {
        display: flex;
        align-items: flex-start;
        padding: 10px 12px;
        background: #f8f9fa;
        border-radius: 8px;
        border-left: 3px solid #3498db;
    }
    
    .field-icon {
        font-size: 1.1rem;
        margin-right: 10px;
        min-width: 24px;
    }
    
    .field-content {
        flex: 1;
        min-width: 0;
    }
    
    .field-label {
        font-size: 11px;
        font-weight: 600;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 0.3px;
        margin-bottom: 3px;
    }
    
    .field-value {
        font-size: 14px;
        color: #333;
        word-break: break-word;
        font-weight: 500;
    }
    
    /* Stats boxes */
    .stats-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 15px;
        margin: 20px 0;
    }
    
    .stats-box {
        background: linear-gradient(135deg, #f8f9fa, #ffffff);
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .stats-number {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1e3a5f;
        line-height: 1;
    }
    
    .stats-label {
        font-size: 11px;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 8px;
        font-weight: 600;
    }
    
    /* No results */
    .no-results {
        text-align: center;
        padding: 60px 20px;
        background: #f8f9fa;
        border-radius: 12px;
        margin: 20px 0;
    }
    
    .no-results h3 {
        color: #555;
        margin-bottom: 10px;
    }
    
    .no-results p {
        color: #888;
        margin: 5px 0;
    }
    
    /* Search section */
    .search-section {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    
    /* Loading animation */
    .loading-text {
        text-align: center;
        color: #666;
        font-size: 1.1rem;
    }
    
    /* Status badges in cards */
    .status-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 600;
    }
    
    .status-pending { background: #fff3cd; color: #856404; }
    .status-completed { background: #d4edda; color: #155724; }
    .status-transit { background: #cce5ff; color: #004085; }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .stats-container {
            grid-template-columns: repeat(2, 1fr);
        }
        .fields-grid {
            grid-template-columns: 1fr;
        }
    }
</style>
""", unsafe_allow_html=True)

# ==================== DATA SOURCES CONFIG ====================
DATA_SOURCES = {
    "APX": {
        "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRDEzAMUwnFZ7aoThGoMERtxxsll2kfEaSpa9ksXIx6sqbdMncts6Go2d5mKKabepbNXDSoeaUlk-mP/pub?gid=0&single=true&output=csv",
        "order_col": "Fleek ID",
        "date_col": "Fleek Handover Date",
        "badge_class": "badge-apx",
        "partner_name": "APX"
    },
    "ECL QC Center": {
        "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSCiZ1MdPMyVAzBqmBmp3Ch8sfefOp_kfPk2RSfMv3bxRD_qccuwaoM7WTVsieKJbA3y3DF41tUxb3T/pub?gid=0&single=true&output=csv",
        "order_col": "Fleek ID",
        "date_col": "Fleek Handover Date",
        "badge_class": "badge-ecl",
        "partner_name": "ECL"
    },
    "ECL Zone": {
        "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSCiZ1MdPMyVAzBqmBmp3Ch8sfefOp_kfPk2RSfMv3bxRD_qccuwaoM7WTVsieKJbA3y3DF41tUxb3T/pub?gid=928309568&single=true&output=csv",
        "order_col": 0,
        "date_col": "Fleek Handover Date",
        "badge_class": "badge-ecl",
        "partner_name": "ECL"
    },
    "GE QC Center": {
        "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQjCPd8bUpx59Sit8gMMXjVKhIFA_f-W9Q4mkBSWulOTg4RGahcVXSD4xZiYBAcAH6eO40aEQ9IEEXj/pub?gid=710036753&single=true&output=csv",
        "order_col": "Order Num",
        "date_col": "Fleek Handover Date",
        "badge_class": "badge-ge",
        "partner_name": "GE"
    },
    "GE Zone": {
        "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQjCPd8bUpx59Sit8gMMXjVKhIFA_f-W9Q4mkBSWulOTg4RGahcVXSD4xZiYBAcAH6eO40aEQ9IEEXj/pub?gid=10726393&single=true&output=csv",
        "order_col": 0,
        "date_col": "Airport Handover Date",
        "badge_class": "badge-ge",
        "partner_name": "GE"
    },
    "Kerry": {
        "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vTZyLyZpVJz9sV5eT4Srwo_KZGnYggpRZkm2ILLYPQKSpTKkWfP9G5759h247O4QEflKCzlQauYsLKI/pub?gid=0&single=true&output=csv",
        "order_col": "_Order",
        "date_col": "Fleek Handover Date",
        "badge_class": "badge-kerry",
        "partner_name": "Kerry"
    }
}

# ==================== TID REFERENCE COLUMNS ====================
TID_COLUMNS = [
    # Order identifiers
    "order#", "order no.", "order no", "order num", "fleek id", "_order", "order_id", "order",
    # Dates
    "upload date", "fleek handover date", "airport handover date", "date", "handover date",
    # Service info
    "services", "partner", "service",
    # IDs
    "line_item_batch_id", "fulfillment_id", "batch_id",
    # Invoice
    "invoice_id", "invoice_type", "invoice_amount", "invoice_currency",
    # Physical
    "weight_kgs", "weight (kg)", "weight", "box_count", "boxes", "box count",
    # Tracking
    "airway_bill", "awb", "courier_service", "courier_tracking_ids", "tracking id", "tracking_id",
    # Reference
    "reference", "shipping_account", "shipping account",
    # Customer
    "consignee", "customer name", "customer_name", "customer",
    # Destination
    "destination", "country",
    # Status
    "status", "qc status", "qc_status"
]

# ==================== FIELD ICONS MAPPING ====================
FIELD_ICONS = {
    "order": "🆔",
    "fleek": "🆔",
    "_order": "🆔",
    "tracking": "📍",
    "awb": "✈️",
    "airway": "✈️",
    "courier": "🚚",
    "weight": "⚖️",
    "box": "📦",
    "date": "📅",
    "handover": "📅",
    "upload": "📅",
    "customer": "👤",
    "consignee": "👤",
    "country": "🌍",
    "destination": "🌍",
    "status": "📊",
    "qc": "📊",
    "invoice": "💰",
    "amount": "💰",
    "currency": "💱",
    "service": "🛠️",
    "partner": "🤝",
    "reference": "📋",
    "shipping": "📮",
    "fulfillment": "✅",
    "batch": "📑"
}

# ==================== HELPER FUNCTIONS ====================

def get_field_icon(field_name):
    """Get appropriate icon for a field based on keywords in field name"""
    field_lower = field_name.lower()
    for keyword, icon in FIELD_ICONS.items():
        if keyword in field_lower:
            return icon
    return "📌"

def get_border_color(field_name):
    """Get border color based on field type"""
    field_lower = field_name.lower()
    if any(k in field_lower for k in ["order", "fleek", "_order"]):
        return "#3498db"
    elif any(k in field_lower for k in ["tracking", "awb", "airway", "courier"]):
        return "#9b59b6"
    elif any(k in field_lower for k in ["date", "handover", "upload"]):
        return "#27ae60"
    elif any(k in field_lower for k in ["status", "qc"]):
        return "#e74c3c"
    elif any(k in field_lower for k in ["customer", "consignee"]):
        return "#f39c12"
    elif any(k in field_lower for k in ["country", "destination"]):
        return "#1abc9c"
    elif any(k in field_lower for k in ["invoice", "amount", "currency"]):
        return "#e67e22"
    else:
        return "#95a5a6"

@st.cache_data(ttl=300)
def load_data_from_source(source_name, url, order_col):
    """Load data from a single CSV source with caching"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        df = pd.read_csv(StringIO(response.text))
        
        # Handle column by index if specified
        actual_order_col = order_col
        if isinstance(order_col, int):
            if order_col < len(df.columns):
                actual_order_col = df.columns[order_col]
            else:
                return None
        
        # Create search column
        if actual_order_col in df.columns:
            df["_search_order"] = df[actual_order_col].astype(str).str.strip()
        else:
            # Try to find a matching column
            for col in df.columns:
                if "order" in col.lower() or "fleek" in col.lower():
                    df["_search_order"] = df[col].astype(str).str.strip()
                    break
        
        return df
    except Exception as e:
        return None

def filter_to_tid_columns(df):
    """Filter DataFrame columns to only those in TID reference (case-insensitive)"""
    if df is None or df.empty:
        return df
    
    tid_lower = [col.lower().strip() for col in TID_COLUMNS]
    
    matched_cols = []
    for col in df.columns:
        if col.startswith("_"):
            matched_cols.append(col)
        elif col.lower().strip() in tid_lower:
            matched_cols.append(col)
    
    # If no TID columns matched, return all columns
    non_internal_matched = [c for c in matched_cols if not c.startswith("_")]
    if len(non_internal_matched) == 0:
        return df
    
    return df[matched_cols]

def search_all_sources(search_term):
    """Search for a term across all configured data sources"""
    all_results = []
    search_upper = search_term.strip().upper()
    
    for source_name, config in DATA_SOURCES.items():
        df = load_data_from_source(
            source_name,
            config["url"],
            config["order_col"]
        )
        
        if df is not None and "_search_order" in df.columns:
            # Search in the order column
            mask = df["_search_order"].str.upper().str.contains(search_upper, na=False)
            matches = df[mask].copy()
            
            if not matches.empty:
                # Add metadata columns
                matches["_source"] = source_name
                matches["_badge_class"] = config["badge_class"]
                matches["_partner"] = config["partner_name"]
                
                # Filter to TID columns
                matches = filter_to_tid_columns(matches)
                all_results.append(matches)
    
    if all_results:
        combined = pd.concat(all_results, ignore_index=True)
        return combined
    
    return pd.DataFrame()

def get_order_id_from_row(row):
    """Extract the order ID from a result row"""
    order_columns = ["Fleek ID", "Order Num", "_Order", "Order#", "Order No.", "order_id"]
    for col in order_columns:
        if col in row and pd.notna(row[col]) and str(row[col]).strip():
            return str(row[col]).strip()
    
    # Fallback to _search_order
    if "_search_order" in row:
        return str(row["_search_order"]).strip()
    
    return "N/A"

def render_result_card_html(row, card_index):
    """Generate HTML for a single result card"""
    source = row.get("_source", "Unknown")
    badge_class = row.get("_badge_class", "badge-ecl")
    order_id = get_order_id_from_row(row)
    
    # Build field items HTML
    fields_html = ""
    for col in row.index:
        if col.startswith("_"):
            continue
        
        value = row[col]
        if pd.isna(value) or str(value).strip() == "" or str(value).strip().lower() == "nan":
            continue
        
        icon = get_field_icon(col)
        border_color = get_border_color(col)
        
        fields_html += f'''
        <div class="field-item" style="border-left-color: {border_color};">
            <span class="field-icon">{icon}</span>
            <div class="field-content">
                <div class="field-label">{col}</div>
                <div class="field-value">{value}</div>
            </div>
        </div>
        '''
    
    # Complete card
    card_html = f'''
    <div class="result-card">
        <div class="card-header">
            <span class="order-id">🆔 {order_id}</span>
            <span class="badge {badge_class}">{source}</span>
        </div>
        <div class="fields-grid">
            {fields_html}
        </div>
    </div>
    '''
    
    return card_html

def render_stats_section(results_df):
    """Render the statistics section"""
    total = len(results_df)
    
    # Count by partner
    ecl_count = 0
    ge_count = 0
    apx_count = 0
    kerry_count = 0
    
    if "_source" in results_df.columns:
        for source in results_df["_source"]:
            if "ECL" in source:
                ecl_count += 1
            elif "GE" in source:
                ge_count += 1
            elif "APX" in source:
                apx_count += 1
            elif "Kerry" in source:
                kerry_count += 1
    
    stats_html = f'''
    <div class="stats-container">
        <div class="stats-box">
            <div class="stats-number">{total}</div>
            <div class="stats-label">Total Results</div>
        </div>
        <div class="stats-box">
            <div class="stats-number" style="color: #f39c12;">{ecl_count}</div>
            <div class="stats-label">ECL Records</div>
        </div>
        <div class="stats-box">
            <div class="stats-number" style="color: #3498db;">{ge_count}</div>
            <div class="stats-label">GE Records</div>
        </div>
        <div class="stats-box">
            <div class="stats-number" style="color: #9b59b6;">{apx_count + kerry_count}</div>
            <div class="stats-label">APX + Kerry</div>
        </div>
    </div>
    '''
    
    return stats_html

# ==================== MAIN APPLICATION ====================

def main():
    # Header
    st.markdown('''
    <div class="main-header">
        <h1>📦 TID Tracking Tool</h1>
        <p>Search logistics data across ECL, GE, APX, and Kerry partners</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Search Section
    st.markdown('<div class="search-section">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([4, 1, 1])
    
    with col1:
        search_term = st.text_input(
            "🔍 Search Order ID / Fleek ID / Tracking Number",
            placeholder="Enter FL-123456, Order number, or AWB...",
            key="main_search",
            label_visibility="collapsed"
        )
    
    with col2:
        search_clicked = st.button("🔍 Search", type="primary", use_container_width=True)
    
    with col3:
        clear_clicked = st.button("🗑️ Clear", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Handle clear
    if clear_clicked:
        st.rerun()
    
    # Perform Search
    if search_clicked and search_term:
        with st.spinner("🔄 Searching across all partners..."):
            results_df = search_all_sources(search_term)
        
        if not results_df.empty:
            # Stats Section
            stats_html = render_stats_section(results_df)
            st.markdown(stats_html, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Results Header
            st.subheader(f"📋 Results for: `{search_term}`")
            
            # View Toggle
            col_view1, col_view2 = st.columns([1, 4])
            with col_view1:
                view_mode = st.selectbox(
                    "View Mode",
                    ["Card View", "Table View"],
                    label_visibility="collapsed"
                )
            
            st.markdown("")
            
            if view_mode == "Card View":
                # Render Cards
                for idx, row in results_df.iterrows():
                    card_html = render_result_card_html(row, idx)
                    st.markdown(card_html, unsafe_allow_html=True)
            else:
                # Table View
                display_cols = [c for c in results_df.columns if not c.startswith("_")]
                display_df = results_df[display_cols].copy()
                
                st.dataframe(
                    display_df,
                    use_container_width=True,
                    hide_index=True
                )
            
            # Download Section
            st.markdown("---")
            
            col_dl1, col_dl2, col_dl3 = st.columns([1, 1, 2])
            
            with col_dl1:
                # Prepare CSV
                export_cols = [c for c in results_df.columns if not c.startswith("_")]
                export_df = results_df[export_cols]
                csv_data = export_df.to_csv(index=False)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"TID_Search_{search_term}_{timestamp}.csv"
                
                st.download_button(
                    label="📥 Download CSV",
                    data=csv_data,
                    file_name=filename,
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col_dl2:
                # JSON download
                json_data = export_df.to_json(orient="records", indent=2)
                st.download_button(
                    label="📥 Download JSON",
                    data=json_data,
                    file_name=f"TID_Search_{search_term}_{timestamp}.json",
                    mime="application/json",
                    use_container_width=True
                )
        
        else:
            # No Results
            st.markdown('''
            <div class="no-results">
                <h3>😔 No Results Found</h3>
                <p>We couldn't find any records matching "<strong>''' + search_term + '''</strong>"</p>
                <p>Try a different Order ID, Fleek ID, or Tracking Number</p>
            </div>
            ''', unsafe_allow_html=True)
    
    elif search_clicked and not search_term:
        st.warning("⚠️ Please enter a search term to continue")
    
    # Footer / Help Section
    st.markdown("---")
    
    with st.expander("ℹ️ Help & Information", expanded=False):
        col_h1, col_h2 = st.columns(2)
        
        with col_h1:
            st.markdown("""
            **🔍 Search Tips:**
            - Enter full or partial Order ID
            - Search by Fleek ID (e.g., FL-123456)
            - Search by AWB/Tracking number
            - Search is case-insensitive
            """)
        
        with col_h2:
            st.markdown("""
            **📊 Connected Partners:**
            - 🟠 **ECL** - QC Center & Zone
            - 🔵 **GE** - QC Center & Zone
            - 🟣 **APX** - Shipments
            - 🟢 **Kerry** - Logistics
            """)
        
        st.markdown("""
        ---
        **📋 Displayed Fields:**
        Order IDs, Dates, Weight, Box Count, AWB, Tracking IDs, Customer Name, Destination, Invoice Details, Status
        
        **⏱️ Data Refresh:**
        Data is cached for 5 minutes for performance. New data will be fetched automatically.
        """)
    
    # Footer
    st.markdown(
        f"""
        <div style="text-align: center; color: #888; padding: 20px; font-size: 12px;">
            TID Tracking Tool v1.0 | Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M")}
        </div>
        """,
        unsafe_allow_html=True
    )

# ==================== RUN APPLICATION ====================
if __name__ == "__main__":
    main()
