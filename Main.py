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
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300&family=DM+Serif+Display:ital@0;1&display=swap');

:root {
    --accent: #B8860B;
    --accent-light: #D4A017;
    --radius: 12px;
    --font-body: 'DM Sans', sans-serif;
    --font-display: 'DM Serif Display', serif;
}

html, body, .stApp, [class*="css"] {
    font-family: var(--font-body) !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    width: 220px !important;
}
section[data-testid="stSidebar"] > div:first-child {
    padding: 1.5rem 1rem !important;
}

/* ── Main content ── */
.block-container {
    max-width: 780px !important;
    padding: 3rem 3rem 5rem !important;
}

/* ── Hero ── */
.hero-eyebrow {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 8px;
}
.hero-title {
    font-family: var(--font-display);
    font-size: 42px;
    line-height: 1.1;
    margin: 0 0 12px;
    font-weight: 400;
}
.hero-subtitle {
    font-size: 14px;
    line-height: 1.75;
    max-width: 480px;
    margin-bottom: 2.5rem;
    opacity: 0.6;
}

/* ── Feature grid ── */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
    margin-bottom: 2.5rem;
}
.feature-card {
    border-radius: var(--radius);
    padding: 20px 22px;
    border: 1px solid;
    transition: transform 0.16s ease, box-shadow 0.16s ease, border-color 0.16s ease;
    cursor: default;
}
.feature-card.wide {
    grid-column: span 2;
}
.feature-card:hover {
    transform: translateY(-2px);
}
.fc-icon {
    font-size: 20px;
    margin-bottom: 10px;
    display: block;
}
.fc-title {
    font-family: var(--font-display);
    font-size: 15px;
    margin-bottom: 4px;
    font-weight: 400;
}
.fc-desc {
    font-size: 12px;
    line-height: 1.65;
    opacity: 0.55;
    margin: 0;
}

/* ── Divider ── */
.section-divider {
    height: 1px;
    margin: 2rem 0;
    opacity: 0.12;
}

/* ── Footer ── */
.app-footer {
    font-size: 11px;
    opacity: 0.3;
    margin-top: 0.5rem;
}
.app-footer strong { opacity: 0.7; }

/* ══════════════════════════════════════
   LIGHT THEME
══════════════════════════════════════ */
[data-theme="light"] .hero-title { color: #111827; }
[data-theme="light"] .hero-subtitle { color: #374151; }
[data-theme="light"] .app-footer { color: #111827; }

[data-theme="light"] .feature-card {
    background: #ffffff;
    border-color: #e5e7eb;
    color: #111827;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
[data-theme="light"] .feature-card:hover {
    border-color: var(--accent);
    box-shadow: 0 4px 20px rgba(184,134,11,0.1);
}
[data-theme="light"] .section-divider { background: #111827; }

[data-theme="light"] .stButton > button,
[data-theme="light"] .stDownloadButton > button {
    background: #111827 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: var(--font-body) !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 10px 24px !important;
    transition: all 0.18s ease !important;
    box-shadow: none !important;
}
[data-theme="light"] .stButton > button:hover,
[data-theme="light"] .stDownloadButton > button:hover {
    background: #1f2937 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(17,24,39,0.2) !important;
}

/* ══════════════════════════════════════
   DARK THEME
══════════════════════════════════════ */
[data-theme="dark"] .hero-title { color: #f9fafb; }
[data-theme="dark"] .hero-subtitle { color: #d1d5db; }
[data-theme="dark"] .app-footer { color: #f9fafb; }

[data-theme="dark"] .feature-card {
    background: rgba(255,255,255,0.04);
    border-color: rgba(255,255,255,0.08);
    color: #e5e7eb;
    box-shadow: none;
}
[data-theme="dark"] .feature-card:hover {
    border-color: var(--accent-light);
    box-shadow: 0 4px 24px rgba(212,160,23,0.1);
}
[data-theme="dark"] .section-divider { background: #f9fafb; }

[data-theme="dark"] .stButton > button,
[data-theme="dark"] .stDownloadButton > button {
    background: var(--accent) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: var(--font-body) !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 10px 24px !important;
    transition: all 0.18s ease !important;
    box-shadow: none !important;
}
[data-theme="dark"] .stButton > button:hover,
[data-theme="dark"] .stDownloadButton > button:hover {
    background: var(--accent-light) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(212,160,23,0.3) !important;
}

/* ── Shared interactive ── */
.stSpinner > div { border-top-color: var(--accent) !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-eyebrow">Metro Loan App</div>
<div class="hero-title">File Organiser</div>
<p class="hero-subtitle">Upload raw loan, mutasi, or pajak files and get clean, structured outputs in seconds — no manual work needed.</p>

<div class="feature-grid">
    <div class="feature-card">
        <span class="fc-icon">🧾</span>
        <div class="fc-title">Mutasi Bank MG (TXT)</div>
        <p class="fc-desc">Parse raw TXT loan files into structured loan details and subtotals.</p>
    </div>
    <div class="feature-card">
        <span class="fc-icon">📄</span>
        <div class="fc-title">Mutasi Bank MG (CSV)</div>
        <p class="fc-desc">Split Debit and Credit from CSV bank mutation exports automatically.</p>
    </div>
    <div class="feature-card">
        <span class="fc-icon">💵</span>
        <div class="fc-title">Pencairan MG</div>
        <p class="fc-desc">Extract disbursement details from Pencairan TXT files cleanly.</p>
    </div>
    <div class="feature-card">
        <span class="fc-icon">🏦</span>
        <div class="fc-title">Mutasi Bank – INA / ENG</div>
        <p class="fc-desc">Reorganise XLSX bank mutations in Indonesian or English column format.</p>
    </div>
    <div class="feature-card wide">
        <span class="fc-icon">🚗</span>
        <div class="fc-title">Faktur Pajak Unit</div>
        <p class="fc-desc">Filter and extract relevant rows from Faktur Pajak Unit XLSX files.</p>
    </div>
</div>

<hr class="section-divider"/>
<p class="app-footer">Created by <strong>Devin Augustin</strong></p>
""", unsafe_allow_html=True)
