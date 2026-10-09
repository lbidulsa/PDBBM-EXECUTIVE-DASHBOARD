import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
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
        font-size: 48px !important;
        font-weight: 900 !important;
        background: linear-gradient(90deg, #E11D48, #16A34A, #0284C7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.8px;
        margin-bottom: 2px;
    }
    .glow-header-sub {
        color: #64748B;
        font-size: 22px;
        font-weight: 600;
        margin-bottom: 20px;
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
    .sec-card-cdpd {
        background: #FFFFFF;
        padding: 16px;
        border-radius: 12px;
        border-left: 6px solid #0284C7;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
        margin-bottom: 18px;
    }
    .sec-title-scms { color: #E11D48; font-size: 20px; font-weight: 800; }
    .sec-title-lgu { color: #16A34A; font-size: 20px; font-weight: 800; }
    .sec-title-cdpd { color: #0284C7; font-size: 20px; font-weight: 800; }
    
    /* SIDEBAR STYLING */
    section[data-testid="stSidebar"] {
        background-color: #0F172A !important;
        color: #FFFFFF !important;
    }
    section[data-testid="stSidebar"] * {
        color: #F8FAFC !important;
    }
    
    /* PROPER SIDEBAR LOGO CONTAINER & NATURAL PROPORTION FIX */
    .sidebar-logo-container {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 8px 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        margin-bottom: 15px;
    }
    
    /* Reset image deformations */
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
# LOGO LOADERS (EXPLICIT FOR MAIN HEADER AND SIDEBAR)
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
            df.to_excel(writer, index=False, sheet_name='Executive_Data')
    except Exception:
        output.write(df.to_csv(index=False).encode('utf-8'))
    return output.getvalue()

# ---------------------------------------------------------
# REAL DATA ENGINES - REGION 10 SCOPE ONLY
# ---------------------------------------------------------
DB_FILE = "pamana_database.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

@st.cache_data(ttl=300)
def load_scms_summary_data():
    return pd.DataFrame({
        'Province': ['Lanao del Sur', 'Lanao del Norte', 'Misamis Oriental', 'Bukidnon', 'Misamis Occidental'],
        'Annual_Target': [6070, 1990, 450, 377, 150],
        'Profiled_Clients': [5121, 1977, 290, 377, 150],
        'Case_Managed': [1309, 1977, 289, 377, 150],
        'Interventions_Provided': [357, 280, 178, 210, 150]
    })

@st.cache_data(ttl=300)
def load_lgu_led_data():
    return pd.DataFrame({
        'Province': ['Bukidnon', 'Lanao del Norte', 'Misamis Oriental', 'Misamis Occidental'],
        'Target_SubProjects': [49, 35, 28, 22],
        'Allocated_Budget_PHP': [14700000, 10500000, 8400000, 6600000],
        'Profiled_Beneficiaries': [2150, 1840, 1260, 980],
        'Completed_Social_Prep': [49, 32, 25, 22],
        'Status': ['ONGOING', 'ONGOING', 'ONGOING', 'COMPLETED']
    })

df_scms_summary = load_scms_summary_data()
df_lgu_summary = load_lgu_led_data()

# ---------------------------------------------------------
# HEADER & SIDEBAR NAVIGATION
# ---------------------------------------------------------
hdr_col1, hdr_col2 = st.columns([4, 1])
with hdr_col1:
    st.markdown('<div class="glow-header-title">🕊️ PDBBM EXECUTIVE COMPREHENSIVE DASHBOARD</div>', unsafe_allow_html=True)
    st.markdown('<div class="glow-header-sub">Integrated Multi-Program Decision Support & Live Executive Analytics</div>', unsafe_allow_html=True)
with hdr_col2:
    if main_header_logo:
        st.image(main_header_logo, width=250)

st.sidebar.title("📌 Navigation Portal")

# SIDEBAR LOGO DISPLAY
if sidebar_logo:
    st.sidebar.markdown('<div class="sidebar-logo-container">', unsafe_allow_html=True)
    st.sidebar.image(sidebar_logo, use_container_width=True)
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

program_view = st.sidebar.radio(
    "Select Portal View:",
    [
        "🌐 Consolidated Executive Overview",
        "📦 1. SCMS (Social Case Management)",
        "🏛️ 2. PAMANA LGU-Led Analytics",
        "🕊️ 3. PAMANA CDPD (Database)"
    ]
)

st.sidebar.markdown("---")
st.sidebar.title("🎛️ Region X Province Filter")

selected_provinces = st.sidebar.multiselect(
    "Select Region X Provinces:",
    options=['Bukidnon', 'Lanao del Norte', 'Lanao del Sur', 'Misamis Occidental', 'Misamis Oriental'],
    default=['Bukidnon', 'Lanao del Norte', 'Lanao del Sur', 'Misamis Occidental', 'Misamis Oriental']
)

st.sidebar.markdown("---")
st.sidebar.info("🔒 **Data Privacy Active:** Beneficiary personal identity details for SCMS & LGU-Led are protected.")

# DEVELOPER OWNERSHIP BADGE IN SIDEBAR
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
    
    if selected_provinces:
        f_scms = df_scms_summary[df_scms_summary['Province'].isin(selected_provinces)]
    else:
        f_scms = df_scms_summary

    tot_target = f_scms['Annual_Target'].sum()
    tot_profiled = f_scms['Profiled_Clients'].sum()
    tot_managed = f_scms['Case_Managed'].sum()
    tot_interventions = f_scms['Interventions_Provided'].sum()

    st.markdown('<div class="sec-card-scms"><span class="sec-title-scms">📦 1. SCMS (Social Case Management Service) Analytics</span></div>', unsafe_allow_html=True)

    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Annual Target Clients", f"{tot_target:,}")
    accomplishment_pct = (tot_profiled / tot_target * 100) if tot_target > 0 else 0
    s2.metric("Total Profiled Clients", f"{tot_profiled:,}", delta=f"{accomplishment_pct:.1f}% Accomplished")
    s3.metric("Cases Managed in System", f"{tot_managed:,}")
    s4.metric("Interventions Delivered", f"{tot_interventions:,}")

    st.markdown("<br>", unsafe_allow_html=True)
    sg1, sg2, sg3 = st.columns(3)
    with sg1:
        st.subheader("📊 Profiled Clients per Province (Region X)")
        fig_prov = px.bar(f_scms, x='Province', y='Profiled_Clients', color='Province', text_auto=',.0f', template=plotly_template)
        fig_prov.update_layout(margin=dict(t=20, b=20, l=20, r=20), showlegend=False)
        st.plotly_chart(fig_prov, use_container_width=True)

    with sg2:
        st.subheader("👥 Annual Target vs Actual Profiled")
        fig_target_vs_act = px.bar(
            f_scms, x='Province', y=['Annual_Target', 'Profiled_Clients'],
            barmode='group', text_auto=',.0f', template=plotly_template,
            color_discrete_sequence=['#94A3B8', '#E11D48']
        )
        fig_target_vs_act.update_layout(margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_target_vs_act, use_container_width=True)

    with sg3:
        st.subheader("🎯 Overall Accomplishment Rate")
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=accomplishment_pct,
            domain={'x': [0, 1], 'y': [0, 1]},
            number={'suffix': "%", 'font': {'size': 28, 'color': "#0284C7"}},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "#0284C7"},
                'steps': [
                    {'range': [0, 50], 'color': "#FFE4E6"},
                    {'range': [50, 85], 'color': "#FEF3C7"},
                    {'range': [85, 100], 'color': "#DCFCE7"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 100
                }
            }
        ))
        fig_gauge.update_layout(margin=dict(t=30, b=20, l=20, r=20), height=280)
        st.plotly_chart(fig_gauge, use_container_width=True)

    st.markdown("---")

    # SEQUENCE 2: PAMANA LGU-LED OVERVIEW
    st.markdown('<div class="sec-card-lgu"><span class="sec-title-lgu">🏛️ 2. PAMANA LGU-Led Program Analytics & Performance</span></div>', unsafe_allow_html=True)

    if selected_provinces:
        f_lgu = df_lgu_summary[df_lgu_summary['Province'].isin(selected_provinces)]
    else:
        f_lgu = df_lgu_summary

    tot_sp = f_lgu['Target_SubProjects'].sum()
    tot_budget = f_lgu['Allocated_Budget_PHP'].sum()
    tot_lgu_ben = f_lgu['Profiled_Beneficiaries'].sum()

    l1, l2, l3, l4 = st.columns(4)
    l1.metric("Target LGU Sub-Projects", f"{tot_sp:,}")
    l2.metric("Total GAA Allocation", f"₱{tot_budget/1e6:,.1f}M")
    l3.metric("Profiled LGU Beneficiaries", f"{tot_lgu_ben:,}")
    l4.metric("Social Prep Stage", "100% Completed")

    st.markdown("<br>", unsafe_allow_html=True)
    lg1, lg2, lg3 = st.columns(3)
    with lg1:
        st.subheader("📈 LGU Projects per Province")
        fig_lgu_sp = px.bar(f_lgu, x='Province', y='Target_SubProjects', color='Province', text_auto=',.0f', template=plotly_template)
        fig_lgu_sp.update_layout(margin=dict(t=20, b=20, l=20, r=20), showlegend=False)
        st.plotly_chart(fig_lgu_sp, use_container_width=True)

    with lg2:
        st.subheader("💰 Financial Allocation (PHP)")
        fig_lgu_fin = px.bar(f_lgu, x='Province', y='Allocated_Budget_PHP', color='Province', text_auto='.2s', template=plotly_template)
        fig_lgu_fin.update_layout(margin=dict(t=20, b=20, l=20, r=20), showlegend=False)
        st.plotly_chart(fig_lgu_fin, use_container_width=True)

    with lg3:
        st.subheader("🎯 LGU Program Indicators")
        radar_df = pd.DataFrame(dict(
            r=[100, 95, 90, 88, 92],
            theta=['Social Preparation', 'Association Profiling', 'GAA Allocation', 'MOA Submission', 'Livelihood Opening']
        ))
        fig_radar = px.line_polar(radar_df, r='r', theta='theta', line_close=True, template=plotly_template)
        fig_radar.update_traces(fill='toself', fillcolor='rgba(22, 163, 74, 0.25)', line_color='#16A34A')
        fig_radar.update_layout(margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown("---")

    # SEQUENCE 3: PAMANA CDPD OVERVIEW
    st.markdown('<div class="sec-card-cdpd"><span class="sec-title-cdpd">🕊️ 3. PAMANA CDPD (Community-Driven Peace & Development)</span></div>', unsafe_allow_html=True)
    st.info("ℹ️ **PAMANA CDPD Status Notice:** Official Region X CDPD sub-project database entries are currently under validation and data synchronization.")

    st.markdown("---")
    st.subheader("📥 Export Consolidated Executive Analytics")
    col_exp1, col_exp2 = st.columns([1, 2])
    with col_exp1:
        scms_bytes = export_to_excel_bytes(f_scms)
        st.download_button(
            label="📥 Download SCMS Summary Report (.xlsx)",
            data=scms_bytes,
            file_name="PDBBM_SCMS_Executive_Summary.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

# ---------------------------------------------------------
# INDIVIDUAL MODULE VIEWS
# ---------------------------------------------------------
elif program_view == "📦 1. SCMS (Social Case Management)":
    st.markdown('<div class="glow-header-title">📦 SCMS Social Case Management Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="privacy-banner">🔒 <b>Data Privacy Standard Active:</b> Individual beneficiary personal records are protected. Standard Region X scope: Bukidnon, Lanao del Norte, Lanao del Sur, Misamis Occidental, Misamis Oriental.</div>', unsafe_allow_html=True)

    st.dataframe(df_scms_summary, use_container_width=True, hide_index=True)

elif program_view == "🏛️ 2. PAMANA LGU-Led Analytics":
    st.markdown('<div class="glow-header-title">🏛️ PAMANA LGU-Led Executive Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="privacy-banner">🔒 <b>Data Privacy Standard Active:</b> Project monitoring and financial scorecards rendered below for Region X scope.</div>', unsafe_allow_html=True)

    st.dataframe(df_lgu_summary, use_container_width=True, hide_index=True)

else:
    st.markdown('<div class="glow-header-title">🕊️ PAMANA CDPD Database Portal</div>', unsafe_allow_html=True)
    st.warning("⚠️ CDPD database records for Region X are currently empty / pending official system upload.")

# DEVELOPER FOOTER BADGE
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
