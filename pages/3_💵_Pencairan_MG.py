import streamlit as st
import pandas as pd
import re
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from styles import SHARED_CSS, page_header, divider

st.set_page_config(page_title="Pencairan MG", page_icon="💵", layout="wide")
st.markdown(SHARED_CSS, unsafe_allow_html=True)
st.markdown(page_header("Pencairan MG", "TXT File Parser", "Upload a Pencairan TXT file to extract disbursement details into a clean, downloadable CSV."), unsafe_allow_html=True)

st.sidebar.markdown("### 💵 Pencairan MG")
st.sidebar.markdown("Extract disbursement details from Pencairan TXT files cleanly.")

# ── Logic ─────────────────────────────────────────────────────────────────────

def parse_loan_details(lines):
    data = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if re.match(r"^\s*\d+\s+", line):
            match = re.match(
                r"(\d+)\s+(.+?)\s+-\s+([A-Z]+)\s+([A-Z0-9]+)\s+([A-Z0-9]+)\s+(\d{1,2}/\d{1,2}/\d{4})\s+(\d{1,2}/\d{1,2}/\d{4})\s+([\d,.]*\.\d{2})\s+([\d,.]*\.\d{2})\s+([A-Z0-9]+)\s+([A-Z0-9]+)\s+(N\/A)",
                line
            )
            if match:
                main_fields = list(match.groups())
                main_fields[8:9] = [float(x.replace(",", "")) for x in main_fields[8:9]]
                if i + 1 < len(lines) and not re.match(r"^\s*\d+\s+", lines[i + 1]):
                    i += 1
                row = [
                    main_fields[0], main_fields[1], "",
                    main_fields[2], main_fields[3], main_fields[4],
                    main_fields[5], main_fields[6],
                    main_fields[7], main_fields[8],
                    main_fields[9], main_fields[10], main_fields[11],
                ]
                data.append(row)
        i += 1
    return data


# ── UI ─────────────────────────────────────────────────────────────────────────

uploaded_file = st.file_uploader("Choose a TXT file", type=["txt"])

if uploaded_file is not None:
    file_content = uploaded_file.read().decode("utf-8")
    lines = file_content.splitlines()

    with st.spinner("Parsing file…"):
        pencairan_data = parse_loan_details(lines)

    loan_columns = [
        "No.", "NAMA CABANG DEBITUR", "KD EXTERNAL", "CAB DEBITUR",
        "NO. GROUPING", "NO. KONTRAK", "TGL. KONTRAK", "TGL. VALUTA",
        "NILAI CAIR", "NILAI CAIR+BUNGA", "CHASIS", "MESIN", "TYPE",
    ]

    df_pencairan = pd.DataFrame(pencairan_data, columns=loan_columns)

    st.success(f"Parsed successfully — {len(df_pencairan)} disbursement records found.")
    st.markdown(divider(), unsafe_allow_html=True)

    st.subheader("Pencairan Details")
    st.dataframe(df_pencairan, use_container_width=True)

    st.markdown(divider(), unsafe_allow_html=True)

    st.download_button(
        "⬇ Download Pencairan CSV",
        df_pencairan.to_csv(index=False).encode("utf-8"),
        "pencairan.csv",
        "text/csv",
    )
