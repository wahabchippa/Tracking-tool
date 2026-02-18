import streamlit as st
import pandas as pd
import requests
from io import StringIO
import concurrent.futures

# Page config
st.set_page_config(
    page_title="TID Search Tool",
    page_icon="🔍",
    layout="wide"
)

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

PARTNER_ICONS = {"ECL": "🟠", "GE": "🔵", "APX": "🟣", "Kerry": "🟢"}

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
# DATA LOADING - ONE TIME ONLY!
# =============================================================================

def fetch_single_source(source_name):
    """Fetch one source"""
    try:
        config = DATA_SOURCES[source_name]
        response = requests.get(config["url"], timeout=120)
        df = pd.read_csv(StringIO(response.text))
        
        # Get order column name
        order_col = config["order_col"]
        if isinstance(order_col, int):
            order_col = df.columns[order_col]
        
        # Convert order column to string for fast search
        if order_col in df.columns:
            df["_search_col"] = df[order_col].astype(str).str.lower().str.strip()
        
        return source_name, df, order_col, None
    except Exception as e:
        return source_name, pd.DataFrame(), None, str(e)

def load_all_data():
    """Load ALL data once - parallel"""
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
    """Initialize data in session state - RUNS ONLY ONCE"""
    if "data_loaded" not in st.session_state:
        with st.spinner("🚀 Loading all data (one time only)..."):
            st.session_state.all_data, st.session_state.load_errors = load_all_data()
            st.session_state.data_loaded = True
            
            # Count total rows
            total = sum(len(d["df"]) for d in st.session_state.all_data.values())
            st.session_state.total_rows = total

# =============================================================================
# INSTANT SEARCH - NO NETWORK!
# =============================================================================

def instant_search(order_ids):
    """Search in memory - INSTANT! ⚡"""
    results = []
    
    for order_id in order_ids:
        search_term = order_id.lower().strip()
        if not search_term:
            continue
        
        for source_name, source_data in st.session_state.all_data.items():
            df = source_data["df"]
            if df.empty or "_search_col" not in df.columns:
                continue
            
            # INSTANT search in memory!
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
    """Map column to standard name"""
    col_lower = col.lower().strip()
    for std, aliases in COLUMN_ALIASES.items():
        if col_lower in aliases:
            return std
    return None

def filter_tid_data(data):
    """Filter to TID columns"""
    filtered = {}
    for col, val in data.items():
        if col == "_search_col":
            continue
        std = get_standard_name(col)
        if std:
            filtered[std] = val
        elif len(filtered) < 15:  # Show some extra if no match
            filtered[col] = val
    return filtered

def is_valid(val):
    """Check if value is valid"""
    if val is None:
        return False
    s = str(val).lower().strip()
    return s not in ['', 'nan', 'none', 'n/a', '#n/a', 'na', '-', 'null']

# =============================================================================
# UI
# =============================================================================

def show_result(result, valid_only):
    """Display one result"""
    partner = result["partner"]
    icon = PARTNER_ICONS.get(partner, "⚪")
    data = filter_tid_data(result["data"])
    
    with st.expander(f"{icon} **{partner}** - {result['source']} | Order: **{result['order_id']}**", expanded=True):
        fields = [(k, v) for k, v in data.items() if not valid_only or is_valid(v)]
        
        if not fields:
            st.info("No data")
            return
        
        for i in range(0, len(fields), 4):
            cols = st.columns(4)
            for j in range(4):
                if i + j < len(fields):
                    name, val = fields[i + j]
                    icon = FIELD_ICONS.get(name, "📌")
                    with cols[j]:
                        st.markdown(f"**{icon} {name}**")
                        st.text(str(val)[:50] if is_valid(val) else "—")

def search_tab():
    """Search tab"""
    st.markdown("## 🔍 TID Search Tool")
    st.caption("Search across ECL, GE, APX, Kerry - **INSTANT RESULTS!** ⚡")
    
    # Show data status
    if st.session_state.data_loaded:
        sources_ok = sum(1 for d in st.session_state.all_data.values() if not d["df"].empty)
        st.success(f"✅ Data ready: **{st.session_state.total_rows:,}** rows from **{sources_ok}** sources")
    
    # Search input
    col1, col2 = st.columns([4, 1])
    
    with col1:
        search_input = st.text_input(
            "🔍 Enter Order ID(s)",
            placeholder="e.g., 122054_98, 122055_99"
        )
    
    with col2:
        valid_only = st.checkbox("Valid only")
    
    # INSTANT SEARCH on Enter or button
    if search_input:
        import re
        order_ids = [x.strip() for x in re.split(r'[\n,\t\s]+', search_input) if x.strip()]
        
        if order_ids:
            # ⚡ INSTANT - no spinner needed!
            import time
            start = time.time()
            results = instant_search(order_ids)
            search_time = (time.time() - start) * 1000  # milliseconds
            
            if results:
                st.success(f"✅ Found **{len(results)}** results in **{search_time:.1f}ms** ⚡")
                
                for result in results:
                    show_result(result, valid_only)
            else:
                st.warning(f"❌ No results for: {', '.join(order_ids)}")

def data_tab(source_name):
    """Data tab"""
    config = DATA_SOURCES[source_name]
    icon = PARTNER_ICONS.get(config["partner"], "⚪")
    
    st.markdown(f"## {icon} {source_name}")
    
    source_data = st.session_state.all_data.get(source_name, {})
    df = source_data.get("df", pd.DataFrame())
    
    if df.empty:
        st.error("No data loaded")
        return
    
    # Stats
    col1, col2, col3 = st.columns(3)
    col1.metric("📦 Total Rows", f"{len(df):,}")
    col2.metric("📊 Columns", len(df.columns))
    col3.metric("📁 Source", config["partner"])
    
    # Filter
    filter_text = st.text_input("🔍 Filter", key=f"f_{source_name}")
    
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
    # LOAD DATA ONCE!
    initialize_data()
    
    # Show errors if any
    if st.session_state.get("load_errors"):
        with st.sidebar:
            with st.expander("⚠️ Load warnings"):
                for err in st.session_state.load_errors:
                    st.warning(err)
    
    # Refresh button in sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        if st.button("🔄 Reload All Data"):
            del st.session_state.data_loaded
            st.rerun()
    
    # Tabs
    tabs = st.tabs([
        "🔍 Search",
        "🟠 ECL QC",
        "🟠 ECL Zone",
        "🔵 GE QC",
        "🔵 GE Zone",
        "🟣 APX",
        "🟢 Kerry"
    ])
    
    with tabs[0]:
        search_tab()
    with tabs[1]:
        data_tab("ECL QC Center")
    with tabs[2]:
        data_tab("ECL Zone")
    with tabs[3]:
        data_tab("GE QC Center")
    with tabs[4]:
        data_tab("GE Zone")
    with tabs[5]:
        data_tab("APX")
    with tabs[6]:
        data_tab("Kerry")

if __name__ == "__main__":
    main()
