import streamlit as st
import pandas as pd
import requests
from io import StringIO
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# ═══════════════════════════════════════════════════════════════════════════════
# 🎨 PREMIUM DARK THEME - CLASSY LOOK
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="TrackMaster Pro",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

CLASSY_THEME = """
<style>
/* ═══════════════════════════════════════════════════════════════════════════════
   🌟 PREMIUM DARK THEME - TRACKMASTER PRO
   ═══════════════════════════════════════════════════════════════════════════════ */

/* Import Premium Font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* Root Variables */
:root {
    --bg-primary: #0a0a0f;
    --bg-secondary: #12121a;
    --bg-card: #16161f;
    --bg-hover: #1c1c28;
    --border-color: #2a2a3d;
    --border-glow: #3d3d5c;
    --text-primary: #f4f4f8;
    --text-secondary: #9898b0;
    --text-muted: #6b6b82;
    --accent-blue: #6366f1;
    --accent-purple: #a855f7;
    --accent-pink: #ec4899;
    --accent-cyan: #22d3ee;
    --accent-green: #10b981;
    --accent-orange: #f97316;
    --accent-yellow: #eab308;
    --gradient-primary: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
    --gradient-blue: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%);
    --gradient-purple: linear-gradient(135deg, #8b5cf6 0%, #a855f7 100%);
    --gradient-green: linear-gradient(135deg, #10b981 0%, #22d3ee 100%);
    --gradient-orange: linear-gradient(135deg, #f97316 0%, #eab308 100%);
    --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.3);
    --shadow-md: 0 4px 20px rgba(0, 0, 0, 0.4);
    --shadow-lg: 0 8px 40px rgba(0, 0, 0, 0.5);
    --shadow-glow-blue: 0 0 30px rgba(99, 102, 241, 0.3);
    --shadow-glow-purple: 0 0 30px rgba(168, 85, 247, 0.3);
    --shadow-glow-green: 0 0 30px rgba(16, 185, 129, 0.3);
}

/* Global Styles */
.stApp {
    background: var(--bg-primary);
    background-image: 
        radial-gradient(ellipse at 20% 20%, rgba(99, 102, 241, 0.08) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 80%, rgba(168, 85, 247, 0.08) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 50%, rgba(236, 72, 153, 0.04) 0%, transparent 70%);
    font-family: 'Inter', sans-serif;
}

/* Hide Streamlit Elements */
#MainMenu, footer, header {visibility: hidden;}
.stDeployButton {display: none;}

/* ═══════════════════════════════════════════════════════════════════════════════
   📱 SIDEBAR STYLING
   ═══════════════════════════════════════════════════════════════════════════════ */

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--bg-secondary) 0%, var(--bg-primary) 100%);
    border-right: 1px solid var(--border-color);
}

section[data-testid="stSidebar"] .stRadio > label {
    color: var(--text-secondary) !important;
    font-weight: 600;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 12px;
}

section[data-testid="stSidebar"] .stRadio > div {
    gap: 6px;
}

section[data-testid="stSidebar"] .stRadio > div > label {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 14px 18px !important;
    color: var(--text-primary) !important;
    font-weight: 500;
    font-size: 0.95rem;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    margin: 0;
}

section[data-testid="stSidebar"] .stRadio > div > label:hover {
    background: var(--bg-hover);
    border-color: var(--accent-blue);
    transform: translateX(4px);
    box-shadow: var(--shadow-glow-blue);
}

section[data-testid="stSidebar"] .stRadio > div > label[data-checked="true"] {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(168, 85, 247, 0.2) 100%);
    border-color: var(--accent-purple);
    box-shadow: var(--shadow-glow-purple);
}

/* ═══════════════════════════════════════════════════════════════════════════════
   🔍 SEARCH INPUT - PREMIUM STYLE
   ═══════════════════════════════════════════════════════════════════════════════ */

.stTextArea textarea {
    background: var(--bg-card) !important;
    border: 2px solid var(--border-color) !important;
    border-radius: 16px !important;
    color: var(--text-primary) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1rem !important;
    padding: 16px 20px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.stTextArea textarea:focus {
    border-color: var(--accent-blue) !important;
    box-shadow: var(--shadow-glow-blue), inset 0 0 20px rgba(99, 102, 241, 0.1) !important;
    outline: none !important;
}

.stTextArea textarea::placeholder {
    color: var(--text-muted) !important;
}

/* ═══════════════════════════════════════════════════════════════════════════════
   🎯 BUTTONS - GRADIENT STYLE
   ═══════════════════════════════════════════════════════════════════════════════ */

.stButton > button {
    background: var(--gradient-primary) !important;
    border: none !important;
    border-radius: 14px !important;
    color: white !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 14px 32px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: var(--shadow-md), 0 0 20px rgba(99, 102, 241, 0.3) !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.stButton > button:hover {
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: var(--shadow-lg), 0 0 40px rgba(168, 85, 247, 0.4) !important;
}

.stButton > button:active {
    transform: translateY(0) scale(0.98) !important;
}

/* Download Button */
.stDownloadButton > button {
    background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-hover) 100%) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
    font-weight: 500 !important;
    padding: 12px 24px !important;
    transition: all 0.3s ease !important;
}

.stDownloadButton > button:hover {
    border-color: var(--accent-green) !important;
    box-shadow: var(--shadow-glow-green) !important;
}

/* ═══════════════════════════════════════════════════════════════════════════════
   📊 METRICS - GLASS MORPHISM
   ═══════════════════════════════════════════════════════════════════════════════ */

[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 20px 24px;
    transition: all 0.3s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    border-color: rgba(99, 102, 241, 0.3);
    box-shadow: var(--shadow-glow-blue);
}

[data-testid="stMetricLabel"] {
    color: var(--text-secondary) !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}

[data-testid="stMetricValue"] {
    color: var(--text-primary) !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
    background: var(--gradient-primary);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* ═══════════════════════════════════════════════════════════════════════════════
   📋 DATAFRAME - SLEEK TABLE
   ═══════════════════════════════════════════════════════════════════════════════ */

.stDataFrame {
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid var(--border-color);
    box-shadow: var(--shadow-md);
}

[data-testid="stDataFrame"] > div {
    background: var(--bg-card) !important;
    border-radius: 16px;
}

/* ═══════════════════════════════════════════════════════════════════════════════
   📝 TEXT ELEMENTS
   ═══════════════════════════════════════════════════════════════════════════════ */

.stMarkdown p {
    color: var(--text-secondary);
}

h1, h2, h3 {
    color: var(--text-primary) !important;
}

/* Divider */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border-color), transparent);
    margin: 24px 0;
}

/* ═══════════════════════════════════════════════════════════════════════════════
   🔄 SPINNER / LOADING
   ═══════════════════════════════════════════════════════════════════════════════ */

.stSpinner > div {
    border-color: var(--accent-purple) transparent transparent transparent !important;
}

/* ═══════════════════════════════════════════════════════════════════════════════
   📜 CUSTOM SCROLLBAR
   ═══════════════════════════════════════════════════════════════════════════════ */

::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: var(--bg-primary);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, var(--accent-blue), var(--accent-purple));
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, var(--accent-purple), var(--accent-pink));
}

/* ═══════════════════════════════════════════════════════════════════════════════
   ✨ ANIMATIONS
   ═══════════════════════════════════════════════════════════════════════════════ */

@keyframes shimmer {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}

@keyframes pulse-glow {
    0%, 100% { box-shadow: 0 0 20px rgba(99, 102, 241, 0.3); }
    50% { box-shadow: 0 0 40px rgba(168, 85, 247, 0.5); }
}

/* ═══════════════════════════════════════════════════════════════════════════════
   🎯 ALERTS & MESSAGES
   ═══════════════════════════════════════════════════════════════════════════════ */

.stAlert {
    border-radius: 14px !important;
    border: none !important;
    backdrop-filter: blur(10px);
}

[data-testid="stAlert"] {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(168, 85, 247, 0.1) 100%) !important;
    border-left: 4px solid var(--accent-purple) !important;
}

/* Success */
.stSuccess {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(34, 211, 238, 0.1) 100%) !important;
    border-left: 4px solid var(--accent-green) !important;
}

/* Warning */
.stWarning {
    background: linear-gradient(135deg, rgba(249, 115, 22, 0.1) 0%, rgba(234, 179, 8, 0.1) 100%) !important;
    border-left: 4px solid var(--accent-orange) !important;
}

/* Error */
.stError {
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(236, 72, 153, 0.1) 100%) !important;
    border-left: 4px solid var(--accent-pink) !important;
}

/* ═══════════════════════════════════════════════════════════════════════════════
   🏷️ EXPANDER
   ═══════════════════════════════════════════════════════════════════════════════ */

.streamlit-expanderHeader {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
    font-weight: 600 !important;
}

.streamlit-expanderContent {
    background: var(--bg-secondary) !important;
    border: 1px solid var(--border-color) !important;
    border-top: none !important;
    border-radius: 0 0 12px 12px !important;
}

/* ═══════════════════════════════════════════════════════════════════════════════
   🔲 TEXT INPUT
   ═══════════════════════════════════════════════════════════════════════════════ */

.stTextInput input {
    background: var(--bg-card) !important;
    border: 2px solid var(--border-color) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
    font-family: 'JetBrains Mono', monospace !important;
    padding: 12px 16px !important;
    transition: all 0.3s ease !important;
}

.stTextInput input:focus {
    border-color: var(--accent-blue) !important;
    box-shadow: var(--shadow-glow-blue) !important;
}

/* Labels */
.stTextInput label, .stTextArea label, .stSelectbox label {
    color: var(--text-secondary) !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
</style>
"""

st.markdown(CLASSY_THEME, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 🎯 PREMIUM HEADER COMPONENT
# ═══════════════════════════════════════════════════════════════════════════════

def render_premium_header():
    """Render a stunning premium header"""
    header_html = """
    <style>
    .premium-header {
        padding: 30px 0 40px 0;
        text-align: center;
        position: relative;
    }
    
    .brand-icon {
        font-size: 4rem;
        margin-bottom: 16px;
        display: inline-block;
        animation: float 3s ease-in-out infinite;
        filter: drop-shadow(0 0 20px rgba(99, 102, 241, 0.5));
    }
    
    .brand-title {
        font-family: 'Inter', sans-serif;
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 30%, #ec4899 60%, #22d3ee 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        letter-spacing: -2px;
        text-shadow: 0 0 40px rgba(99, 102, 241, 0.3);
        animation: shimmer 3s ease-in-out infinite;
        background-size: 200% auto;
    }
    
    .brand-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        font-weight: 500;
        color: #9898b0;
        margin-top: 12px;
        letter-spacing: 3px;
        text-transform: uppercase;
    }
    
    .header-line {
        width: 120px;
        height: 4px;
        background: linear-gradient(90deg, #6366f1, #a855f7, #ec4899);
        border-radius: 2px;
        margin: 24px auto 0 auto;
        box-shadow: 0 0 20px rgba(168, 85, 247, 0.5);
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-10px) rotate(5deg); }
    }
    
    @keyframes shimmer {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    </style>
    
    <div class="premium-header">
        <div class="brand-icon">🔎</div>
        <h1 class="brand-title">TrackMaster Pro</h1>
        <p class="brand-subtitle">Intelligent Shipment Tracking System</p>
        <div class="header-line"></div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)


def render_mini_header():
    """Render a compact header for sidebar or secondary pages"""
    mini_header = """
    <style>
    .mini-header {
        padding: 16px;
        text-align: center;
        margin-bottom: 20px;
    }
    
    .mini-logo {
        font-size: 2.5rem;
        filter: drop-shadow(0 0 15px rgba(99, 102, 241, 0.5));
    }
    
    .mini-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.4rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6366f1, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 8px 0 0 0;
    }
    </style>
    
    <div class="mini-header">
        <div class="mini-logo">🔎</div>
        <div class="mini-title">TrackMaster Pro</div>
    </div>
    """
    st.markdown(mini_header, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# 🎨 PREMIUM RESULT CARD STYLING
# ═══════════════════════════════════════════════════════════════════════════════

def get_partner_theme(partner):
    """Get premium color theme for each partner"""
    themes = {
        "ECL": {
            "gradient": "linear-gradient(135deg, #f97316 0%, #eab308 100%)",
            "glow": "rgba(249, 115, 22, 0.3)",
            "border": "#f97316",
            "icon": "🟠"
        },
        "GE": {
            "gradient": "linear-gradient(135deg, #3b82f6 0%, #6366f1 100%)",
            "glow": "rgba(99, 102, 241, 0.3)",
            "border": "#6366f1",
            "icon": "🔵"
        },
        "APX": {
            "gradient": "linear-gradient(135deg, #8b5cf6 0%, #a855f7 100%)",
            "glow": "rgba(168, 85, 247, 0.3)",
            "border": "#a855f7",
            "icon": "🟣"
        },
        "Kerry": {
            "gradient": "linear-gradient(135deg, #10b981 0%, #22d3ee 100%)",
            "glow": "rgba(16, 185, 129, 0.3)",
            "border": "#10b981",
            "icon": "🟢"
        }
    }
    return themes.get(partner, themes["GE"])


def render_result_card_header(result):
    """Render premium card header"""
    partner = result.get("partner", "Unknown")
    source = result.get("source", "Unknown")
    order_id = result.get("order_id", "N/A")
    theme = get_partner_theme(partner)
    
    header_html = f"""
    <style>
    .result-card-header {{
        background: {theme["gradient"]};
        border-radius: 16px 16px 0 0;
        padding: 20px 24px;
        margin-top: 24px;
        box-shadow: 0 4px 20px {theme["glow"]};
        position: relative;
        overflow: hidden;
    }}
    
    .result-card-header::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, transparent 50%);
        pointer-events: none;
    }}
    
    .header-content {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: relative;
        z-index: 1;
    }}
    
    .header-left {{
        display: flex;
        align-items: center;
        gap: 14px;
    }}
    
    .partner-badge {{
        font-size: 2rem;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
    }}
    
    .source-info {{
        color: white;
    }}
    
    .source-name {{
        font-size: 1.3rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }}
    
    .source-type {{
        font-size: 0.85rem;
        opacity: 0.9;
        font-weight: 500;
    }}
    
    .order-badge {{
        background: rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.3);
        border-radius: 12px;
        padding: 10px 18px;
        color: white;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
        font-size: 1.1rem;
        letter-spacing: 0.5px;
    }}
    </style>
    
    <div class="result-card-header">
        <div class="header-content">
            <div class="header-left">
                <div class="partner-badge">{theme["icon"]}</div>
                <div class="source-info">
                    <div class="source-name">{partner}</div>
                    <div class="source-type">{source}</div>
                </div>
            </div>
            <div class="order-badge">#{order_id}</div>
        </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)


def render_section_header(title, icon):
    """Render premium section header"""
    section_html = f"""
    <style>
    .section-header {{
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 12px 0 8px 0;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 12px;
    }}
    
    .section-icon {{
        font-size: 1.2rem;
    }}
    
    .section-title {{
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        font-weight: 600;
        color: #9898b0;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }}
    </style>
    
    <div class="section-header">
        <span class="section-icon">{icon}</span>
        <span class="section-title">{title}</span>
    </div>
    """
    st.markdown(section_html, unsafe_allow_html=True)


def render_field_value(label, value, style_type="normal"):
    """Render a field with premium styling"""
    
    style_configs = {
        "highlight": {
            "bg": "linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(168, 85, 247, 0.15) 100%)",
            "border": "rgba(99, 102, 241, 0.4)",
            "text": "#a5b4fc",
            "font": "'Inter', sans-serif"
        },
        "tracking": {
            "bg": "linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(34, 211, 238, 0.15) 100%)",
            "border": "rgba(16, 185, 129, 0.4)",
            "text": "#6ee7b7",
            "font": "'JetBrains Mono', monospace"
        },
        "status": {
            "bg": "linear-gradient(135deg, rgba(236, 72, 153, 0.15) 0%, rgba(168, 85, 247, 0.15) 100%)",
            "border": "rgba(236, 72, 153, 0.4)",
            "text": "#f9a8d4",
            "font": "'Inter', sans-serif"
        },
        "normal": {
            "bg": "rgba(255, 255, 255, 0.03)",
            "border": "rgba(255, 255, 255, 0.08)",
            "text": "#f4f4f8",
            "font": "'Inter', sans-serif"
        }
    }
    
    config = style_configs.get(style_type, style_configs["normal"])
    
    field_html = f"""
    <style>
    .field-container-{hash(label) % 10000} {{
        margin-bottom: 10px;
    }}
    
    .field-label-{hash(label) % 10000} {{
        font-size: 0.75rem;
        font-weight: 600;
        color: #6b6b82;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }}
    
    .field-value-{hash(label) % 10000} {{
        background: {config["bg"]};
        border: 1px solid {config["border"]};
        border-radius: 10px;
        padding: 10px 14px;
        color: {config["text"]};
        font-family: {config["font"]};
        font-size: 0.95rem;
        font-weight: 500;
        word-break: break-all;
    }}
    </style>
    
    <div class="field-container-{hash(label) % 10000}">
        <div class="field-label-{hash(label) % 10000}">{label}</div>
        <div class="field-value-{hash(label) % 10000}">{value}</div>
    </div>
    """
    st.markdown(field_html, unsafe_allow_html=True)


def render_card_footer():
    """Render card footer/closing"""
    footer_html = """
    <style>
    .card-footer {
        height: 8px;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(168, 85, 247, 0.2) 100%);
        border-radius: 0 0 16px 16px;
        margin-bottom: 16px;
    }
    </style>
    <div class="card-footer"></div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)


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
# 📋 DISPLAY FIELDS CONFIGURATION
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
        {"name": "Pieces", "aliases": ["n.o of pieces", "pieces", "item count", "items", "no of pieces", "no. of pieces"], "style": "normal"},
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
    "📡 Live Status": [
        {"name": "Latest Status", "aliases": ["latest status", "latest_status", "live status", "current status", "status update", "delivery status"], "style": "status"},
    ]
}

# ═══════════════════════════════════════════════════════════════════════════════
# ⚙️ DATA LOADING FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def fetch_single_source(name, config, timeout=120):
    """Fetch a single data source with retry logic"""
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
                return {
                    "name": name,
                    "df": None,
                    "error": str(e)
                }
            time.sleep(1)


def load_all_data():
    """Load all data sources in parallel"""
    results = {}
    errors = []
    
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {
            executor.submit(fetch_single_source, name, config): name 
            for name, config in DATA_SOURCES.items()
        }
        
        for future in as_completed(futures):
            result = future.result()
            name = result["name"]
            
            if result["error"]:
                errors.append(f"{name}: {result['error']}")
            else:
                results[name] = result
    
    return results, errors


def initialize_data():
    """Initialize data loading into session state"""
    if "data_loaded" not in st.session_state:
        st.session_state.data_loaded = False
    
    if not st.session_state.data_loaded:
        with st.spinner("🚀 Initializing TrackMaster Pro..."):
            data, errors = load_all_data()
            st.session_state.all_data = data
            st.session_state.load_errors = errors
            st.session_state.total_rows = sum(
                len(d["df"]) for d in data.values() if d.get("df") is not None
            )
            st.session_state.data_loaded = True


# ═══════════════════════════════════════════════════════════════════════════════
# 🔍 SEARCH FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def parse_order_ids(input_text):
    """Parse multiple order IDs from input"""
    import re
    order_ids = re.split(r'[,\n\t\s]+', input_text.strip())
    return [oid.strip() for oid in order_ids if oid.strip()]


def instant_search(order_ids):
    """Search all loaded data instantly"""
    results = []
    
    for order_id in order_ids:
        search_term = order_id.lower().strip()
        
        for source_name, source_data in st.session_state.all_data.items():
            df = source_data.get("df")
            if df is None:
                continue
            
            matches = df[df["_search_col"] == search_term]
            
            for _, row in matches.iterrows():
                results.append({
                    "source": source_name,
                    "partner": source_data["partner"],
                    "type": source_data["type"],
                    "icon": source_data["icon"],
                    "order_id": order_id,
                    "data": row.to_dict()
                })
    
    return results


def get_field_value(data, aliases):
    """Get field value by checking multiple aliases"""
    data_lower = {k.lower().strip(): v for k, v in data.items()}
    
    for alias in aliases:
        alias_lower = alias.lower().strip()
        if alias_lower in data_lower:
            val = data_lower[alias_lower]
            if is_valid(val):
                return str(val)
    return None


def is_valid(val):
    """Check if value is valid (not empty/NA/None)"""
    if val is None:
        return False
    if pd.isna(val):
        return False
    str_val = str(val).strip().lower()
    if str_val in ["", "nan", "none", "na", "n/a", "-", "null"]:
        return False
    return True


# ═══════════════════════════════════════════════════════════════════════════════
# 🎨 RENDER RESULT CARD
# ═══════════════════════════════════════════════════════════════════════════════

def render_result_card(result):
    """Render a complete result card with premium styling"""
    data = result["data"]
    
    # Render premium header
    render_result_card_header(result)
    
    # Card body container
    body_html = """
    <style>
    .card-body {
        background: linear-gradient(180deg, #16161f 0%, #12121a 100%);
        border: 1px solid #2a2a3d;
        border-top: none;
        padding: 20px 24px;
    }
    </style>
    <div class="card-body">
    """
    st.markdown(body_html, unsafe_allow_html=True)
    
    # Render each section
    for section_name, fields in DISPLAY_FIELDS.items():
        section_values = []
        
        for field in fields:
            value = get_field_value(data, field["aliases"])
            if value:
                section_values.append((field["name"], value, field["style"]))
        
        if section_values:
            icon = section_name.split()[0]
            title = " ".join(section_name.split()[1:])
            render_section_header(title, icon)
            
            cols = st.columns(2)
            for idx, (name, value, style) in enumerate(section_values):
                with cols[idx % 2]:
                    render_field_value(name, value, style)
    
    # Close body and render footer
    st.markdown("</div>", unsafe_allow_html=True)
    render_card_footer()


# ═══════════════════════════════════════════════════════════════════════════════
# 🎯 HOME PAGE
# ═══════════════════════════════════════════════════════════════════════════════

def render_home_page():
    """Render the premium home/search page"""
    render_premium_header()
    
    # Stats row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Total Records", f"{st.session_state.total_rows:,}")
    with col2:
        st.metric("🔗 Data Sources", len(st.session_state.all_data))
    with col3:
        st.metric("⚡ Search Speed", "< 50ms")
    
    st.markdown("---")
    
    # Search section
    search_input = st.text_area(
        "🔍 ENTER ORDER IDs",
        placeholder="Enter order IDs (one per line, or separated by commas)...",
        height=120,
        key="search_input"
    )
    
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        search_btn = st.button("🚀 SEARCH", use_container_width=True)
    with col2:
        if st.button("🔄 REFRESH DATA", use_container_width=True):
            st.session_state.data_loaded = False
            st.rerun()
    
    # Handle search
    if search_btn and search_input.strip():
        order_ids = parse_order_ids(search_input)
        
        if order_ids:
            start_time = time.time()
            results = instant_search(order_ids)
            search_time = (time.time() - start_time) * 1000
            
            st.markdown("---")
            
            if results:
                st.success(f"✨ Found **{len(results)}** result(s) in **{search_time:.1f}ms**")
                
                for result in results:
                    render_result_card(result)
            else:
                st.warning("🔍 No results found for the provided order IDs.")
        else:
            st.warning("⚠️ Please enter at least one order ID.")
    
    # Show load errors if any
    if st.session_state.load_errors:
        with st.expander("⚠️ Data Load Warnings"):
            for error in st.session_state.load_errors:
                st.warning(error)


# ═══════════════════════════════════════════════════════════════════════════════
# 📊 DATA SOURCE PAGE
# ═══════════════════════════════════════════════════════════════════════════════

def render_data_source_page(source_name):
    """Render individual data source page"""
    source_data = st.session_state.all_data.get(source_name)
    
    if not source_data or source_data.get("df") is None:
        st.error(f"❌ Data not available for {source_name}")
        return
    
    df = source_data["df"]
    partner = source_data["partner"]
    theme = get_partner_theme(partner)
    
    # Page header
    header_html = f"""
    <style>
    .source-page-header {{
        background: {theme["gradient"]};
        border-radius: 16px;
        padding: 24px 32px;
        margin-bottom: 24px;
        box-shadow: 0 4px 30px {theme["glow"]};
    }}
    
    .source-title {{
        font-size: 2rem;
        font-weight: 700;
        color: white;
        margin: 0;
    }}
    
    .source-subtitle {{
        color: rgba(255,255,255,0.8);
        font-size: 1rem;
        margin-top: 4px;
    }}
    </style>
    
    <div class="source-page-header">
        <h2 class="source-title">{theme["icon"]} {partner} - {source_data["type"]}</h2>
        <p class="source-subtitle">Data Management & Export</p>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📋 Total Records", f"{len(df):,}")
    with col2:
        st.metric("📊 Columns", len(df.columns))
    with col3:
        st.metric("🔗 Partner", partner)
    
    # Filter
    filter_text = st.text_input("🔍 Filter data...", placeholder="Type to filter...")
    
    if filter_text:
        mask = df.astype(str).apply(lambda x: x.str.contains(filter_text, case=False, na=False)).any(axis=1)
        filtered_df = df[mask]
    else:
        filtered_df = df
    
    # Display DataFrame
    display_df = filtered_df.drop(columns=["_search_col"], errors="ignore")
    st.dataframe(display_df, use_container_width=True, height=500)
    
    # Download button
    csv = display_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"{partner}_{source_data['type']}_export.csv",
        mime="text/csv",
        use_container_width=True
    )


# ═══════════════════════════════════════════════════════════════════════════════
# 🚀 MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    # Initialize data
    initialize_data()
    
    # Sidebar
    with st.sidebar:
        render_mini_header()
        
        st.markdown("---")
        
        nav_options = ["🏠 Global Search"] + list(DATA_SOURCES.keys())
        selected = st.radio(
            "NAVIGATION",
            nav_options,
            label_visibility="collapsed"
        )
    
    # Main content
    if selected == "🏠 Global Search":
        render_home_page()
    else:
        render_data_source_page(selected)


if __name__ == "__main__":
    main()
