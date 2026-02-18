import streamlit as st
import pandas as pd
import requests
from io import StringIO
from datetime import datetime

# Page config
st.set_page_config(
    page_title="TID Search Tool",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1e3a8a;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #64748b;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stExpander {
        border-radius: 10px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# DATA SOURCES CONFIGURATION
# =============================================================================

DATA_SOURCES = {
    "ECL QC Center": {
        "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSCiZ1MdPMyVAzBqmBmp3Ch8sfefOp_kfPk2RSfMv3bxRD_qccuwaoM7WTVsieKJbA3y3DF41tUxb3T/pub?gid=0&single=true&output=csv",
        "order_col": "Fleek ID",
        "date_col": "Fleek Handover Date",
        "partner": "ECL",
        "color": "#f59e0b"
    },
    "ECL Zone": {
        "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSCiZ1MdPMyVAzBqmBmp3Ch8sfefOp_kfPk2RSfMv3bxRD_qccuwaoM7WTVsieKJbA3y3DF41tUxb3T/pub?gid=928309568&single=true&output=csv",
        "order_col": 0,
        "date_col": "Fleek Handover Date",
        "partner": "ECL",
        "color": "#f59e0b"
    },
    "GE QC Center": {
        "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQjCPd8bUpx59Sit8gMMXjVKhIFA_f-W9Q4mkBSWulOTg4RGahcVXSD4xZiYBAcAH6eO40aEQ9IEEXj/pub?gid=710036753&single=true&output=csv",
        "order_col": "Order Num",
        "date_col": "Fleek Handover Date",
        "partner": "GE",
        "color": "#3b82f6"
    },
    "GE Zone": {
        "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQjCPd8bUpx59Sit8gMMXjVKhIFA_f-W9Q4mkBSWulOTg4RGahcVXSD4xZiYBAcAH6eO40aEQ9IEEXj/pub?gid=10726393&single=true&output=csv",
        "order_col": 0,
        "date_col": "Airport Handover Date",
        "partner": "GE",
        "color": "#3b82f6"
    },
    "APX": {
        "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vRDEzAMUwnFZ7aoThGoMERtxxsll2kfEaSpa9ksXIx6sqbdMncts6Go2d5mKKabepbNXDSoeaUlk-mP/pub?gid=0&single=true&output=csv",
        "order_col": "Fleek ID",
        "date_col": "Fleek Handover Date",
        "partner": "APX",
        "color": "#8b5cf6"
    },
    "Kerry": {
        "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vTZyLyZpVJz9sV5eT4Srwo_KZGnYggpRZkm2ILLYPQKSpTKkWfP9G5759h247O4QEflKCzlQauYsLKI/pub?gid=0&single=true&output=csv",
        "order_col": "_Order",
        "date_col": "Fleek Handover Date",
        "partner": "Kerry",
        "color": "#10b981"
    }
}

# =============================================================================
# TID REQUIRED COLUMNS
# =============================================================================

TID_REQUIRED_COLUMNS = [
    "date", "order#", "upload date", "services", "order_id", "line_item_batch_id",
    "fulfillment_id", "invoice_id", "invoice_type", "weight_kgs", "box_count",
    "airway_bill", "courier_service", "courier_tracking_ids", "reference",
    "shipping_account", "consignee", "destination"
]

# Alternative column names mapping
COLUMN_ALIASES = {
    "date": ["date", "fleek handover date", "airport handover date", "handover date", "handover_date"],
    "order#": ["order#", "order", "fleek id", "_order", "order no", "order no.", "order num", "order_id", "orderid"],
    "upload date": ["upload date", "upload_date", "uploaded date"],
    "services": ["services", "service", "partner", "3pl"],
    "order_id": ["order_id", "orderid", "order id"],
    "line_item_batch_id": ["line_item_batch_id", "line item batch id", "batch id", "batch_id"],
    "fulfillment_id": ["fulfillment_id", "fulfillment id", "fulfillment"],
    "invoice_id": ["invoice_id", "invoice id", "invoice"],
    "invoice_type": ["invoice_type", "invoice type"],
    "weight_kgs": ["weight_kgs", "weight (kg)", "weight", "order net weight", "net weight", "weight kg"],
    "box_count": ["box_count", "boxes", "box count", "no of boxes", "number of boxes"],
    "airway_bill": ["airway_bill", "awb", "hawb", "mawb", "apx awb number", "kerry awb number", "ge awb", "airway bill"],
    "courier_service": ["courier_service", "courier", "carrier", "shipping method"],
    "courier_tracking_ids": ["courier_tracking_ids", "tracking id", "tracking_id", "trackingid", "tracking", "tracking number"],
    "reference": ["reference", "ref", "reference number"],
    "shipping_account": ["shipping_account", "shipping account"],
    "consignee": ["consignee", "customer name", "customer_name", "customer", "name", "recipient"],
    "destination": ["destination", "country", "city", "dest", "destination country"]
}

# Field icons
FIELD_ICONS = {
    "date": "📅", "order#": "🆔", "upload date": "📤", "services": "⚙️", 
    "order_id": "🔢", "line_item_batch_id": "📑", "fulfillment_id": "✅", 
    "invoice_id": "🧾", "invoice_type": "📋", "weight_kgs": "⚖️", 
    "box_count": "📦", "airway_bill": "🎫", "courier_service": "🚚", 
    "courier_tracking_ids": "📍", "reference": "🔗", "shipping_account": "📮", 
    "consignee": "👤", "destination": "🎯"
}

# Partner colors
PARTNER_COLORS = {
    "ECL": "🟠",
    "GE": "🔵",
    "APX": "🟣",
    "Kerry": "🟢"
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_standard_column_name(col_name):
    """Map any column name to its standard TID column name"""
    col_lower = col_name.lower().strip()
    for standard_name, aliases in COLUMN_ALIASES.items():
        if col_lower in [a.lower() for a in aliases]:
            return standard_name
    return None

def is_tid_column(col_name):
    """Check if column is a TID required column"""
    return get_standard_column_name(col_name) is not None

def is_valid_value(value):
    """Check if value is valid (not empty/NA)"""
    if value is None:
        return False
    str_val = str(value).lower().strip()
    invalid_values = ['#n/a', 'n/a', 'na', 'not applicable', 'none', '', '-', 'nan', 'null', 'undefined']
    return str_val not in invalid_values

@st.cache_data(ttl=300)
def load_data(source_name):
    """Load data from a source with caching"""
    try:
        config = DATA_SOURCES[source_name]
        response = requests.get(config["url"], timeout=30)
        response.raise_for_status()
        df = pd.read_csv(StringIO(response.text))
        
        # Handle index-based column reference
        order_col = config["order_col"]
        if isinstance(order_col, int):
            actual_col_name = df.columns[order_col]
            config["order_col_actual"] = actual_col_name
        else:
            config["order_col_actual"] = order_col
            
        return df
    except Exception as e:
        st.error(f"Error loading {source_name}: {str(e)}")
        return pd.DataFrame()

def filter_tid_columns(data_dict):
    """Filter dictionary to only TID columns with standardized names"""
    filtered = {}
    for col, value in data_dict.items():
        standard_name = get_standard_column_name(col)
        if standard_name:
            filtered[standard_name] = value
    return filtered if filtered else data_dict

def filter_tid_columns_df(df):
    """Filter DataFrame to only TID columns"""
    tid_cols = [col for col in df.columns if is_tid_column(col)]
    if tid_cols:
        return df[tid_cols]
    return df

def search_order(order_id, source_name):
    """Search for an order in a specific source"""
    df = load_data(source_name)
    if df.empty:
        return []
    
    config = DATA_SOURCES[source_name]
    order_col = config.get("order_col_actual", config["order_col"])
    
    if isinstance(order_col, int):
        order_col = df.columns[order_col]
    
    if order_col not in df.columns:
        return []
    
    # Search with string matching
    df[order_col] = df[order_col].astype(str)
    matches = df[df[order_col].str.lower().str.strip() == str(order_id).lower().strip()]
    
    results = []
    for _, row in matches.iterrows():
        data_dict = row.to_dict()
        filtered_data = filter_tid_columns(data_dict)
        results.append({
            "source": source_name,
            "partner": config["partner"],
            "color": config["color"],
            "order_id": order_id,
            "data": filtered_data
        })
    
    return results

def search_all_sources(order_ids):
    """Search for multiple orders across all sources"""
    all_results = []
    
    for order_id in order_ids:
        order_id = order_id.strip()
        if not order_id:
            continue
            
        for source_name in DATA_SOURCES.keys():
            results = search_order(order_id, source_name)
            all_results.extend(results)
    
    return all_results

def parse_order_ids(input_text):
    """Parse order IDs from input text"""
    # Split by newlines, commas, tabs, spaces
    import re
    order_ids = re.split(r'[\n,\t\s]+', input_text)
    # Clean and filter empty
    order_ids = [oid.strip() for oid in order_ids if oid.strip()]
    return order_ids

def calculate_stats(df, source_name):
    """Calculate statistics for a dataframe"""
    config = DATA_SOURCES[source_name]
    stats = {
        "total_orders": len(df),
        "total_boxes": 0,
        "total_weight": 0,
        "unique_countries": 0,
        "with_tracking": 0
    }
    
    # Find box column
    for col in df.columns:
        if get_standard_column_name(col) == "box_count":
            try:
                stats["total_boxes"] = pd.to_numeric(df[col], errors='coerce').sum()
            except:
                pass
            break
    
    # Find weight column
    for col in df.columns:
        if get_standard_column_name(col) == "weight_kgs":
            try:
                stats["total_weight"] = pd.to_numeric(df[col], errors='coerce').sum()
            except:
                pass
            break
    
    # Find destination column
    for col in df.columns:
        if get_standard_column_name(col) == "destination":
            try:
                stats["unique_countries"] = df[col].nunique()
            except:
                pass
            break
    
    # Find tracking column
    for col in df.columns:
        if get_standard_column_name(col) == "courier_tracking_ids":
            try:
                stats["with_tracking"] = df[col].apply(lambda x: is_valid_value(x)).sum()
            except:
                pass
            break
    
    return stats

# =============================================================================
# UI COMPONENTS
# =============================================================================

def render_result_card(result, show_valid_only=False):
    """Render a single result card using native Streamlit components"""
    partner = result["partner"]
    source = result["source"]
    order_id = result["order_id"]
    data = result["data"]
    
    partner_icon = PARTNER_COLORS.get(partner, "⚪")
    
    with st.expander(f"{partner_icon} **{partner}** - {source} | Order: **{order_id}**", expanded=True):
        # Create columns for fields (4 per row)
        fields = list(data.items())
        
        # Filter if show_valid_only
        if show_valid_only:
            fields = [(k, v) for k, v in fields if is_valid_value(v)]
        
        if not fields:
            st.info("No valid data found for this order")
            return
        
        # Display fields in 4 columns
        for i in range(0, len(fields), 4):
            cols = st.columns(4)
            for j, col in enumerate(cols):
                if i + j < len(fields):
                    field_name, field_value = fields[i + j]
                    icon = FIELD_ICONS.get(field_name, "📌")
                    with col:
                        st.markdown(f"**{icon} {field_name.title()}**")
                        if is_valid_value(field_value):
                            st.text(str(field_value)[:50])
                        else:
                            st.text("—")

def render_search_tab():
    """Render the global search tab"""
    st.markdown('<p class="main-header">🔍 TID Search Tool</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Search across all logistics partners: ECL, GE, APX, Kerry</p>', unsafe_allow_html=True)
    
    # Search input
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_input = st.text_area(
            "Enter Order ID(s)",
            placeholder="Enter one or multiple order IDs\nSeparated by new lines, commas, or spaces",
            height=100
        )
    
    with col2:
        st.write("")
        st.write("")
        search_button = st.button("🔍 Search", use_container_width=True, type="primary")
        show_valid_only = st.checkbox("Valid values only", value=False)
    
    # Perform search
    if search_button and search_input:
        order_ids = parse_order_ids(search_input)
        
        if not order_ids:
            st.warning("Please enter at least one order ID")
            return
        
        with st.spinner(f"Searching for {len(order_ids)} order(s) across all sources..."):
            results = search_all_sources(order_ids)
        
        # Display results
        if results:
            st.success(f"✅ Found {len(results)} result(s) for {len(order_ids)} order(s)")
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            
            partners_found = list(set(r["partner"] for r in results))
            sources_found = list(set(r["source"] for r in results))
            
            with col1:
                st.metric("Total Results", len(results))
            with col2:
                st.metric("Orders Searched", len(order_ids))
            with col3:
                st.metric("Partners Found", len(partners_found))
            with col4:
                st.metric("Sources Matched", len(sources_found))
            
            st.divider()
            
            # Display each result
            for result in results:
                render_result_card(result, show_valid_only)
        else:
            st.error(f"❌ No results found for: {', '.join(order_ids)}")
            st.info("💡 Tips:\n- Check if the order ID is correct\n- Try searching with different formats\n- Order might not be in the system yet")

def render_data_tab(source_name):
    """Render a data source tab"""
    config = DATA_SOURCES[source_name]
    partner = config["partner"]
    partner_icon = PARTNER_COLORS.get(partner, "⚪")
    
    st.markdown(f"## {partner_icon} {source_name}")
    
    # Load data
    with st.spinner(f"Loading {source_name} data..."):
        df = load_data(source_name)
    
    if df.empty:
        st.error(f"Failed to load data from {source_name}")
        return
    
    # Filter to TID columns
    df_filtered = filter_tid_columns_df(df)
    
    # Stats
    stats = calculate_stats(df, source_name)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("📦 Total Orders", f"{stats['total_orders']:,}")
    with col2:
        st.metric("📦 Total Boxes", f"{int(stats['total_boxes']):,}")
    with col3:
        st.metric("⚖️ Total Weight (kg)", f"{stats['total_weight']:,.1f}")
    with col4:
        st.metric("🌍 Countries", stats['unique_countries'])
    with col5:
        st.metric("📍 With Tracking", f"{stats['with_tracking']:,}")
    
    st.divider()
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_filter = st.text_input("🔍 Quick Search", key=f"filter_{source_name}")
    
    with col2:
        # Find date column
        date_col = None
        for col in df.columns:
            if get_standard_column_name(col) == "date":
                date_col = col
                break
        
        if date_col:
            try:
                df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
                min_date = df[date_col].min()
                max_date = df[date_col].max()
                if pd.notna(min_date) and pd.notna(max_date):
                    date_range = st.date_input(
                        "📅 Date Range",
                        value=(min_date, max_date),
                        key=f"date_{source_name}"
                    )
            except:
                date_range = None
        else:
            date_range = None
    
    with col3:
        show_all_cols = st.checkbox("Show all columns", key=f"allcols_{source_name}")
    
    # Apply filters
    display_df = df if show_all_cols else df_filtered
    
    if search_filter:
        mask = display_df.astype(str).apply(lambda x: x.str.contains(search_filter, case=False, na=False)).any(axis=1)
        display_df = display_df[mask]
    
    # Display dataframe
    st.dataframe(
        display_df,
        use_container_width=True,
        height=500
    )
    
    # Download button
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        csv = display_df.to_csv(index=False)
        st.download_button(
            "📥 Download CSV",
            csv,
            f"{source_name.lower().replace(' ', '_')}_data.csv",
            "text/csv",
            use_container_width=True
        )
    with col2:
        st.button("🔄 Refresh Data", key=f"refresh_{source_name}", on_click=lambda: load_data.clear())

# =============================================================================
# MAIN APP
# =============================================================================

def main():
    # Create tabs
    tabs = st.tabs([
        "🔍 Global Search",
        "🟠 ECL QC Center",
        "🟠 ECL Zone", 
        "🔵 GE QC Center",
        "🔵 GE Zone",
        "🟣 APX",
        "🟢 Kerry"
    ])
    
    with tabs[0]:
        render_search_tab()
    
    with tabs[1]:
        render_data_tab("ECL QC Center")
    
    with tabs[2]:
        render_data_tab("ECL Zone")
    
    with tabs[3]:
        render_data_tab("GE QC Center")
    
    with tabs[4]:
        render_data_tab("GE Zone")
    
    with tabs[5]:
        render_data_tab("APX")
    
    with tabs[6]:
        render_data_tab("Kerry")

if __name__ == "__main__":
    main()
