import os
os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"

import streamlit as st

st.set_page_config(
    page_title="Metro Loan App",
    page_icon="🗂️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Instrument+Serif:ital@0;1&display=swap');

html, body, .stApp {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

section[data-testid="stSidebar"] { width: 230px !important; }
section[data-testid="stSidebar"] > div { padding: 0 !important; }

.block-container { max-width: 860px; padding: 48px 56px 72px !important; }

.page-eyebrow {
    font-size: 10px; font-weight: 700; letter-spacing: 0.22em;
    text-transform: uppercase; margin-bottom: 6px; color: #c4933f;
}
.page-title {
    font-family: 'Instrument Serif', serif;
    font-size: 40px; line-height: 1.1; margin-bottom: 10px;
}
.page-desc {
    font-size: 14px; line-height: 1.7; max-width: 540px;
    margin-bottom: 40px; opacity: 0.65;
}

.feature-grid {
    display: grid; grid-template-columns: repeat(2, 1fr);
    gap: 14px; margin-bottom: 36px;
}
.feature-card {
    border-radius: 14px; padding: 22px; border: 1px solid;
    transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
}
.feature-card:hover { transform: translateY(-3px); }
.feature-card-icon { font-size: 22px; margin-bottom: 10px; }
.feature-card-title {
    font-family: 'Instrument Serif', serif; font-size: 15px; margin-bottom: 5px;
}
.feature-card-desc { font-size: 12px; line-height: 1.6; opacity: 0.6; }
.author-line { font-size: 11px; opacity: 0.35; margin-top: 4px; }

/* ── LIGHT ── */
[data-theme="light"] .stApp { background: #f7f6f3 !important; }
[data-theme="light"] section[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #ece8e2 !important;
}
[data-theme="light"] .page-title  { color: #1a1a2e; }
[data-theme="light"] .feature-card {
    background: #ffffff; border-color: #e5e1db; color: #1a1a2e;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
[data-theme="light"] .feature-card:hover {
    border-color: #c4933f; box-shadow: 0 6px 24px rgba(196,147,63,0.12);
}
[data-theme="light"] .stButton > button,
[data-theme="light"] .stDownloadButton > button {
    background: #1a1a2e !important; color: #ffffff !important;
    border: none !important; border-radius: 10px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important; font-size: 13px !important;
    padding: 11px 26px !important;
    box-shadow: 0 2px 12px rgba(26,26,46,0.15) !important;
    transition: all 0.2s ease !important;
}
[data-theme="light"] .stButton > button:hover,
[data-theme="light"] .stDownloadButton > button:hover {
    background: #2e2e4a !important; transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(26,26,46,0.22) !important;
}

/* ── DARK ── */
[data-theme="dark"] .stApp { background: #0a0c14 !important; }
[data-theme="dark"] section[data-testid="stSidebar"] {
    background: #0d0f18 !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}
[data-theme="dark"] .page-title  { color: #f0f2f8; }
[data-theme="dark"] .page-desc   { color: #c8d0e0; }
[data-theme="dark"] .author-line { color: #c8d0e0; }
[data-theme="dark"] .feature-card {
    background: #13172a; border-color: rgba(255,255,255,0.07); color: #e2e8f0;
}
[data-theme="dark"] .feature-card:hover {
    border-color: #c4933f; box-shadow: 0 6px 28px rgba(196,147,63,0.12);
}
[data-theme="dark"] .stButton > button,
[data-theme="dark"] .stDownloadButton > button {
    background: #c4933f !important; color: #ffffff !important;
    border: none !important; border-radius: 10px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important; font-size: 13px !important;
    padding: 11px 26px !important;
    box-shadow: 0 2px 16px rgba(196,147,63,0.25) !important;
    transition: all 0.2s ease !important;
}
[data-theme="dark"] .stButton > button:hover,
[data-theme="dark"] .stDownloadButton > button:hover {
    background: #d4a34a !important; transform: translateY(-1px) !important;
    box-shadow: 0 4px 24px rgba(196,147,63,0.4) !important;
}

#MainMenu, footer, header { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
.stSpinner > div { border-top-color: #c4933f !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-eyebrow">Metro Loan App</div>
<div class="page-title">File Organiser</div>
<div class="page-desc">Upload your raw loan, mutasi, or pajak files and get clean,
structured outputs in seconds — no manual work needed.</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="feature-grid">
    <div class="feature-card">
        <div class="feature-card-icon">🧾</div>
        <div class="feature-card-title">Mutasi Bank MG (TXT)</div>
        <div class="feature-card-desc">Parse raw TXT loan files into structured loan details and subtotals.</div>
    </div>
    <div class="feature-card">
        <div class="feature-card-icon">📄</div>
        <div class="feature-card-title">Mutasi Bank MG (CSV)</div>
        <div class="feature-card-desc">Split Debit and Credit from CSV bank mutation exports automatically.</div>
    </div>
    <div class="feature-card">
        <div class="feature-card-icon">💵</div>
        <div class="feature-card-title">Pencairan MG</div>
        <div class="feature-card-desc">Extract disbursement details from Pencairan TXT files cleanly.</div>
    </div>
    <div class="feature-card">
        <div class="feature-card-icon">🏦</div>
        <div class="feature-card-title">Mutasi Bank – INA / ENG</div>
        <div class="feature-card-desc">Reorganise XLSX bank mutations in Indonesian or English column format.</div>
    </div>
    <div class="feature-card" style="grid-column: span 2;">
        <div class="feature-card-icon">🚗</div>
        <div class="feature-card-title">Faktur Pajak Unit</div>
        <div class="feature-card-desc">Filter and extract relevant rows from Faktur Pajak Unit XLSX files.</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="author-line">Created by &nbsp;<strong>Devin Augustin</strong></div>', unsafe_allow_html=True)
