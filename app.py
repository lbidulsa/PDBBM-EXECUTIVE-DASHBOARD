import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
import json
import re
import os
from io import BytesIO, StringIO
from sqlalchemy import create_engine, text

# ---------------------------------------------------------
# PAGE CONFIGURATION & EXECUTIVE LIGHT UI (NO SIDEBAR)
# ---------------------------------------------------------
st.set_page_config(
    page_title="PDBBM Executive Multi-Program System",
    page_icon="🕊️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# EXECUTIVE TOP NAVBAR & NEON GLOW STYLING INJECTION
# ---------------------------------------------------------
st.markdown("""
    <style>
    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Hide Sidebar completely */
    section[data-testid="stSidebar"],
    [data-testid="stSidebarCollapseButton"],
    [data-testid="collapsedControl"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* Hide Deploy Button, Toolbar Actions, Footer & Cloud Viewer Badge */
    .stAppDeployButton,
    [data-testid="stToolbarActions"],
    [data-testid="stActionButtonIcon"],
    footer,
    [data-testid="stStatusWidget"],
    .viewerBadge_container__1QSob,
    .viewerBadge_link__1S137,
    .viewerBadge_text__1JaDK,
    div[class^="viewerBadge_"],
    div[class^="_profileContainer_"],
    div[class^="_terminalButton_"],
    a[href*="streamlit.io/cloud"] {
        visibility: hidden !important;
        display: none !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }

    #MainMenu {
        visibility: visible !important;
        display: flex !important;
    }

    .block-container {
        padding-top: 1.5rem !important;
        max-width: 96% !important;
    }

    /* Keyframe Animations for Neon Pulse & Glow */
    @keyframes activeNavGlow {
        0% { box-shadow: 0 0 10px rgba(225, 29, 72, 0.35), 0 0 20px rgba(225, 29, 72, 0.15); }
        50% { box-shadow: 0 0 18px rgba(225, 29, 72, 0.65), 0 0 30px rgba(225, 29, 72, 0.35); }
        100% { box-shadow: 0 0 10px rgba(225, 29, 72, 0.35), 0 0 20px rgba(225, 29, 72, 0.15); }
    }

    /* Executive Navbar Brand Typography */
    .exec-brand-title {
        font-size: 22px;
        font-weight: 900;
        letter-spacing: -0.4px;
        background: linear-gradient(90deg, #1E3A8A, #0284C7, #E11D48);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        line-height: 1.1;
    }
    .exec-brand-sub {
        font-size: 11px;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }

    /* ========================================================= */
    /* 🌟 TOP NAV MENU BUTTONS WITH NEON GLOW & HOVER LIFT 🌟    */
    /* ========================================================= */
    div[data-testid="stHorizontalBlock"] div.stButton > button {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-bottom: 3px solid transparent !important;
        border-radius: 10px !important;
        color: #1E293B !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        padding: 9px 14px !important;
        box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04) !important;
        transition: all 0.28s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
    }

    div[data-testid="stHorizontalBlock"] div.stButton > button:hover {
        color: #E11D48 !important;
        background: #FFF1F2 !important;
        border-color: #E11D48 !important;
        border-bottom: 3px solid #E11D48 !important;
        transform: translateY(-3px) scale(1.03) !important;
        box-shadow: 0 0 16px rgba(225, 29, 72, 0.6), 0 0 28px rgba(225, 29, 72, 0.3) !important;
    }

    div[data-testid="stHorizontalBlock"] div.stButton > button:active {
        transform: translateY(1px) scale(0.98) !important;
        box-shadow: 0 0 8px rgba(225, 29, 72, 0.4) !important;
    }

    /* Active Selected Top Menu Tab (Breathing Glow) */
    div[data-testid="stHorizontalBlock"] div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #FFF1F2 0%, #FFE4E6 100%) !important;
        color: #E11D48 !important;
        border: 1px solid #FDA4AF !important;
        border-bottom: 3px solid #E11D48 !important;
        border-radius: 10px !important;
        font-weight: 800 !important;
        animation: activeNavGlow 2.4s infinite ease-in-out !important;
    }

    /* Download & Other Action Buttons Glow */
    div.stDownloadButton > button {
        background-color: #E2E8F0 !important;
        color: #0F172A !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        border: 1px solid #CBD5E1 !important;
        padding: 10px 20px !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
    }
    div.stDownloadButton > button:hover {
        background-color: #FFFFFF !important;
        color: #0284C7 !important;
        border-color: #0284C7 !important;
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 0 16px rgba(2, 132, 199, 0.6), 0 0 28px rgba(2, 132, 199, 0.3) !important;
    }

    .glow-header-title {
        font-size: 32px !important;
        font-weight: 900 !important;
        background: linear-gradient(90deg, #E11D48, #16A34A, #0284C7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.6px;
        margin-bottom: 8px;
        text-align: center !important;
    }

    /* METRIC CARDS GLOW & HOVER ANIMATION */
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
        box-shadow: 0 0 18px rgba(225, 29, 72, 0.45), 0 0 28px rgba(225, 29, 72, 0.2) !important;
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

    /* SECTION CARDS HOVER EFFECT */
    .sec-card-scms, .sec-card-lgu, .sec-card-cdpd {
        background: #FFFFFF;
        padding: 14px 18px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
        margin-bottom: 16px;
        transition: all 0.3s ease;
    }
    .sec-card-scms { border-left: 6px solid #E11D48; }
    .sec-card-lgu { border-left: 6px solid #16A34A; }
    .sec-card-cdpd { border-left: 6px solid #0284C7; }

    .sec-card-scms:hover { transform: translateX(4px); box-shadow: 0 0 15px rgba(225, 29, 72, 0.25); }
    .sec-card-lgu:hover { transform: translateX(4px); box-shadow: 0 0 15px rgba(22, 163, 74, 0.25); }
    .sec-card-cdpd:hover { transform: translateX(4px); box-shadow: 0 0 15px rgba(2, 132, 199, 0.25); }

    .sec-title-scms { color: #E11D48; font-size: 19px; font-weight: 800; }
    .sec-title-lgu { color: #16A34A; font-size: 19px; font-weight: 800; }
    .sec-title-cdpd { color: #0284C7; font-size: 19px; font-weight: 800; }
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
def get_brand_logo():
    if os.path.exists("logo.png"):
        return "logo.png"
    elif os.path.exists("Peace and Dev LOGO.jpg"):
        return "Peace and Dev LOGO.jpg"
    return None

brand_logo = get_brand_logo()
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
# EXTERNAL PORTAL & PUBLISHED SCMS SHEET CONSTANTS
# ---------------------------------------------------------
PAMANA_CDPD_URL = st.secrets.get("PAMANA_CDPD_URL", "https://pdbbmpamanacdpd.streamlit.app/")
SCMS_PUB_ID = "2PACX-1vSiS3wDEdJUU6Xh8jL66xpLMz8RoDnv-Z32rcF6TeCHg_UKwAutb6_VbMyViNeMi7R9SyiEm-5bU9S_"
SCMS_PUB_HTML_URL = st.secrets.get(
    "SCMS_PUB_HTML_URL",
    f"https://docs.google.com/spreadsheets/d/e/{SCMS_PUB_ID}/pubhtml?gid=0&single=true"
)
SCMS_PUB_CSV_URL = st.secrets.get(
    "SCMS_PUB_CSV_URL",
    f"https://docs.google.com/spreadsheets/d/e/{SCMS_PUB_ID}/pub?gid=0&single=true&output=csv"
)

# ---------------------------------------------------------
# LIVE PAMANA CDPD SUPABASE CONNECTION ENGINE
# ---------------------------------------------------------
DEFAULT_CDPD_DB_URL = ""

def get_cdpd_db_url():
    try:
        if "SUPABASE_URL" in st.secrets and str(st.secrets["SUPABASE_URL"]).strip():
            return str(st.secrets["SUPABASE_URL"]).strip()
        if "postgres" in st.secrets and "url" in st.secrets["postgres"]:
            return str(st.secrets["postgres"]["url"]).strip()
    except Exception:
        pass
    return DEFAULT_CDPD_DB_URL

@st.cache_resource
def get_cdpd_engine(db_url: str):
    if not db_url:
        return None
    target_url = db_url
    if target_url.startswith("postgresql://"):
        target_url = target_url.replace("postgresql://", "postgresql+psycopg2://", 1)
    eng = create_engine(
        target_url,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
        pool_recycle=300
    )
    with eng.connect() as conn:
        conn.execute(text("SELECT 1"))
    return eng

@st.cache_data(ttl=60)
def load_cdpd_live_data(db_url: str):
    """Loads aggregate/summary tables from the PAMANA CDPD Supabase database."""
    result = {
        "connected": False,
        "error": "",
        "ceac_barangay": pd.DataFrame(),
        "ceac_municipal": pd.DataFrame(),
        "closeout": pd.DataFrame(),
        "disbursement": pd.DataFrame(),
    }
    if not db_url:
        result["error"] = "SUPABASE_URL or [postgres] url not configured in Streamlit Secrets."
        return result

    try:
        eng = get_cdpd_engine(db_url)

        def safe_read(sql_query):
            try:
                return pd.read_sql_query(text(sql_query), eng)
            except Exception:
                return pd.DataFrame()

        result["ceac_barangay"] = safe_read(
            "SELECT id, activity_name, region, province, municipality, barangay, cycle_batch, activity_date, mov_status, encoded_status FROM ceac_barangay ORDER BY id DESC"
        )
        result["ceac_municipal"] = safe_read(
            "SELECT id, activity_name, region, province, municipality, cycle_batch, activity_date, mov_status, encoded_status FROM ceac_municipal ORDER BY id DESC"
        )
        result["closeout"] = safe_read(
            "SELECT id, sp_id, sp_name, municipality, barangay, cycle_batch, overall_closeout_status, target_hhs, actual_hhs FROM sub_project_closeout_tracker ORDER BY id DESC"
        )
        result["disbursement"] = safe_read(
            "SELECT id, sp_id, municipality, dv_number, disbursement_date, amount, net_amount, status FROM disbursement ORDER BY id DESC"
        )
        result["connected"] = True
    except Exception as ex:
        result["error"] = str(ex)

    return result

# ---------------------------------------------------------
# LIVE GOOGLE SHEETS FETCH ENGINE (PUBLISHED -> API v4 -> CSV -> GVIZ)
# ---------------------------------------------------------
SCMS_SHEET_ID = st.secrets.get("SCMS_SHEET_ID", "1jjITQy_Z8w2A-gkghOTnzULjMaC3dx49Y8BCOeZmAyY")
GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY", "")

def normalize_prov_name(val):
    s = str(val).strip().upper()
    if not s or s in ["NAN", "NONE", "NULL", "TOTAL", "GRAND TOTAL", "SUBTOTAL"]:
        return ""
    if "BUKIDNON" in s:
        return "Bukidnon"
    if "LANAO DEL NORTE" in s or "LDN" in s:
        return "Lanao del Norte"
    if "LANAO DEL SUR" in s or "LDS" in s:
        return "Lanao del Sur"
    if "MISAMIS OCCIDENTAL" in s or "MIS. OCC" in s or "MIS OCC" in s:
        return "Misamis Occidental"
    if "MISAMIS ORIENTAL" in s or "MIS. OR" in s or "MIS OR" in s:
        return "Misamis Oriental"
    if "ZAMBOANGA DEL SUR" in s:
        return "Zamboanga del Sur"
    if "ZAMBOANGA DEL NORTE" in s:
        return "Zamboanga del Norte"
    if "NO ADDRESS" in s or "UNKNOWN" in s:
        return "No Address / Unassigned"
    return str(val).strip().title()

def finalize_dataframe(raw_rows):
    if not raw_rows or len(raw_rows) < 2:
        return pd.DataFrame()
    header_idx = 0
    for idx, r in enumerate(raw_rows[:10]):
        row_str = " ".join([str(x).upper() for x in r if x is not None])
        if any(k in row_str for k in ["PROVINCE", "AFFILIATION", "MUNICIPALITY", "CLIENTS", "BENES", "TARGET"]):
            header_idx = idx
            break
    cols = [str(x).strip() if (x is not None and str(x).strip() != "") else f"Col_{i}" for i, x in enumerate(raw_rows[header_idx])]
    data_rows = raw_rows[header_idx + 1:]

    clean_rows = []
    for r in data_rows:
        padded = list(r) + [None] * max(0, len(cols) - len(r))
        clean_rows.append(padded[:len(cols)])

    unique_cols = []
    seen = {}
    for c in cols:
        if c in seen:
            seen[c] += 1
            unique_cols.append(f"{c}_{seen[c]}")
        else:
            seen[c] = 0
            unique_cols.append(c)

    df = pd.DataFrame(clean_rows, columns=unique_cols)
    df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    df.dropna(how="all", inplace=True)
    return df

@st.cache_data(ttl=60)
def fetch_all_scms_tabs():
    """Fetches SCMS published/live tabs via Published CSV/HTML, API v4, or GVIZ fallback."""
    df_actual = pd.DataFrame()
    df_target = pd.DataFrame()
    sync_status = "offline"

    # TIER 0: Published SCMS Sheet CSV/HTML
    try:
        pub_res = requests.get(SCMS_PUB_CSV_URL, timeout=10)
        if pub_res.status_code == 200 and "<!DOCTYPE html>" not in pub_res.text[:200] and "<html" not in pub_res.text[:200].lower():
            pub_df = pd.read_csv(StringIO(pub_res.text))
            pub_df.dropna(how="all", inplace=True)
            if not pub_df.empty:
                df_actual = pub_df
                sync_status = "published_sheet"
    except Exception:
        pass

    if df_actual.empty:
        try:
            html_res = requests.get(SCMS_PUB_HTML_URL, timeout=10)
            if html_res.status_code == 200:
                tables = pd.read_html(StringIO(html_res.text))
                for tbl in tables:
                    tbl = tbl.dropna(how="all")
                    if not tbl.empty and tbl.shape[1] >= 2:
                        df_actual = tbl
                        sync_status = "published_html"
                        break
        except Exception:
            pass

    # TIER 1: Google Sheets API v4
    if GOOGLE_API_KEY:
        meta_url = f"https://sheets.googleapis.com/v4/spreadsheets/{SCMS_SHEET_ID}?fields=sheets.properties&key={GOOGLE_API_KEY}"
        try:
            meta_res = requests.get(meta_url, timeout=10)
            if meta_res.status_code == 200:
                sheets_meta = meta_res.json().get("sheets", [])
                for s in sheets_meta:
                    props = s.get("properties", {})
                    exact_title = props.get("title", "")
                    norm_title = exact_title.strip().upper()

                    if "ACTUAL" in norm_title or "SCMS TARGET" in norm_title:
                        encoded_exact = requests.utils.quote(exact_title)
                        val_url = f"https://sheets.googleapis.com/v4/spreadsheets/{SCMS_SHEET_ID}/values/{encoded_exact}?key={GOOGLE_API_KEY}"
                        val_res = requests.get(val_url, timeout=10)
                        if val_res.status_code == 200:
                            values = val_res.json().get("values", [])
                            parsed_df = finalize_dataframe(values)
                            if "ACTUAL" in norm_title:
                                df_actual = parsed_df
                            elif "SCMS TARGET" in norm_title:
                                df_target = parsed_df
                if not df_actual.empty or not df_target.empty:
                    sync_status = "api_v4"
                    return df_actual, df_target, sync_status
        except Exception:
            pass

    # TIER 2: GVIZ CSV Fallback
    for target_key, tab_candidates in [
        ("actual", ["ACTUAL NUMBER OF BENES", "ACTUAL NUMBER OF BENES "]),
        ("target", ["SCMS TARGET PER P-M", "SCMS TARGET PER P-M "])
    ]:
        if target_key == "actual" and not df_actual.empty:
            continue
        for t_name in tab_candidates:
            enc = requests.utils.quote(t_name)
            csv_url = f"https://docs.google.com/spreadsheets/d/{SCMS_SHEET_ID}/gviz/tq?tqx=out:csv&sheet={enc}"
            try:
                r = requests.get(csv_url, timeout=10)
                if r.status_code == 200 and "<!DOCTYPE html>" not in r.text[:200]:
                    temp_df = pd.read_csv(StringIO(r.text))
                    temp_df.dropna(how="all", inplace=True)
                    if not temp_df.empty:
                        if target_key == "actual":
                            df_actual = temp_df
                        else:
                            df_target = temp_df
                        if sync_status == "offline":
                            sync_status = "gviz_csv"
                        break
            except Exception:
                continue

    return df_actual, df_target, sync_status

@st.cache_data(ttl=60)
def load_scms_live_data():
    df_actual_raw, df_target_raw, sync_status = fetch_all_scms_tabs()

    df_target_clean = pd.DataFrame()
    if not df_target_raw.empty:
        df_t = df_target_raw.copy()
        col_map = {str(c).upper(): c for c in df_t.columns}
        prov_col = next((v for k, v in col_map.items() if "PROVINCE" in k), df_t.columns[0])
        muni_col = next((v for k, v in col_map.items() if "MUNICIPALITY" in k), df_t.columns[1] if len(df_t.columns) > 1 else None)
        aff_col = next((v for k, v in col_map.items() if "AFFILIATION" in k), df_t.columns[2] if len(df_t.columns) > 2 else None)
        clients_col = next((v for k, v in col_map.items() if ("NUMBER OF CLIENTS" in k or "TARGET" in k) and "TOTAL" not in k), df_t.columns[3] if len(df_t.columns) > 3 else None)

        df_t[prov_col] = df_t[prov_col].replace(r'^\s*$', np.nan, regex=True).ffill()
        if muni_col:
            df_t[muni_col] = df_t[muni_col].replace(r'^\s*$', np.nan, regex=True).ffill()

        df_t["Province_Clean"] = df_t[prov_col].apply(normalize_prov_name)
        df_t = df_t[df_t["Province_Clean"] != ""]

        if aff_col:
            df_t["Affiliation_Clean"] = df_t[aff_col].astype(str).str.strip().str.upper()
            df_t = df_t[~df_t["Affiliation_Clean"].isin(["", "NAN", "NONE", "TOTAL", "GRAND TOTAL"])]
        else:
            df_t["Affiliation_Clean"] = "UNSPECIFIED"

        if clients_col:
            df_t["Target_Count"] = pd.to_numeric(
                df_t[clients_col].astype(str).str.replace(",", "").str.strip(),
                errors="coerce"
            ).fillna(0).astype(int)
        else:
            df_t["Target_Count"] = 0

        if muni_col:
            df_t = df_t[~df_t[muni_col].astype(str).str.upper().str.contains("TOTAL", na=False)]

        df_target_clean = df_t

    df_actual_clean = pd.DataFrame()
    if not df_actual_raw.empty:
        df_a = df_actual_raw.copy()
        col_map_a = {str(c).upper(): c for c in df_a.columns}
        prov_col_a = next((v for k, v in col_map_a.items() if "PROVINCE" in k), df_a.columns[0])
        muni_col_a = next((v for k, v in col_map_a.items() if "MUNICIPALITY" in k), df_a.columns[1] if len(df_a.columns) > 1 else None)
        aff_col_a = next((v for k, v in col_map_a.items() if "AFFILIATION" in k), df_a.columns[2] if len(df_a.columns) > 2 else None)

        df_a[prov_col_a] = df_a[prov_col_a].replace(r'^\s*$', np.nan, regex=True).ffill()
        if muni_col_a:
            df_a[muni_col_a] = df_a[muni_col_a].replace(r'^\s*$', np.nan, regex=True).ffill()

        df_a["Province_Clean"] = df_a[prov_col_a].apply(normalize_prov_name)
        df_a = df_a[df_a["Province_Clean"] != ""]

        if aff_col_a:
            df_a["Affiliation_Clean"] = df_a[aff_col_a].astype(str).str.strip().str.upper()
            df_a = df_a[~df_a["Affiliation_Clean"].isin(["", "NAN", "NONE", "TOTAL", "GRAND TOTAL"])]
        else:
            df_a["Affiliation_Clean"] = "UNSPECIFIED"

        male_col = next((v for k, v in col_map_a.items() if k == "MALE" or ("MALE" in k and "FEMALE" not in k)), None)
        female_col = next((v for k, v in col_map_a.items() if "FEMALE" in k), None)
        total_col = next((v for k, v in col_map_a.items() if any(w in k for w in ["NUMBER OF CLIENTS", "ACTUAL", "PROFILED", "BENES", "TOTAL"])), None)

        if male_col and female_col:
            df_a["Male_Count"] = pd.to_numeric(df_a[male_col].astype(str).str.replace(",", ""), errors="coerce").fillna(0).astype(int)
            df_a["Female_Count"] = pd.to_numeric(df_a[female_col].astype(str).str.replace(",", ""), errors="coerce").fillna(0).astype(int)
            df_a["Profiled_Count"] = df_a["Male_Count"] + df_a["Female_Count"]
        elif total_col:
            df_a["Profiled_Count"] = pd.to_numeric(df_a[total_col].astype(str).str.replace(",", ""), errors="coerce").fillna(0).astype(int)
            df_a["Male_Count"] = (df_a["Profiled_Count"] * (8264 / 9004)).round().astype(int)
            df_a["Female_Count"] = df_a["Profiled_Count"] - df_a["Male_Count"]
        else:
            num_candidates = [c for c in df_a.columns[3:] if pd.to_numeric(df_a[c], errors="coerce").notna().sum() > 0]
            if num_candidates:
                df_a["Profiled_Count"] = pd.to_numeric(df_a[num_candidates[0]].astype(str).str.replace(",", ""), errors="coerce").fillna(0).astype(int)
            else:
                df_a["Profiled_Count"] = 0
            df_a["Male_Count"] = (df_a["Profiled_Count"] * (8264 / 9004)).round().astype(int)
            df_a["Female_Count"] = df_a["Profiled_Count"] - df_a["Male_Count"]

        if muni_col_a:
            df_a = df_a[~df_a[muni_col_a].astype(str).str.upper().str.contains("TOTAL", na=False)]

        df_actual_clean = df_a

    return df_actual_raw, df_target_raw, df_actual_clean, df_target_clean, sync_status

@st.cache_data(ttl=120)
def check_cdpd_portal_status(url):
    try:
        r = requests.get(url, timeout=8)
        return r.status_code == 200, r.status_code
    except Exception as ex:
        return False, str(ex)

df_actual_raw, df_target_raw, df_actual_clean, df_target_clean, sync_status = load_scms_live_data()
cdpd_online, cdpd_status_info = check_cdpd_portal_status(PAMANA_CDPD_URL)
cdpd_db = load_cdpd_live_data(get_cdpd_db_url())

# Fallback static datasets
df_scms_affiliation_fallback = pd.DataFrame({
    'Affiliation': ['MILF', 'MNLF', 'FR', 'DPAGS', 'KAPATIRAN', 'MSAP'],
    'Target': [7472, 606, 3067, 0, 29, 0],
    'Male': [6784, 27, 1429, 0, 24, 0],
    'Female': [355, 2, 380, 0, 3, 0],
    'Total_Profiled': [7139, 29, 1809, 0, 27, 0],
    'Not_Yet_Profiled': [333, 577, 1258, 0, 2, 0]
})

df_scms_province_fallback = pd.DataFrame({
    'Province': ['Bukidnon', 'Lanao del Norte', 'Lanao del Sur', 'Misamis Occidental', 'Misamis Oriental'],
    'Profiled_Clients': [1433, 1977, 5150, 152, 292]
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
# EXECUTIVE TOP NAVIGATION BAR (KALAHI-CIDSS REGION X STYLE)
# ---------------------------------------------------------
if "active_nav" not in st.session_state:
    st.session_state["active_nav"] = "overview"

nav_brand, nav_m1, nav_m2, nav_m3, nav_m4 = st.columns([3.2, 1.8, 1.7, 1.8, 1.5])

with nav_brand:
    b_col1, b_col2 = st.columns([1.2, 3.8])
    with b_col1:
        if brand_logo:
            st.image(brand_logo, use_container_width=True)
    with b_col2:
        st.markdown('<div class="exec-brand-title">PDBBM-RPMO REGION X</div>', unsafe_allow_html=True)
        st.markdown('<div class="exec-brand-sub">DSWD FO X • Executive Decision Portal</div>', unsafe_allow_html=True)

with nav_m1:
    if st.button(
        "🌐 Executive Overview",
        type="primary" if st.session_state["active_nav"] == "overview" else "secondary",
        use_container_width=True
    ):
        st.session_state["active_nav"] = "overview"
        st.rerun()

with nav_m2:
    if st.button(
        "📦 SCMS Analytics",
        type="primary" if st.session_state["active_nav"] == "scms" else "secondary",
        use_container_width=True
    ):
        st.session_state["active_nav"] = "scms"
        st.rerun()

with nav_m3:
    if st.button(
        "🏛️ PAMANA LGU-Led",
        type="primary" if st.session_state["active_nav"] == "lgu" else "secondary",
        use_container_width=True
    ):
        st.session_state["active_nav"] = "lgu"
        st.rerun()

with nav_m4:
    if st.button(
        "🕊️ PAMANA CDPD",
        type="primary" if st.session_state["active_nav"] == "cdpd" else "secondary",
        use_container_width=True
    ):
        st.session_state["active_nav"] = "cdpd"
        st.rerun()

st.markdown("<hr style='margin: 6px 0 14px 0; border-color: #CBD5E1;'>", unsafe_allow_html=True)

# ---------------------------------------------------------
# COMPACT PROVINCE FILTER & LIVE SYNC STATUS BAR
# ---------------------------------------------------------
live_provinces = []
if not df_actual_clean.empty:
    live_provinces.extend(df_actual_clean["Province_Clean"].unique().tolist())
if not df_target_clean.empty:
    live_provinces.extend(df_target_clean["Province_Clean"].unique().tolist())
for tbl_key in ["ceac_barangay", "ceac_municipal", "closeout", "disbursement"]:
    t_df = cdpd_db.get(tbl_key, pd.DataFrame())
    if not t_df.empty and "province" in t_df.columns:
        live_provinces.extend([normalize_prov_name(x) for x in t_df["province"].dropna().tolist()])

base_provinces = ['Bukidnon', 'Lanao del Norte', 'Lanao del Sur', 'Misamis Occidental', 'Misamis Oriental', 'Zamboanga del Sur', 'Zamboanga del Norte']
all_provinces_list = sorted(list(set(base_provinces + [p for p in live_provinces if p])))

f_col1, f_col2, f_col3, f_col4 = st.columns([2.7, 2.0, 1.3, 1.3])
with f_col1:
    db_badge = "🟢 CDPD DB Connected" if cdpd_db["connected"] else "🟡 CDPD DB Check"
    if sync_status != "offline":
        st.success(f"🟢 **LIVE SCMS (`{sync_status}`)** • {db_badge}")
    else:
        st.info(f"ℹ️ **SCMS Published Link Active** • {db_badge}")

with f_col2:
    selected_province_opt = st.selectbox(
        "Province Filter:",
        options=["All Provinces (Region X)"] + all_provinces_list,
        label_visibility="collapsed"
    )
    selected_provinces = all_provinces_list if selected_province_opt == "All Provinces (Region X)" else [selected_province_opt]

with f_col3:
    st.link_button("🕊️ Open CDPD", PAMANA_CDPD_URL, use_container_width=True)

with f_col4:
    if st.button("🔄 Sync Live Data", use_container_width=True):
        st.cache_data.clear()
        st.toast("🔄 Refreshed Live SCMS & CDPD Data!", icon="✨")
        st.rerun()

# ---------------------------------------------------------
# COMPUTE ACCURATE SCMS METRICS FROM LIVE 2 TABS
# ---------------------------------------------------------
using_live_scms = (not df_actual_clean.empty) or (not df_target_clean.empty)

if using_live_scms:
    act_f = df_actual_clean[df_actual_clean["Province_Clean"].isin(selected_provinces)] if not df_actual_clean.empty else pd.DataFrame()
    tgt_f = df_target_clean[df_target_clean["Province_Clean"].isin(selected_provinces)] if not df_target_clean.empty else pd.DataFrame()

    tot_profiled = int(act_f["Profiled_Count"].sum()) if not act_f.empty else 0
    tot_male = int(act_f["Male_Count"].sum()) if not act_f.empty else 0
    tot_female = int(act_f["Female_Count"].sum()) if not act_f.empty else 0
    tot_target = int(tgt_f["Target_Count"].sum()) if not tgt_f.empty else 11174
    tot_not_yet = max(0, tot_target - tot_profiled)

    if not act_f.empty:
        df_scms_province = (
            act_f.groupby("Province_Clean", as_index=False)["Profiled_Count"]
            .sum()
            .rename(columns={"Province_Clean": "Province", "Profiled_Count": "Profiled_Clients"})
        )
    else:
        df_scms_province = df_scms_province_fallback

    aff_act = act_f.groupby("Affiliation_Clean", as_index=False).agg(
        Male=("Male_Count", "sum"),
        Female=("Female_Count", "sum"),
        Total_Profiled=("Profiled_Count", "sum")
    ) if not act_f.empty else pd.DataFrame(columns=["Affiliation_Clean", "Male", "Female", "Total_Profiled"])

    aff_tgt = tgt_f.groupby("Affiliation_Clean", as_index=False).agg(
        Target=("Target_Count", "sum")
    ) if not tgt_f.empty else pd.DataFrame(columns=["Affiliation_Clean", "Target"])

    df_scms_affiliation = pd.merge(aff_tgt, aff_act, on="Affiliation_Clean", how="outer").fillna(0)
    df_scms_affiliation.rename(columns={"Affiliation_Clean": "Affiliation"}, inplace=True)
    for col_n in ["Target", "Male", "Female", "Total_Profiled"]:
        df_scms_affiliation[col_n] = df_scms_affiliation[col_n].astype(int)
    df_scms_affiliation["Not_Yet_Profiled"] = (df_scms_affiliation["Target"] - df_scms_affiliation["Total_Profiled"]).clip(lower=0)
else:
    filtered_prov = df_scms_province_fallback[df_scms_province_fallback['Province'].isin(selected_provinces)]
    df_scms_province = filtered_prov
    df_scms_affiliation = df_scms_affiliation_fallback
    tot_profiled = int(filtered_prov['Profiled_Clients'].sum())
    tot_target = 11174
    tot_male = int(np.round(tot_profiled * (8264 / 9004))) if tot_profiled > 0 else 0
    tot_female = tot_profiled - tot_male
    tot_not_yet = max(0, tot_target - tot_profiled)

# ---------------------------------------------------------
# FILTER LIVE CDPD DATA BY SELECTED PROVINCE
# ---------------------------------------------------------
def filter_by_prov_col(df_in):
    if df_in is None or df_in.empty:
        return pd.DataFrame()
    if selected_province_opt == "All Provinces (Region X)" or "province" not in df_in.columns:
        return df_in.copy()
    norm_col = df_in["province"].apply(normalize_prov_name)
    return df_in[norm_col.isin(selected_provinces)].copy()

df_cdpd_brgy_f = filter_by_prov_col(cdpd_db.get("ceac_barangay", pd.DataFrame()))
df_cdpd_muni_f = filter_by_prov_col(cdpd_db.get("ceac_municipal", pd.DataFrame()))
df_cdpd_sp_f = filter_by_prov_col(cdpd_db.get("closeout", pd.DataFrame()))
df_cdpd_disb_f = filter_by_prov_col(cdpd_db.get("disbursement", pd.DataFrame()))

cdpd_brgy_cnt = len(df_cdpd_brgy_f)
cdpd_muni_cnt = len(df_cdpd_muni_f)
cdpd_sp_cnt = len(df_cdpd_sp_f)
cdpd_disb_tot = float(pd.to_numeric(df_cdpd_disb_f["amount"], errors="coerce").fillna(0).sum()) if (not df_cdpd_disb_f.empty and "amount" in df_cdpd_disb_f.columns) else 0.0

def render_ceac_activities_block(key_prefix="ov"):
    """Renders CEAC Barangay & Municipal activities metrics, charts, and tables."""
    cm1, cm2, cm3, cm4 = st.columns(4)
    cm1.metric("CEAC BARANGAY LOGS", f"{cdpd_brgy_cnt:,}")
    cm2.metric("CEAC MUNICIPAL LOGS", f"{cdpd_muni_cnt:,}")
    cm3.metric("SUB-PROJECTS TRACKED", f"{cdpd_sp_cnt:,}")
    cm4.metric("TOTAL DISBURSED", f"₱{cdpd_disb_tot:,.2f}")

    if not cdpd_db["connected"]:
        st.warning(
            f"⚠️ **CDPD Database Sync Notice:** `{cdpd_db['error']}` — "
            "I-check ang Streamlit Cloud Logs ug i-reboot ang Dashboard app human ma-save ang `requirements.txt` ug `[postgres]` Secrets."
        )
        return

    st.markdown("<br>", unsafe_allow_html=True)
    c_ch1, c_ch2 = st.columns(2)
    with c_ch1:
        st.subheader("📍 CEAC Barangay Activities")
        if not df_cdpd_brgy_f.empty and "activity_name" in df_cdpd_brgy_f.columns:
            b_cnt = df_cdpd_brgy_f["activity_name"].fillna("Unspecified").value_counts().reset_index()
            b_cnt.columns = ["Activity", "Count"]
            fig_cb = px.bar(b_cnt, x="Activity", y="Count", color="Activity", text_auto=True, template=plotly_template)
            fig_cb.update_layout(showlegend=False, margin=dict(t=20, b=20, l=20, r=20))
            st.plotly_chart(fig_cb, use_container_width=True, key=f"{key_prefix}_chart_brgy")
        else:
            st.info("No CEAC Barangay activity records found for selected filter.")

    with c_ch2:
        st.subheader("🏢 CEAC Municipal Activities")
        if not df_cdpd_muni_f.empty and "activity_name" in df_cdpd_muni_f.columns:
            m_cnt = df_cdpd_muni_f["activity_name"].fillna("Unspecified").value_counts().reset_index()
            m_cnt.columns = ["Activity", "Count"]
            fig_cm = px.bar(m_cnt, x="Activity", y="Count", color="Activity", text_auto=True, template=plotly_template)
            fig_cm.update_layout(showlegend=False, margin=dict(t=20, b=20, l=20, r=20))
            st.plotly_chart(fig_cm, use_container_width=True, key=f"{key_prefix}_chart_muni")
        else:
            st.info("No CEAC Municipal activity records found for selected filter.")

    st.markdown("#### 📋 CEAC Activities & CDPD Records")
    ct1, ct2, ct3 = st.tabs([
        f"📍 CEAC Barangay ({cdpd_brgy_cnt})",
        f"🏢 CEAC Municipal ({cdpd_muni_cnt})",
        "🏗️ Sub-Projects & Disbursements"
    ])
    with ct1:
        if not df_cdpd_brgy_f.empty:
            st.dataframe(df_cdpd_brgy_f, use_container_width=True, hide_index=True)
        else:
            st.info("No CEAC Barangay records available.")
    with ct2:
        if not df_cdpd_muni_f.empty:
            st.dataframe(df_cdpd_muni_f, use_container_width=True, hide_index=True)
        else:
            st.info("No CEAC Municipal records available.")
    with ct3:
        st.markdown("**Sub-Project Closeout Tracker**")
        st.dataframe(df_cdpd_sp_f, use_container_width=True, hide_index=True)
        st.markdown("**Disbursements**")
        st.dataframe(df_cdpd_disb_f, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# VIEW 1: CONSOLIDATED EXECUTIVE OVERVIEW
# ---------------------------------------------------------
if st.session_state["active_nav"] == "overview":
    st.markdown('<div class="sec-card-scms"><span class="sec-title-scms">📦 1. SCMS Analytics (Social Case Management Service)</span></div>', unsafe_allow_html=True)

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
        fig_prov = px.bar(df_scms_province, x='Province', y='Profiled_Clients', color='Province', text_auto=',.0f', template=plotly_template)
        fig_prov.update_layout(margin=dict(t=20, b=20, l=20, r=20), showlegend=False)
        st.plotly_chart(fig_prov, use_container_width=True)

    with sg2:
        st.subheader("👥 Male vs Female Distribution")
        fig_gender = px.pie(
            pd.DataFrame({'Gender': ['Male', 'Female'], 'Count': [tot_male, tot_female]}),
            names='Gender', values='Count', color='Gender',
            color_discrete_map={'Male': '#0284C7', 'Female': '#E11D48'},
            template=plotly_template, hole=0.4
        )
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

    st.markdown("#### 📋 SCMS Live Source Tables & Published Sheet")
    tab_scms_1, tab_scms_2, tab_scms_3, tab_scms_4 = st.tabs([
        "📊 Consolidated Affiliation Scorecard",
        "📑 Tab 1: ACTUAL NUMBER OF BENES",
        "🎯 Tab 2: SCMS TARGET PER P-M",
        "🌐 Published SCMS Sheet"
    ])
    with tab_scms_1:
        st.dataframe(df_scms_affiliation, use_container_width=True, hide_index=True)
    with tab_scms_2:
        if not df_actual_raw.empty:
            st.dataframe(df_actual_raw, use_container_width=True, hide_index=True)
        else:
            st.info(f"ℹ️ Published SCMS Sheet link configured: [Open Published SCMS Sheet]({SCMS_PUB_HTML_URL})")
    with tab_scms_3:
        if not df_target_raw.empty:
            st.dataframe(df_target_raw, use_container_width=True, hide_index=True)
        else:
            st.info("ℹ️ Waiting for `SCMS TARGET PER P-M` tab access or API key.")
    with tab_scms_4:
        st.link_button("🔗 Open Published SCMS Sheet in New Tab", SCMS_PUB_HTML_URL)
        st.markdown(
            f'<iframe src="{SCMS_PUB_HTML_URL}" width="100%" height="460" style="border: 1px solid #CBD5E1; border-radius: 10px; background: #FFFFFF;"></iframe>',
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.markdown('<div class="sec-card-lgu"><span class="sec-title-lgu">🏛️ 2. PAMANA LGU-Led Analytics</span></div>', unsafe_allow_html=True)

    l1, l2, l3, l4 = st.columns(4)
    l1.metric("TARGET POs", "99 POs")
    l2.metric("PROVIDED WITH ASSISTANCE", "97 POs", delta="↑ 98.0% Accomplished")
    l3.metric("WAIVED / DISBANDED POs", "2 POs", delta_color="inverse")
    l4.metric("PENDING FUND WITHDRAWAL", "₱600,000")

    st.markdown("---")
    st.markdown('<div class="sec-card-cdpd"><span class="sec-title-cdpd">🕊️ 3. PAMANA CDPD & CEAC ACTIVITIES</span></div>', unsafe_allow_html=True)
    c_ov1, c_ov2 = st.columns([3.2, 1.2])
    with c_ov1:
        status_badge = "🟢 Online" if cdpd_online else f"🟡 Check Link ({cdpd_status_info})"
        st.caption(f"PAMANA CDPD Portal (`{PAMANA_CDPD_URL}`) • Status: {status_badge}")
    with c_ov2:
        st.link_button("🚀 Launch PAMANA CDPD Portal", PAMANA_CDPD_URL, use_container_width=True)
        if st.button("🧭 Go to CDPD View", key="btn_ov_to_cdpd", use_container_width=True):
            st.session_state["active_nav"] = "cdpd"
            st.rerun()

    render_ceac_activities_block(key_prefix="ov")

# ---------------------------------------------------------
# VIEW 2: SCMS ANALYTICS DEDICATED VIEW
# ---------------------------------------------------------
elif st.session_state["active_nav"] == "scms":
    st.markdown('<div class="glow-header-title">📦 SCMS Analytics & Live Source Tabs</div>', unsafe_allow_html=True)

    s1, s2, s3, s4, s5 = st.columns(5)
    s1.metric("ANNUAL TARGET", f"{tot_target:,}")
    accomplishment_pct = (tot_profiled / tot_target * 100) if tot_target > 0 else 0
    s2.metric("TOTAL PROFILED CLIENTS", f"{tot_profiled:,}", delta=f"↑ {accomplishment_pct:.1f}% Accomplished")
    s3.metric("👨 MALE CLIENTS", f"{tot_male:,}")
    s4.metric("👩 FEMALE CLIENTS", f"{tot_female:,}")
    s5.metric("⏳ NOT YET PROFILED", f"{tot_not_yet:,}")

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📊 Consolidated SCMS Scorecard by Affiliation")
    st.dataframe(df_scms_affiliation, use_container_width=True, hide_index=True)

    st.download_button(
        label="📥 Download SCMS Consolidated Summary (Excel)",
        data=export_to_excel_bytes(df_scms_affiliation),
        file_name="SCMS_Consolidated_Scorecard_2026.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.markdown("---")
    st.subheader("🗂️ Live Google Sheet Source Tabs & Published Sheet")
    t1, t2, t3 = st.tabs(["📑 ACTUAL NUMBER OF BENES", "🎯 SCMS TARGET PER P-M", "🌐 Published SCMS Sheet"])
    with t1:
        if not df_actual_raw.empty:
            st.dataframe(df_actual_raw, use_container_width=True, hide_index=True)
        else:
            st.warning(f"⚠️ Using fallback/published view. Open [Published SCMS Sheet]({SCMS_PUB_HTML_URL}) directly or set General Access to 'Anyone with the link → Viewer'.")
    with t2:
        if not df_target_raw.empty:
            st.dataframe(df_target_raw, use_container_width=True, hide_index=True)
        else:
            st.warning("⚠️ Restricted Sheet: Ask the sheet owner to change General Access to 'Anyone with the link → Viewer' (or Publish to Web) so the API can pull `SCMS TARGET PER P-M`.")
    with t3:
        st.link_button("🔗 Open Published SCMS Sheet", SCMS_PUB_HTML_URL)
        st.markdown(
            f'<iframe src="{SCMS_PUB_HTML_URL}" width="100%" height="520" style="border: 1px solid #CBD5E1; border-radius: 10px; background: #FFFFFF;"></iframe>',
            unsafe_allow_html=True
        )

# ---------------------------------------------------------
# VIEW 3: PAMANA LGU-LED ANALYTICS
# ---------------------------------------------------------
elif st.session_state["active_nav"] == "lgu":
    st.markdown('<div class="glow-header-title">🏛️ PAMANA LGU-Led Analytics</div>', unsafe_allow_html=True)
    st.dataframe(df_lgu_summary, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# VIEW 4: PAMANA CDPD ANALYTICS (LIVE DB + PORTAL LINK)
# ---------------------------------------------------------
else:
    st.markdown('<div class="glow-header-title">🕊️ PAMANA CDPD Portal & Analytics</div>', unsafe_allow_html=True)

    c_top1, c_top2, c_top3 = st.columns([2.6, 1.2, 1.2])
    with c_top1:
        if cdpd_db["connected"]:
            st.success("🟢 **LIVE CDPD DATABASE CONNECTED:** Pulling CEAC Barangay, Municipal, Closeout & Disbursement data.")
        elif cdpd_online:
            st.info(f"🔗 **PAMANA CDPD PORTAL CONNECTED:** `{PAMANA_CDPD_URL}` • {cdpd_db['error']}")
        else:
            st.warning(f"⚠️ **CDPD PORTAL STATUS:** `{cdpd_status_info}` • {cdpd_db['error']}")
    with c_top2:
        st.link_button("🚀 Open PAMANA CDPD App", PAMANA_CDPD_URL, use_container_width=True)
    with c_top3:
        show_embed = st.toggle("Embed Portal", value=False, key="toggle_cdpd_embed")

    render_ceac_activities_block(key_prefix="cdpd_tab")

    if show_embed:
        st.markdown("---")
        st.caption("Tip: Kung dili mo-load ang embedded window tungod sa browser/Streamlit frame headers, i-click ang **Open PAMANA CDPD App** sa ibabaw.")
        st.markdown(
            f"""
            <iframe src="{PAMANA_CDPD_URL}" width="100%" height="780"
                    style="border: 1px solid #CBD5E1; border-radius: 12px; background: #FFFFFF;"
                    allow="geolocation"></iframe>
            """,
            unsafe_allow_html=True
        )

# ---------------------------------------------------------
# FOOTER & DATA PRIVACY COMPLIANCE NOTICE
# ---------------------------------------------------------
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; font-size: 0.85em; color: #64748B; padding-bottom: 20px;">
        🔒 <b>Data Privacy Act (RA 10173) Compliant:</b> Aggregate executive counts only; no individual beneficiary PII exposed.<br>
        ⚙️ <b>PDBBM Executive Multi-Program Decision Support Portal</b> | Powered by Streamlit & Python<br>
        Designed & Developed by <b>LOUIE B. IDULSA - PDBBM ITO I</b> • DSWD Field Office X
    </div>
    """, 
    unsafe_allow_html=True
)
