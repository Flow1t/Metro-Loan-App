import streamlit as st
import pandas as pd
import re
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from styles import SHARED_CSS, page_header, divider

st.set_page_config(page_title="Mutasi Bank MG – TXT", page_icon="🧾", layout="wide")
st.markdown(SHARED_CSS, unsafe_allow_html=True)
st.markdown(page_header("Mutasi Bank MG", "TXT File Parser", "Upload a raw Mutasi Bank TXT file to extract loan details and subtotals into downloadable CSV files."), unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────────────────────
st.sidebar.markdown("### 🧾 Mutasi Bank MG (TXT)")
st.sidebar.markdown("Parse raw TXT loan files into structured loan details and subtotals.")

# ── Logic ─────────────────────────────────────────────────────────────────────

def parse_loan_details(lines):
    data = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if re.match(r"^\s*\d+\s+", line):
            match = re.match(
                r"(\d+)\s+([A-Z0-9]+)\s+-\s+(\d{1,2}/\d{1,2}/\d{4})\s+(\d{1,2}/\d{1,2}/\d{4})\s+(\d{1,2}/\d{1,2}/\d{4})\s+([A-Z]+)\s+([\d,]+\.\d{2})\s+([\d.]+)\s+([\d,]+\.\d{2})\s+([\d,]+\.\d{2})\s+([\d,]+\.\d{2})\s+([\d,]+\.\d{2})",
                line
            )
            if match:
                main_fields = list(match.groups())
                main_fields[6:12] = [float(x.replace(",", "")) for x in main_fields[6:12]]
                chasis = mesin = status = ""
                if i + 1 < len(lines) and not re.match(r"^\s*\d+\s+", lines[i + 1]):
                    extra_fields = re.split(r"\s{2,}", lines[i + 1].strip())
                    if len(extra_fields) >= 1: chasis = extra_fields[0]
                    if len(extra_fields) >= 2: mesin = extra_fields[1]
                    if len(extra_fields) >= 3: status = extra_fields[2]
                    i += 1
                row = [
                    main_fields[0], main_fields[1],
                    chasis, mesin,
                    main_fields[2], main_fields[3], main_fields[4],
                    main_fields[5],
                    main_fields[6], main_fields[7],
                    main_fields[8], main_fields[9], main_fields[10], main_fields[11],
                    "", status,
                ]
                data.append(row)
        i += 1
    return data


def parse_all_subtotals(lines):
    subtotals = []
    pattern = re.compile(
        r"Sub Total\s+per\s+(.+?)\s+:\s+([\d,]+\.\d{2})\s+([\d,]+\.\d{2})\s+([\d,]+\.\d{2})\s+([\d,]+\.\d{2})\s+([\d,]+\.\d{2})",
        re.IGNORECASE
    )
    for line in lines:
        line = line.strip()
        if line.startswith("Sub Total"):
            match = pattern.match(line)
            if match:
                row = list(match.groups())
                row[1:] = [float(x.replace(",", "")) for x in row[1:]]
                subtotals.append(row)
    return subtotals


# ── UI ─────────────────────────────────────────────────────────────────────────

uploaded_file = st.file_uploader("Choose a TXT file", type=["txt"])

if uploaded_file is not None:
    file_content = uploaded_file.read().decode("utf-8")
    lines = file_content.splitlines()

    with st.spinner("Parsing file…"):
        loan_data = parse_loan_details(lines)
        subtotal_data = parse_all_subtotals(lines)

    loan_columns = [
        "No.", "No Kontrak", "Chasis", "Mesin", "Tgl Kontrak", "Tgl Valuta", "Mature Date",
        "CCY", "Principal (IDR)", "Int(%)", "Bunga Berjalan", "Bunga sd JT",
        "Kewajiban Berjalan", "Kewajiban JT", "Warna", "Status",
    ]
    subtotal_columns = ["Subtotal Type", "Pokok", "Bunga Berjalan", "Bunga sd JT", "Kewajiban Berjalan", "Kewajiban JT"]

    df_loans = pd.DataFrame(loan_data, columns=loan_columns)
    df_subtotals = pd.DataFrame(subtotal_data, columns=subtotal_columns)

    st.success(f"Parsed successfully — {len(df_loans)} loan records, {len(df_subtotals)} subtotal rows.")

    st.markdown(divider(), unsafe_allow_html=True)

    st.subheader("Loan Details")
    st.dataframe(df_loans, use_container_width=True)

    st.subheader("Subtotals")
    st.dataframe(df_subtotals, use_container_width=True)

    st.markdown(divider(), unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "⬇ Download Loan Details CSV",
            df_loans.to_csv(index=False).encode("utf-8"),
            "loan_details.csv",
            "text/csv",
            use_container_width=True,
        )
    with col2:
        st.download_button(
            "⬇ Download Subtotals CSV",
            df_subtotals.to_csv(index=False).encode("utf-8"),
            "subtotals.csv",
            "text/csv",
            use_container_width=True,
        )
