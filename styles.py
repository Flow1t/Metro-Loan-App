"""Shared UI styles for Metro Loan App pages."""

SHARED_CSS = """
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

section[data-testid="stSidebar"] { width: 220px !important; }
section[data-testid="stSidebar"] > div:first-child { padding: 1.5rem 1rem !important; }

.block-container {
    max-width: 780px !important;
    padding: 3rem 3rem 5rem !important;
}

/* ── Page header ── */
.page-eyebrow {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 8px;
}
.page-title {
    font-family: var(--font-display);
    font-size: 36px;
    line-height: 1.1;
    margin: 0 0 10px;
    font-weight: 400;
}
.page-desc {
    font-size: 14px;
    line-height: 1.75;
    max-width: 520px;
    margin-bottom: 2rem;
    opacity: 0.6;
}

/* ── Info card / instruction box ── */
.info-card {
    border-radius: var(--radius);
    padding: 16px 20px;
    border: 1px solid;
    margin-bottom: 1.5rem;
    font-size: 13px;
    line-height: 1.7;
}
.info-card ul {
    margin: 6px 0 0;
    padding-left: 1.2rem;
}
.info-card li { margin-bottom: 2px; }

/* ── Divider ── */
.section-divider {
    height: 1px;
    margin: 1.75rem 0;
    opacity: 0.12;
}

/* ══════════════════════════════════════
   LIGHT THEME
══════════════════════════════════════ */
[data-theme="light"] .page-title { color: #111827; }
[data-theme="light"] .page-desc  { color: #374151; }
[data-theme="light"] .section-divider { background: #111827; }

[data-theme="light"] .info-card {
    background: #fafaf9;
    border-color: #e5e7eb;
    color: #374151;
}

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
[data-theme="dark"] .page-title { color: #f9fafb; }
[data-theme="dark"] .page-desc  { color: #d1d5db; }
[data-theme="dark"] .section-divider { background: #f9fafb; }

[data-theme="dark"] .info-card {
    background: rgba(255,255,255,0.04);
    border-color: rgba(255,255,255,0.08);
    color: #d1d5db;
}

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

/* ── Shared ── */
.stSpinner > div { border-top-color: var(--accent) !important; }
</style>
"""


def page_header(eyebrow: str, title: str, desc: str) -> str:
    return f"""
<div class="page-eyebrow">{eyebrow}</div>
<div class="page-title">{title}</div>
<p class="page-desc">{desc}</p>
"""


def info_card(content: str) -> str:
    return f'<div class="info-card">{content}</div>'


def divider() -> str:
    return '<hr class="section-divider"/>'
