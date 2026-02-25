import os
os.environ["STREAMLIT_SERVER_FILE_WATCHER_TYPE"] = "none"
os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"

import streamlit as st
import pandas as pd
import numpy as np
import re
from io import BytesIO, StringIO

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Metro Loan App",
    page_icon="🗂️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Instrument+Serif:ital@0;1&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, .stApp {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background: #f7f6f3;
    color: #1a1a2e;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #e8e5e0 !important;
    width: 230px !important;
}
section[data-testid="stSidebar"] > div { padding: 0 !important; }

.sidebar-header {
    padding: 28px 20px 20px;
    border-bottom: 1px solid #f0ede8;
}
.sidebar-app-name {
    font-family: 'Instrument Serif', serif;
    font-size: 20px;
    color: #1a1a2e;
    line-height: 1.2;
    margin-bottom: 3px;
}
.sidebar-app-sub {
    font-size: 11px;
    font-weight: 600;
    color: #9b8ea0;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.sidebar-author {
    font-size: 10px;
    color: #c4bbc9;
    margin-top: 10px;
}

/* Nav radio */
div[data-testid="stSidebar"] .stRadio > div { gap: 1px !important; }
div[data-testid="stSidebar"] .stRadio label {
    display: flex;
    align-items: center;
    padding: 11px 20px;
    margin: 0 !important;
    border-radius: 0;
    cursor: pointer;
    font-size: 13px;
    font-weight: 500;
    color: #8a7f94;
    transition: all 0.15s ease;
    border-left: 2px solid transparent;
}
div[data-testid="stSidebar"] .stRadio label:hover {
    background: #f9f7f5;
    color: #1a1a2e;
    border-left-color: #d4a853;
}
div[data-testid="stSidebar"] .stRadio [aria-checked="true"] + div label {
    background: #fdf8ef;
    color: #b8862a;
    border-left-color: #d4a853;
    font-weight: 600;
}
div[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] > div:first-child {
    display: none !important;
}

/* ── Layout ── */
.block-container {
    max-width: 820px;
    padding: 44px 52px 64px !important;
}

/* ── Typography ── */
.page-eyebrow {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.2em;
    color: #d4a853;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.page-title {
    font-family: 'Instrument Serif', serif;
    font-size: 32px;
    color: #1a1a2e;
    line-height: 1.15;
    margin-bottom: 8px;
}
.page-desc {
    font-size: 13.5px;
    color: #8a7f94;
    margin-bottom: 36px;
    line-height: 1.65;
    max-width: 520px;
}

/* ── Upload cards ── */
.upload-card {
    background: #ffffff;
    border: 1px solid #e8e5e0;
    border-radius: 14px;
    padding: 22px 24px 18px;
    margin-bottom: 16px;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.upload-card:hover {
    border-color: #d4a853;
    box-shadow: 0 2px 16px rgba(212,168,83,0.08);
}
.upload-card-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.16em;
    color: #d4a853;
    text-transform: uppercase;
    margin-bottom: 12px;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] { background: transparent !important; }
[data-testid="stFileUploader"] > div {
    background: #faf9f7 !important;
    border: 1.5px dashed #d8d2cc !important;
    border-radius: 10px !important;
    padding: 14px !important;
    transition: all 0.2s ease !important;
}
[data-testid="stFileUploader"] > div:hover {
    border-color: #d4a853 !important;
    background: #fdf8ef !important;
}
[data-testid="stFileUploader"] label { color: #8a7f94 !important; font-size: 13px !important; }
[data-testid="stFileUploader"] small { color: #bbb5b0 !important; font-size: 11px !important; }

/* ── Buttons ── */
.stButton > button, .stDownloadButton > button {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    letter-spacing: 0.04em !important;
    background: #1a1a2e !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 11px 26px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 12px rgba(26,26,46,0.15) !important;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    background: #2e2e4a !important;
    box-shadow: 0 4px 20px rgba(26,26,46,0.22) !important;
    transform: translateY(-1px) !important;
}

/* ── Alerts ── */
.stAlert {
    background: #fdf8ef !important;
    border: 1px solid #f0e0b0 !important;
    border-radius: 10px !important;
    color: #6b5a28 !important;
}
div[data-testid="stNotification"] {
    background: #f0faf4 !important;
    border: 1px solid #a8ddb8 !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1px solid #e8e5e0 !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

/* ── Home feature cards ── */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 14px;
    margin-top: 4px;
    margin-bottom: 28px;
}
.feature-card {
    background: #ffffff;
    border: 1px solid #e8e5e0;
    border-radius: 14px;
    padding: 22px 22px;
    transition: all 0.2s ease;
}
.feature-card:hover {
    border-color: #d4a853;
    box-shadow: 0 4px 20px rgba(212,168,83,0.1);
    transform: translateY(-2px);
}
.feature-card-icon { font-size: 20px; margin-bottom: 10px; }
.feature-card-title {
    font-family: 'Instrument Serif', serif;
    font-size: 15px;
    color: #1a1a2e;
    margin-bottom: 5px;
}
.feature-card-desc { font-size: 12px; color: #9b8ea0; line-height: 1.55; }

.file-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #f0faf4;
    border: 1px solid #a8ddb8;
    border-radius: 6px;
    padding: 4px 10px;
    font-size: 11px;
    color: #2d7d4e;
    margin-top: 6px;
    font-weight: 600;
}

/* ── Chrome ── */
#MainMenu, footer, header { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
.stSpinner > div { border-top-color: #d4a853 !important; }
</style>
""", unsafe_allow_html=True)

# ─── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <div class="sidebar-app-name">Metro<br>Loan App</div>
        <div class="sidebar-app-sub">File Organiser</div>
        <div class="sidebar-author">by Devin Augustin</div>
    </div>
    """, unsafe_allow_html=True)

    pages = {
        "🏠  Home":             "home",
        "🧾  Mutasi MG (TXT)":  "mutasi_txt",
        "📄  Mutasi MG (CSV)":  "mutasi_csv",
        "💵  Pencairan MG":     "pencairan",
        "🏦  Mutasi Bank – INA":"mutasi_ina",
        "🌐  Mutasi Bank – ENG":"mutasi_eng",
        "🚗  Faktur Pajak Unit":"faktur",
    }

    selected_label = st.radio("nav", options=list(pages.keys()), label_visibility="collapsed")
    selected = pages[selected_label]

# ─── Helpers ────────────────────────────────────────────────────────────────────
def page_header(eyebrow, title, desc=""):
    st.markdown(f"""
    <div class="page-eyebrow">{eyebrow}</div>
    <div class="page-title">{title}</div>
    <div class="page-desc">{desc}</div>
    """, unsafe_allow_html=True)

def file_badge(name, size_kb):
    st.markdown(
        f'<div class="file-badge">✓ {name}&nbsp;·&nbsp;{size_kb:.1f} KB</div>',
        unsafe_allow_html=True
    )

def upload_card(label, key, types):
    st.markdown(f'<div class="upload-card"><div class="upload-card-label">{label}</div>', unsafe_allow_html=True)
    f = st.file_uploader(label, type=types, key=key, label_visibility="collapsed")
    if f:
        file_badge(f.name, len(f.getbuffer()) / 1024)
    st.markdown("</div>", unsafe_allow_html=True)
    return f

def df_to_xlsx(df, sheet="Sheet1"):
    buf = BytesIO()
    with pd.ExcelWriter(buf, engine='xlsxwriter') as w:
        df.to_excel(w, index=False, sheet_name=sheet)
    return buf.getvalue()

# ─── Processing Functions ────────────────────────────────────────────────────────

def parse_mutasi_txt(lines):
    data = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if re.match(r"^\s*\d+\s+", line):
            match = re.match(
                r"(\d+)\s+([A-Z0-9]+)\s+-\s+(\d{1,2}/\d{1,2}/\d{4})\s+(\d{1,2}/\d{1,2}/\d{4})\s+"
                r"(\d{1,2}/\d{1,2}/\d{4})\s+([A-Z]+)\s+([\d,]+\.\d{2})\s+([\d.]+)\s+"
                r"([\d,]+\.\d{2})\s+([\d,]+\.\d{2})\s+([\d,]+\.\d{2})\s+([\d,]+\.\d{2})",
                line
            )
            if match:
                f = list(match.groups())
                f[6:12] = [float(x.replace(",", "")) for x in f[6:12]]
                chasis = mesin = status = ""
                if i + 1 < len(lines) and not re.match(r"^\s*\d+\s+", lines[i + 1]):
                    extra = re.split(r"\s{2,}", lines[i + 1].strip())
                    chasis = extra[0] if len(extra) > 0 else ""
                    mesin  = extra[1] if len(extra) > 1 else ""
                    status = extra[2] if len(extra) > 2 else ""
                    i += 1
                data.append([f[0], f[1], chasis, mesin, f[2], f[3], f[4], f[5],
                              f[6], f[7], f[8], f[9], f[10], f[11], "", status])
        i += 1
    return data

def parse_subtotals(lines):
    pattern = re.compile(
        r"Sub Total\s+per\s+(.+?)\s+:\s+([\d,]+\.\d{2})\s+([\d,]+\.\d{2})\s+"
        r"([\d,]+\.\d{2})\s+([\d,]+\.\d{2})\s+([\d,]+\.\d{2})",
        re.IGNORECASE
    )
    rows = []
    for line in lines:
        m = pattern.match(line.strip())
        if m:
            r = list(m.groups())
            r[1:] = [float(x.replace(",", "")) for x in r[1:]]
            rows.append(r)
    return rows

def parse_pencairan(lines):
    data = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if re.match(r"^\s*\d+\s+", line):
            match = re.match(
                r"(\d+)\s+(.+?)\s+-\s+([A-Z]+)\s+([A-Z0-9]+)\s+([A-Z0-9]+)\s+"
                r"(\d{1,2}/\d{1,2}/\d{4})\s+(\d{1,2}/\d{1,2}/\d{4})\s+"
                r"([\d,.]*\.\d{2})\s+([\d,.]*\.\d{2})\s+([A-Z0-9]+)\s+([A-Z0-9]+)\s+(N\/A)",
                line
            )
            if match:
                f = list(match.groups())
                f[8:9] = [float(x.replace(",", "")) for x in f[8:9]]
                if i + 1 < len(lines) and not re.match(r"^\s*\d+\s+", lines[i + 1]):
                    i += 1
                data.append([f[0], f[1], "", f[2], f[3], f[4], f[5], f[6], f[7], f[8], f[9], f[10], f[11]])
        i += 1
    return data

def process_mutasi_csv(file):
    df = pd.read_csv(file, header=None)
    df = df[[0, 1, 2, 3, 4]]
    df.columns = ['Tanggal Transaksi', 'Keterangan', 'Cabang', 'Jumlah', 'Saldo']
    df['Jumlah']  = df['Jumlah'].astype(str)
    df['Nominal'] = df['Jumlah'].str.replace(',', '').str.extract(r'([\d.]+)').astype(float)
    df['Jenis']   = df['Jumlah'].str[-2:]
    df['Debit']   = np.where(df['Jenis'] == 'DB', df['Nominal'], 0)
    df['Kredit']  = np.where(df['Jenis'] == 'CR', df['Nominal'], 0)
    return df[['Tanggal Transaksi', 'Keterangan', 'Cabang', 'Debit', 'Kredit', 'Saldo']]

def process_mutasi_xlsx(file, lang='id'):
    df = pd.read_excel(file, header=0)
    if lang == 'id':
        df['Debit']  = np.where(df['Jenis Transaksi'] == 'DB', df['Mutasi'], 0)
        df['Kredit'] = np.where(df['Jenis Transaksi'] == 'CR', df['Mutasi'], 0)
        df = df.drop(columns=['Mutasi', 'Jenis Transaksi', 'Cabang'])
        return df.reindex(columns=['Tanggal', 'Keterangan', 'Debit', 'Kredit', 'Saldo'], fill_value=0)
    else:
        df['Debit']  = np.where(df['Transaction Type'] == 'DB', df['Amount'], 0)
        df['Kredit'] = np.where(df['Transaction Type'] == 'CR', df['Amount'], 0)
        df = df.drop(columns=['Amount', 'Transaction Type', 'Branch'])
        return df.reindex(columns=['Date', 'Description', 'Debit', 'Kredit', 'Balance'], fill_value=0)

def process_faktur(file):
    df = pd.read_excel(file, header=0)
    pattern = (r"seri faktur pajak|900|901|total ppn|dasar pengenaan pajak"
               r"|2021|2022|2023|2024|^(?:[1-9]|[1-9]\d|100)$")
    return df[df['ColumnA'].astype(str).str.strip().str.contains(pattern, case=False, na=False)]

# ─── Pages ──────────────────────────────────────────────────────────────────────

if selected == "home":
    page_header("Metro Loan App", "Organise your files\nin an instant.",
                "Upload raw loan, mutasi, or pajak files — get clean, structured outputs with one click.")
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
    st.markdown('<p style="font-size:11px;color:#c4bbc9;">Source files are available from the internal system.</p>', unsafe_allow_html=True)

elif selected == "mutasi_txt":
    page_header("Mutasi Bank MG", "TXT File Parser",
                "Upload a Mutasi Bank TXT file to extract loan details and subtotals into downloadable CSVs.")
    f = upload_card("TXT File", "mt_f", ["txt"])
    st.markdown("<br>", unsafe_allow_html=True)
    if f:
        if st.button("Parse File", key="btn_mt"):
            lines = f.read().decode("utf-8").splitlines()
            loan_data = parse_mutasi_txt(lines)
            sub_data  = parse_subtotals(lines)
            loan_cols = ["No.", "No Kontrak", "Chasis", "Mesin", "Tgl Kontrak", "Tgl Valuta",
                         "Mature Date", "CCY", "Principal (IDR)", "Int(%)", "Bunga Berjalan",
                         "Bunga sd JT", "Kewajiban Berjalan", "Kewajiban JT", "Warna", "Status"]
            sub_cols  = ["Subtotal Type", "Pokok", "Bunga Berjalan", "Bunga sd JT",
                         "Kewajiban Berjalan", "Kewajiban JT"]
            df_loans = pd.DataFrame(loan_data, columns=loan_cols)
            df_subs  = pd.DataFrame(sub_data,  columns=sub_cols)
            st.success(f"Parsed {len(df_loans)} loan records · {len(df_subs)} subtotal rows.")
            c1, c2 = st.columns(2, gap="medium")
            with c1:
                st.markdown("**Loan Details**")
                st.dataframe(df_loans, use_container_width=True, height=260)
                st.download_button("⬇  Loan Details CSV",
                    df_loans.to_csv(index=False).encode(), "loan_details.csv", "text/csv")
            with c2:
                st.markdown("**Subtotals**")
                st.dataframe(df_subs, use_container_width=True, height=260)
                st.download_button("⬇  Subtotals CSV",
                    df_subs.to_csv(index=False).encode(), "subtotals.csv", "text/csv")

elif selected == "mutasi_csv":
    page_header("Mutasi Bank MG", "CSV Organiser",
                "Upload a bank mutation CSV — Debit and Credit will be separated automatically.")
    f = upload_card("CSV File", "mc_f", ["csv"])
    st.markdown("<br>", unsafe_allow_html=True)
    if f:
        if st.button("Process File", key="btn_mc"):
            with st.spinner("Processing..."):
                df = process_mutasi_csv(f)
            st.success(f"Done — {len(df)} rows processed.")
            st.dataframe(df, use_container_width=True, height=300)
            out = StringIO()
            df.to_csv(out, index=False)
            st.download_button("⬇  Download Processed CSV",
                out.getvalue().encode(), f.name.replace(".csv", "_processed.csv"), "text/csv")

elif selected == "pencairan":
    page_header("Pencairan MG", "Disbursement Parser",
                "Upload your Pencairan TXT file to extract structured disbursement details.")
    f = upload_card("TXT File", "pc_f", ["txt"])
    st.markdown("<br>", unsafe_allow_html=True)
    if f:
        if st.button("Parse File", key="btn_pc"):
            lines = f.read().decode("utf-8").splitlines()
            data  = parse_pencairan(lines)
            cols  = ["No.", "NAMA CABANG DEBITUR", "KD EXTERNAL", "CAB DEBITUR",
                     "NO. GROUPING", "NO. KONTRAK", "TGL. KONTRAK", "TGL. VALUTA",
                     "NILAI CAIR", "NILAI CAIR+BUNGA", "CHASIS", "MESIN", "TYPE"]
            df = pd.DataFrame(data, columns=cols)
            st.success(f"Parsed {len(df)} disbursement records.")
            st.dataframe(df, use_container_width=True, height=320)
            st.download_button("⬇  Download Pencairan CSV",
                df.to_csv(index=False).encode(), "pencairan.csv", "text/csv")

elif selected == "mutasi_ina":
    page_header("Mutasi Bank", "Indonesian Version",
                "Upload an XLSX bank mutation file in Indonesian format to split Debit and Credit.")
    f = upload_card("XLSX File", "mi_f", ["xlsx"])
    st.markdown("<br>", unsafe_allow_html=True)
    if f:
        if st.button("Process File", key="btn_mi"):
            with st.spinner("Processing..."):
                df = process_mutasi_xlsx(f, lang='id')
            st.success(f"Done — {len(df)} rows processed.")
            st.dataframe(df, use_container_width=True, height=300)
            st.download_button("⬇  Download Processed XLSX",
                df_to_xlsx(df, "Mutasi"), f.name,
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

elif selected == "mutasi_eng":
    page_header("Mutasi Bank", "English Version",
                "Upload an XLSX bank mutation file in English format to split Debit and Credit.")
    f = upload_card("XLSX File", "me_f", ["xlsx"])
    st.markdown("<br>", unsafe_allow_html=True)
    if f:
        if st.button("Process File", key="btn_me"):
            with st.spinner("Processing..."):
                df = process_mutasi_xlsx(f, lang='en')
            st.success(f"Done — {len(df)} rows processed.")
            st.dataframe(df, use_container_width=True, height=300)
            st.download_button("⬇  Download Processed XLSX",
                df_to_xlsx(df, "Mutasi"), f.name,
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

elif selected == "faktur":
    page_header("Faktur Pajak Unit", "Tax Invoice Filter",
                "Filter and extract relevant rows from your Faktur Pajak XLSX file.")
    st.markdown("""
    <div style="background:#fdf8ef;border:1px solid #f0e0b0;border-radius:10px;padding:14px 18px;
                margin-bottom:20px;font-size:12.5px;color:#6b5a28;line-height:1.7;">
        <strong>Required column names:</strong>&nbsp; First column → <code>ColumnA</code>
        &nbsp;|&nbsp; Second column → <code>ColumnB</code>
    </div>
    """, unsafe_allow_html=True)
    f = upload_card("XLSX File", "fk_f", ["xlsx"])
    st.markdown("<br>", unsafe_allow_html=True)
    if f:
        if st.button("Process File", key="btn_fk"):
            with st.spinner("Filtering rows..."):
                df = process_faktur(f)
            st.success(f"Done — {len(df)} matching rows found.")
            st.dataframe(df, use_container_width=True, height=320)
            st.download_button("⬇  Download Faktur Pajak XLSX",
                df_to_xlsx(df, "pajak_unit"), "faktur_pajak_unit.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
