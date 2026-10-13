import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
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

# Custom Styling
st.markdown("""
    <style>
    .stApp {
        background: #F1F5F9;
        color: #0F172A;
    }
    .glow-header-title {
        font-size: 44px !important;
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
        font-size: 20px;
        font-weight: 600;
        margin-bottom: 20px;
        text-align: center !important;
    }
    div[data-testid="stMetric"] {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 14px !important;
        padding: 16px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        border-color: #0284C7 !important;
        box-shadow: 0 0 20px rgba(2, 132, 199, 0.25) !important;
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
    .sec-card-scms {
        background: #FFFFFF;
        padding: 16px;
        border-radius: 12px;
        border-left: 6px solid #E11D48;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
        margin-bottom: 18px;
    }
    .sec-card-lgu {
        background: #FFFFFF;
        padding: 16px;
        border-radius: 12px;
        border-left: 6px solid #16A34A;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
        margin-bottom: 18px;
    }
    .sec-title-scms { color: #E11D48; font-size: 20px; font-weight: 800; }
    .sec-title-lgu { color: #16A34A; font-size: 20px; font-weight: 800; }
    
    section[data-testid="stSidebar"] {
        background-color: #0F172A !important;
        color: #FFFFFF !important;
    }
    section[data-testid="stSidebar"] * {
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
        
        1. **Official Use Only:** Data presented in this portal consists of consolidated executive analytics, program targets, and operational metrics.
        2. **Confidentiality Notice:** Unlawful reproduction, redistribution, or unauthorized sharing of these metrics is strictly prohibited.
        3. **Security Standards:** All system interactions and access sessions are logged for audit compliance.
        """)
        st.divider()
        if st.button("✅ I Agree & Proceed to Executive Portal", use_container_width=True):
            st.session_state["privacy_accepted"] = True
            st.rerun()

    if not st.session_state["privacy_accepted"]:
        privacy_modal()

# ---------------------------------------------------------
# LOGO LOADERS & CONFIGURATION
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

# Live Google Sheet Link for AppSheet / Client Tab
SCMS_SHEET_HTML = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSiS3wDEdJUU6Xh8jL66xpLMz8RoDnv-Z32rcF6TeCHg_UKwAutb6_VbMyViNeMi7R9SyiEm-5bU9S_/pubhtml"
SCMS_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSiS3wDEdJUU6Xh8jL66xpLMz8RoDnv-Z32rcF6TeCHg_UKwAutb6_VbMyViNeMi7R9SyiEm-5bU9S_/pub?gid=0&single=true&output=csv"

def export_to_excel_bytes(df):
    output = BytesIO()
    try:
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Executive_Data')
    except Exception:
        output.write(df.to_csv(index=False).encode('utf-8'))
    return output.getvalue()

# ---------------------------------------------------------
# SUPABASE DATABASE CONNECTION & GOOGLE SHEET LIVE LOADER
# ---------------------------------------------------------
DEFAULT_DB_URL = "postgresql+psycopg2://postgres.oxyvjstdncnnefbkilaa:5GLJZg5tWE28Wud9@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"

@st.cache_resource
def get_db_engine():
    try:
        db_url = st.secrets.get("SUPABASE_URL", DEFAULT_DB_URL)
    except Exception:
        db_url = DEFAULT_DB_URL
    return create_engine(db_url, pool_pre_ping=True)

engine = get_db_engine()

# Load Live AppSheet Client Data directly from published CSV feed
@st.cache_data(ttl=180)
def load_live_appsheet_client_data():
    try:
        df = pd.read_csv(SCMS_CSV_URL)
        return df
    except Exception:
        return pd.DataFrame()

# Load Database Summary
@st.cache_data(ttl=180)
def load_db_cases_summary():
    try:
        df_db = pd.read_sql_query(text("SELECT * FROM cases"), engine)
        return df_db
    except Exception:
        return pd.DataFrame()

df_live_clients = load_live_appsheet_client_data()
df_db_cases = load_db_cases_summary()

# ---------------------------------------------------------
# HEADER & SIDEBAR NAVIGATION
# ---------------------------------------------------------
hdr_col1, hdr_col2 = st.columns([4, 1])
with hdr_col1:
    st.markdown('<div class="glow-header-title">🕊️ PDBBM EXECUTIVE COMPREHENSIVE DASHBOARD</div>', unsafe_allow_html=True)
    st.markdown('<div class="glow-header-sub">Integrated Multi-Program Decision Support & Live Analytics</div>', unsafe_allow_html=True)
with hdr_col2:
    if main_header_logo:
        st.image(main_header_logo, width=250)

st.sidebar.title("📌 Navigation Portal")

if sidebar_logo:
    st.sidebar.markdown('<div class="sidebar-logo-container">', unsafe_allow_html=True)
    st.sidebar.image(sidebar_logo, use_container_width=True)
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

program_view = st.sidebar.radio(
    "Select Portal View:",
    [
        "🌐 Consolidated Executive Overview",
        "📦 1. SCMS Live Client Entry (Google Sheet / AppSheet)",
        "📊 2. Master Database Analytics"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔗 Direct Sheet Access")
st.sidebar.markdown(f"👉 [**Open Google Sheet / AppSheet Tab**]({SCMS_SHEET_HTML})")

st.sidebar.markdown("---")
st.sidebar.info("🔒 **Data Privacy Active:** Beneficiary personal identity details are protected under RA 10173.")

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
    
    # 1. Calculate Metrics from Live AppSheet Client Data & DB
    tot_actual_appsheet = len(df_live_clients) if not df_live_clients.empty else 0
    tot_db_cases = len(df_db_cases) if not df_db_cases.empty else 0
    
    # Find Sex Column in Live AppSheet
    male_count = 0
    female_count = 0
    sex_col = [c for c in df_live_clients.columns if 'sex' in c.lower() or 'gender' in c.lower()] if not df_live_clients.empty else []
    
    if sex_col:
        col_name = sex_col[0]
        male_count = len(df_live_clients[df_live_clients[col_name].astype(str).str.lower() == 'male'])
        female_count = len(df_live_clients[df_live_clients[col_name].astype(str).str.lower() == 'female'])
    elif not df_db_cases.empty and 'sex' in df_db_cases.columns:
        male_count = len(df_db_cases[df_db_cases['sex'].astype(str).str.lower() == 'male'])
        female_count = len(df_db_cases[df_db_cases['sex'].astype(str).str.lower() == 'female'])

    # Profile Completion Status
    completed_cnt = 0
    incomplete_cnt = 0
    if not df_db_cases.empty and 'profile_status' in df_db_cases.columns:
        completed_cnt = len(df_db_cases[df_db_cases['profile_status'].astype(str).str.lower() == 'completed'])
        incomplete_cnt = tot_db_cases - completed_cnt

    st.markdown('<div class="sec-card-scms"><span class="sec-title-scms">📦 SCMS Live "Client" Tab vs Database Analytics</span></div>', unsafe_allow_html=True)

    m1, m2, m3, m4, m5, m6 = st.columns(6)
    m1.metric("Live AppSheet Clients", f"{tot_actual_appsheet:,}")
    m2.metric("Master DB Total", f"{tot_db_cases:,}")
    m3.metric("👨 Male Clients", f"{male_count:,}")
    m4.metric("👩 Female Clients", f"{female_count:,}")
    m5.metric("🟢 Completed Profiles", f"{completed_cnt:,}")
    m6.metric("🟡 Incomplete / Drafts", f"{incomplete_cnt:,}")

    st.markdown("<br>", unsafe_allow_html=True)
    g1, g2, g3 = st.columns(3)
    
    with g1:
        st.subheader("👥 Total Client Male vs Female Breakdown")
        gender_df = pd.DataFrame({
            'Gender': ['Male', 'Female'],
            'Total Clients': [male_count, female_count]
        })
        fig_gender = px.pie(
            gender_df, names='Gender', values='Total Clients', 
            color='Gender', color_discrete_map={'Male': '#0284C7', 'Female': '#E11D48'}, 
            template=plotly_template, hole=0.4
        )
        fig_gender.update_layout(margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_gender, use_container_width=True)

    with g2:
        st.subheader("📍 Beneficiaries Distribution per Province")
        prov_col = [c for c in df_live_clients.columns if 'province' in c.lower()] if not df_live_clients.empty else []
        if prov_col:
            prov_df = df_live_clients[prov_col[0]].value_counts().reset_index()
            prov_df.columns = ['Province', 'Total Encoded']
            fig_prov = px.bar(prov_df, x='Province', y='Total Encoded', color='Province', text_auto=',.0f', template=plotly_template)
            fig_prov.update_layout(margin=dict(t=20, b=20, l=20, r=20), showlegend=False)
            st.plotly_chart(fig_prov, use_container_width=True)
        elif not df_db_cases.empty and 'province' in df_db_cases.columns:
            prov_df = df_db_cases['province'].value_counts().reset_index()
            prov_df.columns = ['Province', 'Total Encoded']
            fig_prov = px.bar(prov_df, x='Province', y='Total Encoded', color='Province', text_auto=',.0f', template=plotly_template)
            fig_prov.update_layout(margin=dict(t=20, b=20, l=20, r=20), showlegend=False)
            st.plotly_chart(fig_prov, use_container_width=True)
        else:
            st.info("No Province data detected in feed.")

    with g3:
        st.subheader("📌 Profile Status Breakdown")
        status_df = pd.DataFrame({
            'Status': ['Completed', 'Incomplete / Draft'],
            'Count': [completed_cnt, incomplete_cnt]
        })
        fig_status = px.bar(status_df, x='Status', y='Count', color='Status', color_discrete_map={'Completed': '#16A34A', 'Incomplete / Draft': '#EAB308'}, text_auto=',.0f', template=plotly_template)
        fig_status.update_layout(margin=dict(t=20, b=20, l=20, r=20), showlegend=False)
        st.plotly_chart(fig_status, use_container_width=True)

    st.divider()

    # AppSheet Live Records Data Table Preview
    st.subheader("📋 Live AppSheet 'Client' Google Sheet Raw Data Preview")
    if not df_live_clients.empty:
        st.dataframe(df_live_clients.head(50), use_container_width=True)
        
        excel_bytes = export_to_excel_bytes(df_live_clients)
        st.download_button(
            label="📥 Download Live AppSheet Client Report (.xlsx)",
            data=excel_bytes,
            file_name="AppSheet_Live_Client_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    else:
        st.info("Unable to fetch live AppSheet data. Displaying database fallback.")

# ---------------------------------------------------------
# INDIVIDUAL MODULE VIEWS
# ---------------------------------------------------------
elif program_view == "📦 1. SCMS Live Client Entry (Google Sheet / AppSheet)":
    st.markdown('<div class="glow-header-title">📦 SCMS Live Google Sheet "Client" View</div>', unsafe_allow_html=True)
    st.markdown('<div class="privacy-banner">🔒 <b>Live Google Sheets Embed:</b> Direct real-time updates from field encoders.</div>', unsafe_allow_html=True)

    st.components.v1.iframe(SCMS_SHEET_HTML, height=750, scrolling=True)

else:
    st.markdown('<div class="glow-header-title">📊 Master Database Registered Cases</div>', unsafe_allow_html=True)
    if not df_db_cases.empty:
        st.dataframe(df_db_cases, use_container_width=True)
    else:
        st.info("No master database records found.")

# DEVELOPER FOOTER BADGE
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; font-size: 0.85em; color: #64748B; padding-bottom: 20px;">
        ⚙️ <b>PDBBM Executive Decision Support Portal</b> | Powered by Streamlit & Python<br>
        Designed & Developed by <b>LOUIE B. IDULSA - PDBBM ITO I</b> • DSWD Field Office X
    </div>
    """, 
    unsafe_allow_html=True
)
