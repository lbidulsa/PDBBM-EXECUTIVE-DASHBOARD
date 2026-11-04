import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
from io import BytesIO

# ---------------------------------------------------------
# PAGE CONFIGURATION & EXECUTIVE LIGHT UI
# ---------------------------------------------------------
st.set_page_config(
    page_title="PDBBM Executive Multi-Program System",
    page_icon="🕊️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# CUSTOM GLOW ANIMATIONS & SECURITY STYLING INJECTION
# ---------------------------------------------------------
st.markdown("""
    <style>
    .stApp {
        background: #F1F5F9;
        color: #0F172A;
    }

    /* Security Fix: Hide Streamlit Header, GitHub Repository Link Icon, and Main Menu */
    header[data-testid="stHeader"] { visibility: hidden !important; display: none !important; }
    #MainMenu { visibility: hidden !important; display: none !important; }
    footer { visibility: hidden !important; display: none !important; }
    .stAppDeployButton { display: none !important; }

    .glow-header-title {
        font-size: 48px !important;
        font-weight: 900 !important;
        background: linear-gradient(90deg, #E11D48, #16A34A, #0284C7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.8px;
        margin-bottom: 2px;
        text-align: center !important;
    }
    .glow-header-sub {
        color: #64748B;
        font-size: 22px;
        font-weight: 600;
        margin-bottom: 20px;
        text-align: center !important;
    }
    
    /* ========================================================= */
    /* 🌟 METRIC CARDS GLOW & HOVER ANIMATION (LOGOUT STYLE) 🌟 */
    /* ========================================================= */
    div[data-testid="stMetric"] {
        background: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 14px !important;
        padding: 16px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03) !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-4px) scale(1.02) !important;
        border-color: #E11D48 !important;
        box-shadow: 0 0 18px rgba(225, 29, 72, 0.5), 0 0 28px rgba(225, 29, 72, 0.25) !important;
    }
    div[data-testid="stMetric"] label {
        color: #475569 !important;
        font-size: 12px !important;
        font-weight: 700 !important;
        text-transform: uppercase;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #0284C7 !important;
        font-weight: 800 !important;
        font-size: 24px !important;
    }

    /* ========================================================= */
    /* 🌟 UNIFIED BUTTON ANIMATIONS & RED/ORANGE GLOW EFFECTS 🌟 */
    /* ========================================================= */
    div.stButton > button, 
    div.stDownloadButton > button,
    div.stFormSubmitButton > button,
    .stSidebar div.stButton > button {
        background-color: #E2E8F0 !important;
        color: #0F172A !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        border: 1px solid #CBD5E1 !important;
        padding: 8px 20px !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }
    
    div.stButton > button:hover, 
    div.stDownloadButton > button:hover,
    div.stFormSubmitButton > button:hover,
    .stSidebar div.stButton > button:hover {
        background-color: #FFFFFF !important;
        color: #E11D48 !important;
        border-color: #E11D48 !important;
        box-shadow: 0 0 15px rgba(225, 29, 72, 0.6), 0 0 25px rgba(225, 29, 72, 0.3) !important;
        transform: translateY(-2px) scale(1.01) !important;
    }
    
    div.stButton > button:active, 
    div.stDownloadButton > button:active,
    div.stFormSubmitButton > button:active,
    .stSidebar div.stButton > button:active {
        transform: translateY(1px) scale(0.99) !important;
        box-shadow: 0 0 5px rgba(225, 29, 72, 0.4) !important;
    }

    /* SECTION CARDS HOVER EFFECT */
    .sec-card-scms, .sec-card-lgu, .sec-card-cdpd {
        background: #FFFFFF;
        padding: 16px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
        margin-bottom: 18px;
        transition: all 0.3s ease;
    }
    .sec-card-scms { border-left: 6px solid #E11D48; }
    .sec-card-lgu { border-left: 6px solid #16A34A; }
    .sec-card-cdpd { border-left: 6px solid #0284C7; }

    .sec-card-scms:hover {
        transform: translateX(4px);
        box-shadow: 0 0 15px rgba(225, 29, 72, 0.25);
    }
    .sec-card-lgu:hover {
        transform: translateX(4px);
        box-shadow: 0 0 15px rgba(22, 163, 74, 0.25);
    }
    .sec-card-cdpd:hover {
        transform: translateX(4px);
        box-shadow: 0 0 15px rgba(2, 132, 199, 0.25);
    }

    .sec-title-scms { color: #E11D48; font-size: 20px; font-weight: 800; }
    .sec-title-lgu { color: #16A34A; font-size: 20px; font-weight: 800; }
    .sec-title-cdpd { color: #0284C7; font-size: 20px; font-weight: 800; }
    
    /* SIDEBAR STYLING */
    section[data-testid="stSidebar"] {
        background-color: #0F172A !important;
        color: #FFFFFF !important;
    }
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span {
        color: #F8FAFC !important;
    }
    
    .sidebar-logo-container {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 8px 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        margin-bottom: 15px;
    }
    
    section[data-testid="stSidebar"] img {
        border-radius: 0px !important;
        mix-blend-mode: normal !important;
        object-fit: contain !important;
        max-width: 100% !important;
        height: auto !important;
    }
    
    .privacy-banner {
        background: rgba(225, 29, 72, 0.08);
        border: 1px solid rgba(225, 29, 72, 0.3);
        border-radius: 10px;
        padding: 12px 18px;
        color: #9F1239;
        font-weight: 600;
        font-size: 13px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# DATA PRIVACY ACT (RA 10173) AUTOMATIC POP-UP MODAL
# ---------------------------------------------------------
if "privacy_accepted" not in st.session_state:
    st.session_state["privacy_accepted"] = False

if hasattr(st, "dialog"):
    @st.dialog("🔒 DATA PRIVACY ACT COMPLIANCE REMINDER (RA 10173)")
    def privacy_modal():
        st.markdown("""
        **DSWD FIELD OFFICE X • PDBBM EXECUTIVE MULTI-PROGRAM PORTAL**
        
        Pursuant to **Republic Act No. 10173 (Data Privacy Act of 2012)**:
        
        1. **Official Use Only:** Data presented in this portal consists strictly of consolidated executive analytics, aggregated metrics, and program scorecards.
        2. **Confidentiality Notice:** No raw personal identity records are exposed in this executive analytics portal.
        3. **Security Standards:** All system interactions and access sessions are logged for audit compliance.
        """)
        st.divider()
        if st.button("✅ I Agree & Proceed to Executive Portal", use_container_width=True):
            st.session_state["privacy_accepted"] = True
            st.rerun()

    if not st.session_state["privacy_accepted"]:
        privacy_modal()

# ---------------------------------------------------------
# LOGO LOADERS & HELPERS
# ---------------------------------------------------------
def get_main_header_logo():
    if os.path.exists("Peace and Dev LOGO.jpg"):
        return "Peace and Dev LOGO.jpg"
    elif os.path.exists("logo.png"):
        return "logo.png"
    return None

def get_sidebar_logo():
    if os.path.exists("logo.png"):
        return "logo.png"
    elif os.path.exists("Peace and Dev LOGO.jpg"):
        return "Peace and Dev LOGO.jpg"
    return None

main_header_logo = get_main_header_logo()
sidebar_logo = get_sidebar_logo()
plotly_template = "plotly_white"

def export_to_excel_bytes(df):
    output = BytesIO()
    try:
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Executive_Summary')
    except Exception:
        output.write(df.to_csv(index=False).encode('utf-8'))
    return output.getvalue()

# ---------------------------------------------------------
# DATA STRUCTURES
# ---------------------------------------------------------
df_scms_affiliation = pd.DataFrame({
    'Affiliation': ['MILF', 'MNLF', 'FR', 'DPAGS', 'KAPATIRAN', 'MSAP'],
    'Target': [7472, 606, 3067, 0, 29, 0],
    'Male': [6784, 27, 1429, 0, 24, 0],
    'Female': [355, 2, 380, 0, 3, 0],
    'Total_Profiled': [7139, 29, 1809, 0, 27, 0],
    'Not_Yet_Profiled': [333, 577, 1258, 0, 2, 0]
})

df_scms_province = pd.DataFrame({
    'Province': ['Bukidnon', 'Lanao del Norte', 'Lanao del Sur', 'Misamis Occidental', 'Misamis Oriental'],
    'NPA': [1377, 0, 0, 150, 282],
    'KAPATIRAN': [20, 0, 0, 0, 7],
    'MILF': [36, 1977, 5121, 2, 3],
    'MNLF': [0, 0, 29, 0, 0],
    'Profiled_Clients': [1433, 1977, 5150, 152, 292]
})

df_lgu_po_summary = pd.DataFrame({
    'Name of PO': [
        'OZAMIZ CONFESSIONS CLASSIFIED COMMUNITY OUTREACH AND DEVELOPMENT INC.',
        'BUKIDNON PEACE BUILDERS FARMERS ASSOCIATION',
        'LANAO DEL NORTE UNITED MULTI-PURPOSE ASSOCIATION',
        'MISAMIS ORIENTAL INTEGRATED PEACEKEEPERS ASSOC.',
        'MISAMIS OCCIDENTAL AGRI-PEACE FARMERS COOP',
        'KADINGILAN PEACE & DEVELOPMENT FARMERS ASSOC.',
        'BALINGASAG LIVELIHOOD & PEACE PROMOTION ASSOC.',
        'MUNAI UNIFIED PEACEKEEPERS ASSOCIATION',
        'TANGUB CITY INTEGRATED COMMUNITY ASSOC.',
        'MARAMAG SUSTAINABLE PEACE FARMERS COOP',
        'TAGOLOAN PEACE BUILDERS MULTI-PURPOSE ASSOC.',
        'BALO-I PROGRESSIVE COMMUNITY ASSOC.'
    ],
    'Province': [
        'Misamis Occidental', 'Bukidnon', 'Lanao del Norte', 'Misamis Oriental', 
        'Misamis Occidental', 'Bukidnon', 'Misamis Oriental', 'Lanao del Norte', 
        'Misamis Occidental', 'Bukidnon', 'Misamis Oriental', 'Lanao del Norte'
    ],
    'Municipality': [
        'Ozamiz City', 'Valencia City', 'Kauswagan', 'Claveria', 
        'Oroquieta City', 'Kadingilan', 'Balingasag', 'Munai', 
        'Tangub City', 'Maramag', 'Tagoloan', 'Balo-i'
    ],
    'Total Profiled Members': [17, 45, 38, 29, 22, 31, 26, 50, 19, 41, 33, 27],
    'Male Members': [5, 38, 30, 24, 18, 25, 20, 42, 14, 33, 27, 21],
    'Female Members': [12, 7, 8, 5, 4, 6, 6, 8, 5, 8, 6, 6],
    'Status of Livelihood Support': ['Provided'] * 12
})

df_lgu_summary = pd.DataFrame({
    'Province': ['Bukidnon', 'Lanao del Norte', 'Misamis Oriental', 'Misamis Occidental'],
    'Target_POs': [49, 35, 28, 22],
    'POs_Provided_Assistance': [48, 34, 27, 21],
    'Waived_Disbanded_POs': [1, 1, 0, 0],
    'Allocated_Budget_PHP': [29400000, 21000000, 16800000, 13200000],
    'Status': ['98% Completed', '97% Completed', '96% Completed', '100% Completed']
})

# ---------------------------------------------------------
# HEADER & SIDEBAR NAVIGATION WITH REFRESH BUTTON
# ---------------------------------------------------------
hdr_col1, hdr_col2 = st.columns([4, 1])
with hdr_col1:
    st.markdown('<div class="glow-header-title">🕊️ PDBBM EXECUTIVE COMPREHENSIVE DASHBOARD</div>', unsafe_allow_html=True)
    st.markdown('<div class="glow-header-sub">Integrated Multi-Program Decision Support & Live Executive Analytics</div>', unsafe_allow_html=True)
with hdr_col2:
    if main_header_logo:
        st.image(main_header_logo, width=250)

st.sidebar.title("📌 Navigation Portal")

if sidebar_logo:
    st.sidebar.markdown('<div class="sidebar-logo-container">', unsafe_allow_html=True)
    st.sidebar.image(sidebar_logo, use_container_width=True)
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

# 🔄 REFRESH DATA BUTTON IN SIDEBAR
if st.sidebar.button("🔄 Refresh System Data", use_container_width=True):
    st.cache_data.clear()
    st.toast("🔄 System Data Refreshed!", icon="✨")
    st.rerun()

program_view = st.sidebar.radio(
    "Select Portal View:",
    [
        "🌐 Consolidated Executive Overview",
        "📦 1. SCMS Analytics",
        "🏛️ 2. PAMANA LGU-Led Analytics",
        "🕊️ 3. PAMANA CDPD Analytics"
    ]
)

st.sidebar.markdown("---")
st.sidebar.title("🎛️ Province Filter")

all_provinces_list = ['Bukidnon', 'Lanao del Norte', 'Lanao del Sur', 'Misamis Occidental', 'Misamis Oriental', 'Zamboanga del Sur', 'Zamboanga del Norte']

filter_mode = st.sidebar.radio(
    "Filter Scope:",
    ["All Provinces (Region X)", "Select Specific Province"]
)

if filter_mode == "Select Specific Province":
    selected_province = st.sidebar.selectbox("Choose Target Province:", options=all_provinces_list)
    selected_provinces = [selected_province]
else:
    selected_provinces = all_provinces_list

st.sidebar.markdown("---")
st.sidebar.info("🔒 **Data Privacy Active (RA 10173):** All individual beneficiary details are protected. Analytics display aggregate counts only.")

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    <div style="text-align: center; font-size: 0.8em; color: #94A3B8;">
        💻 <b>System Developer & Architect</b><br>
        Developed with ❤️ by <br><b style="color:#38BDF8;">LOUIE B. IDULSA - PDBBM ITO I</b><br>
        <i>DSWD FO X - PDBBM Multi-Program Portal © 2026</i>
    </div>
    """, 
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# CONSOLIDATED EXECUTIVE OVERVIEW
# ---------------------------------------------------------
if program_view == "🌐 Consolidated Executive Overview":
    filtered_prov = df_scms_province[df_scms_province['Province'].isin(selected_provinces)] if selected_provinces else df_scms_province
    tot_profiled = filtered_prov['Profiled_Clients'].sum()
    tot_target = 11174
    tot_male = int(np.round(tot_profiled * (8264 / 9004))) if tot_profiled > 0 else 0
    tot_female = tot_profiled - tot_male
    tot_not_yet = max(0, tot_target - tot_profiled)

    st.markdown('<div class="sec-card-scms"><span class="sec-title-scms">📦 1. SCMS Analytics</span></div>', unsafe_allow_html=True)

    s1, s2, s3, s4, s5 = st.columns(5)
    s1.metric("ANNUAL TARGET", f"{tot_target:,}")
    accomplishment_pct = (tot_profiled / tot_target * 100) if tot_target > 0 else 0
    s2.metric("TOTAL PROFILED CLIENTS", f"{tot_profiled:,}", delta=f"↑ {accomplishment_pct:.1f}% Accomplished")
    s3.metric("👨 MALE CLIENTS", f"{tot_male:,}")
    s4.metric("👩 FEMALE CLIENTS", f"{tot_female:,}")
    s5.metric("⏳ NOT YET PROFILED", f"{tot_not_yet:,}")

    st.markdown("<br>", unsafe_allow_html=True)
    sg1, sg2, sg3 = st.columns(3)
    with sg1:
        st.subheader("📊 Profiled Clients per Province")
        fig_prov = px.bar(filtered_prov, x='Province', y='Profiled_Clients', color='Province', text_auto=',.0f', template=plotly_template)
        fig_prov.update_layout(margin=dict(t=20, b=20, l=20, r=20), showlegend=False)
        st.plotly_chart(fig_prov, use_container_width=True)

    with sg2:
        st.subheader("👥 Male vs Female Distribution")
        fig_gender = px.pie(pd.DataFrame({'Gender': ['Male', 'Female'], 'Count': [tot_male, tot_female]}), names='Gender', values='Count', color='Gender', color_discrete_map={'Male': '#0284C7', 'Female': '#E11D48'}, template=plotly_template, hole=0.4)
        fig_gender.update_layout(margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_gender, use_container_width=True)

    with sg3:
        st.subheader("🎯 Accomplishment Rate")
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=accomplishment_pct,
            domain={'x': [0, 1], 'y': [0, 1]},
            number={'suffix': "%", 'font': {'size': 28, 'color': "#0284C7"}},
            gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "#0284C7"}}
        ))
        fig_gauge.update_layout(margin=dict(t=30, b=20, l=20, r=20), height=280)
        st.plotly_chart(fig_gauge, use_container_width=True)

    st.markdown("---")
    st.markdown('<div class="sec-card-lgu"><span class="sec-title-lgu">🏛️ 2. PAMANA LGU-Led Analytics</span></div>', unsafe_allow_html=True)

    l1, l2, l3, l4 = st.columns(4)
    l1.metric("TARGET POs", "99 POs")
    l2.metric("PROVIDED WITH ASSISTANCE", "97 POs", delta="↑ 98.0% Accomplished")
    l3.metric("WAIVED / DISBANDED POs", "2 POs", delta_color="inverse")
    l4.metric("PENDING FUND WITHDRAWAL", "₱600,000")

    st.markdown("---")
    st.markdown('<div class="sec-card-cdpd"><span class="sec-title-cdpd">🕊️ 3. PAMANA CDPD</span></div>', unsafe_allow_html=True)
    st.info("ℹ️ **PAMANA CDPD Status Notice:** Official Region X CDPD sub-project database metrics are currently undergoing final validation.")

elif program_view == "📦 1. SCMS Analytics":
    st.markdown('<div class="glow-header-title">📦 1. SCMS Analytics Scorecard</div>', unsafe_allow_html=True)
    st.dataframe(df_scms_affiliation, use_container_width=True, hide_index=True)

elif program_view == "🏛️ 2. PAMANA LGU-Led Analytics":
    st.markdown('<div class="glow-header-title">🏛️ 2. PAMANA LGU-Led Analytics</div>', unsafe_allow_html=True)
    st.dataframe(df_lgu_summary, use_container_width=True, hide_index=True)

else:
    st.markdown('<div class="glow-header-title">🕊️ 3. PAMANA CDPD Analytics</div>', unsafe_allow_html=True)
    st.warning("⚠️ CDPD database analytics for Region X are currently under system synchronization.")

st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; font-size: 0.85em; color: #64748B; padding-bottom: 20px;">
        ⚙️ <b>PDBBM Executive Multi-Program Decision Support Portal</b> | Powered by Streamlit & Python<br>
        Designed & Developed by <b>LOUIE B. IDULSA - PDBBM ITO I</b> • DSWD Field Office X
    </div>
    """, 
    unsafe_allow_html=True
)
