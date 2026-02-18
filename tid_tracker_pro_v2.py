import streamlit as st
import pandas as pd
import requests
from io import StringIO
from datetime import datetime
import concurrent.futures

# Page config
st.set_page_config(
    page_title="TID Search Tool",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS
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
# TID COLUMNS CONFIG
# =============================================================================

TID_REQUIRED_COLUMNS = [
    "date", "order#", "upload date", "services", "order_id", "line_item_batch_id",
    "fulfillment_id", "invoice_id", "invoice_type", "weight_kgs", "box_count",
    "airway_bill", "courier_service", "courier_tracking_ids", "reference",
    "shipping_account", "consignee", "destination"
]

COLUMN_ALIASES = {
    "date": ["date", "fleek handover date", "airport handover date", "handover date"],
    "order#": ["order#", "order", "fleek id", "_order", "order no", "order no.", "order num", "order_id"],
    "upload date": ["upload date", "upload_date", "uploaded date"],
    "services": ["services", "service", "partner", "3pl"],
    "order_id": ["order_id", "orderid", "order id"],
    "line_item_batch_id": ["line_item_batch_id", "line item batch id", "batch id"],
    "fulfillment_id": ["fulfillment_id", "fulfillment id", "fulfillment"],
    "invoice_id": ["invoice_id", "invoice id", "invoice"],
    "invoice_type": ["invoice_type", "invoice type"],
    "weight_kgs": ["weight_kgs", "weight (kg)", "weight", "order net weight", "net weight"],
    "box_count": ["box_count", "boxes", "box count", "no of boxes"],
    "airway_bill": ["airway_bill", "awb", "hawb", "mawb", "apx awb number", "kerry awb number", "ge awb"],
    "courier_service": ["courier_service", "courier", "carrier"],
    "courier_tracking_ids": ["courier_tracking_ids", "tracking id", "tracking_id", "tracking"],
    "reference": ["reference", "ref"],
    "shipping_account": ["shipping_account", "shipping account"],
    "consignee": ["consignee", "customer name", "customer_name", "customer", "name"],
    "destination": ["destination", "country", "city"]
}

FIELD_ICONS = {
    "date": "📅", "order#": "🆔", "upload date": "📤", "services": "⚙️",
    "order_id": "🔢", "line_item_batch_id": "📑", "fulfillment_id": "✅",
    "invoice_id": "🧾", "invoice_type": "📋", "weight_kgs": "⚖️",
    "box_count": "📦", "airway_bill": "🎫", "courier_service": "🚚",
    "courier_tracking_ids": "📍", "reference": "🔗", "shipping_account": "📮",
    "consignee": "👤", "destination": "🎯"
}

PARTNER_COLORS = {"ECL": "🟠", "GE": "🔵", "APX": "🟣", "Kerry": "🟢"}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_standard_column_name(col_name):
    """Map column name to standard TID column name"""
    col_lower = col_name.lower().strip()
    for standard_name, aliases in COLUMN_ALIASES.items():
        if col_lower in [a.lower() for a in aliases]:
            return standard_name
    return None

def is_tid_column(col_name):
    return get_standard_column_name(col_name) is not None

def is_valid_value(value):
    if value is None:
        return False
    str_val = str(value).lower().strip()
    invalid = ['#n/a', 'n/a', 'na', 'not applicable', 'none', '', '-', 'nan', 'null']
    return str_val not in invalid

def fetch_csv_data(url, timeout=60):
    """Fetch CSV with retry logic"""
    for attempt in range(3):  # 3 attempts
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return response.text
        except requests.exceptions.Timeout:
            if attempt < 2:
                continue
            return None
        except Exception:
            return None
    return None

@st.cache_data(ttl=600, show_spinner=False)  # Cache for 10 minutes
def load_data(source_name):
    """Load data from source with better error handling"""
    try:
        config = DATA_SOURCES[source_name]
        csv_text = fetch_csv_data(config["url"])
        
        if csv_text is None:
            return pd.DataFrame(), f"Timeout loading {source_name}"
        
        df = pd.read_csv(StringIO(csv_text))
        
        # Handle index-based column
        order_col = config["order_col"]
        if isinstance(order_col, int):
            config["order_col_actual"] = df.columns[order_col]
        else:
            config["order_col_actual"] = order_col
        
        return df, None
    except Exception as e:
        return pd.DataFrame(), str(e)

def load_all_data_parallel():
    """Load all data sources in parallel"""
    results = {}
    errors = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        future_to_source = {
            executor.submit(load_data, source): source 
            for source in DATA_SOURCES.keys()
        }
        
        for future in concurrent.futures.as_completed(future_to_source):
            source = future_to_source[future]
            try:
                df, error = future.result()
                results[source] = df
                if error:
                    errors.append(f"{source}: {error}")
            except Exception as e:
                results[source] = pd.DataFrame()
                errors.append(f"{source}: {str(e)}")
    
    return results, errors

def filter_tid_columns(data_dict):
    """Filter to TID columns only"""
    filtered = {}
    for col, value in data_dict.items():
        standard_name = get_standard_column_name(col)
        if standard_name:
            filtered[standard_name] = value
    return filtered if filtered else data_dict

def filter_tid_columns_df(df):
    """Filter DataFrame to TID columns"""
    tid_cols = [col for col in df.columns if is_tid_column(col)]
    return df[tid_cols] if tid_cols else df

def search_in_dataframe(df, order_id, source_name):
    """Search for order in a dataframe"""
    if df.empty:
        return []
    
    config = DATA_SOURCES[source_name]
    order_col = config.get("order_col_actual", config["order_col"])
    
    if isinstance(order_col, int):
        order_col = df.columns[order_col]
    
    if order_col not in df.columns:
        return []
    
    df[order_col] = df[order_col].astype(str)
    matches = df[df[order_col].str.lower().str.strip() == str(order_id).lower().strip()]
    
    results = []
    for _, row in matches.iterrows():
        results.append({
            "source": source_name,
            "partner": config["partner"],
            "color": config["color"],
            "order_id": order_id,
            "data": filter_tid_columns(row.to_dict())
        })
    
    return results

def parse_order_ids(input_text):
    """Parse order IDs from input"""
    import re
    order_ids = re.split(r'[\n,\t\s]+', input_text)
    return [oid.strip() for oid in order_ids if oid.strip()]

def calculate_stats(df, source_name):
    """Calculate stats for dataframe"""
    stats = {"total_orders": len(df), "total_boxes": 0, "total_weight": 0, 
             "unique_countries": 0, "with_tracking": 0}
    
    for col in df.columns:
        std_name = get_standard_column_name(col)
        if std_name == "box_count":
            stats["total_boxes"] = pd.to_numeric(df[col], errors='coerce').sum()
        elif std_name == "weight_kgs":
            stats["total_weight"] = pd.to_numeric(df[col], errors='coerce').sum()
        elif std_name == "destination":
            stats["unique_countries"] = df[col].nunique()
        elif std_name == "courier_tracking_ids":
            stats["with_tracking"] = df[col].apply(lambda x: is_valid_value(x)).sum()
    
    return stats

# =============================================================================
# UI COMPONENTS
# =============================================================================

def render_result_card(result, show_valid_only=False):
    """Render result card"""
    partner = result["partner"]
    source = result["source"]
    order_id = result["order_id"]
    data = result["data"]
    
    partner_icon = PARTNER_COLORS.get(partner, "⚪")
    
    with st.expander(f"{partner_icon} **{partner}** - {source} | Order: **{order_id}**", expanded=True):
        fields = list(data.items())
        
        if show_valid_only:
            fields = [(k, v) for k, v in fields if is_valid_value(v)]
        
        if not fields:
            st.info("No valid data found")
            return
        
        for i in range(0, len(fields), 4):
            cols = st.columns(4)
            for j, col in enumerate(cols):
                if i + j < len(fields):
                    field_name, field_value = fields[i + j]
                    icon = FIELD_ICONS.get(field_name, "📌")
                    with col:
                        st.markdown(f"**{icon} {field_name.title()}**")
                        st.text(str(field_value)[:50] if is_valid_value(field_value) else "—")

def render_search_tab():
    """Render search tab"""
    st.markdown('<p class="main-header">🔍 TID Search Tool</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Search across all logistics partners: ECL, GE, APX, Kerry</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_input = st.text_area(
            "Enter Order ID(s)",
            placeholder="Enter order IDs (comma, space, or newline separated)",
            height=100
        )
    
    with col2:
        st.write("")
        st.write("")
        search_button = st.button("🔍 Search", use_container_width=True, type="primary")
        show_valid_only = st.checkbox("Valid values only", value=False)
    
    if search_button and search_input:
        order_ids = parse_order_ids(search_input)
        
        if not order_ids:
            st.warning("Please enter at least one order ID")
            return
        
        # Load all data in parallel first
        progress_text = st.empty()
        progress_bar = st.progress(0)
        
        progress_text.text("📥 Loading data from all sources...")
        progress_bar.progress(10)
        
        all_data, load_errors = load_all_data_parallel()
        
        progress_bar.progress(50)
        
        # Show any loading errors
        if load_errors:
            with st.expander("⚠️ Some sources had issues loading", expanded=False):
                for err in load_errors:
                    st.warning(err)
        
        progress_text.text("🔍 Searching orders...")
        progress_bar.progress(70)
        
        # Search in all loaded data
        all_results = []
        for order_id in order_ids:
            order_id = order_id.strip()
            if not order_id:
                continue
            
            for source_name, df in all_data.items():
                if not df.empty:
                    results = search_in_dataframe(df, order_id, source_name)
                    all_results.extend(results)
        
        progress_bar.progress(100)
        progress_text.empty()
        progress_bar.empty()
        
        # Display results
        if all_results:
            st.success(f"✅ Found {len(all_results)} result(s) for {len(order_ids)} order(s)")
            
            col1, col2, col3, col4 = st.columns(4)
            partners_found = list(set(r["partner"] for r in all_results))
            sources_found = list(set(r["source"] for r in all_results))
            
            col1.metric("Total Results", len(all_results))
            col2.metric("Orders Searched", len(order_ids))
            col3.metric("Partners Found", len(partners_found))
            col4.metric("Sources Matched", len(sources_found))
            
            st.divider()
            
            for result in all_results:
                render_result_card(result, show_valid_only)
        else:
            st.error(f"❌ No results found for: {', '.join(order_ids)}")
            st.info("💡 Check order ID or try different format")

def render_data_tab(source_name):
    """Render data tab"""
    config = DATA_SOURCES[source_name]
    partner_icon = PARTNER_COLORS.get(config["partner"], "⚪")
    
    st.markdown(f"## {partner_icon} {source_name}")
    
    with st.spinner(f"Loading {source_name}..."):
        df, error = load_data(source_name)
    
    if error:
        st.error(f"Error: {error}")
        if st.button("🔄 Retry", key=f"retry_{source_name}"):
            load_data.clear()
            st.rerun()
        return
    
    if df.empty:
        st.warning("No data available")
        return
    
    df_filtered = filter_tid_columns_df(df)
    stats = calculate_stats(df, source_name)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("📦 Orders", f"{stats['total_orders']:,}")
    col2.metric("📦 Boxes", f"{int(stats['total_boxes']):,}")
    col3.metric("⚖️ Weight (kg)", f"{stats['total_weight']:,.1f}")
    col4.metric("🌍 Countries", stats['unique_countries'])
    col5.metric("📍 Tracking", f"{stats['with_tracking']:,}")
    
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_filter = st.text_input("🔍 Filter", key=f"filter_{source_name}")
    with col2:
        show_all = st.checkbox("Show all columns", key=f"all_{source_name}")
    with col3:
        if st.button("🔄 Refresh", key=f"refresh_{source_name}"):
            load_data.clear()
            st.rerun()
    
    display_df = df if show_all else df_filtered
    
    if search_filter:
        mask = display_df.astype(str).apply(
            lambda x: x.str.contains(search_filter, case=False, na=False)
        ).any(axis=1)
        display_df = display_df[mask]
    
    st.dataframe(display_df, use_container_width=True, height=500)
    
    csv = display_df.to_csv(index=False)
    st.download_button(
        "📥 Download CSV",
        csv,
        f"{source_name.lower().replace(' ', '_')}.csv",
        "text/csv"
    )

# =============================================================================
# MAIN APP
# =============================================================================

def main():
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
