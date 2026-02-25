import streamlit as st
import pandas as pd
from io import BytesIO
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from styles import SHARED_CSS, page_header, info_card, divider

st.set_page_config(page_title="Faktur Pajak Unit", page_icon="🚗", layout="wide")
st.markdown(SHARED_CSS, unsafe_allow_html=True)
st.markdown(page_header("Faktur Pajak Unit", "XLSX Organiser", "Upload your Faktur Pajak XLSX file to filter and extract relevant rows automatically."), unsafe_allow_html=True)

st.sidebar.markdown("### 🚗 Faktur Pajak Unit")
st.sidebar.markdown("Filter and extract relevant rows from Faktur Pajak Unit XLSX files.")

# ── Instructions ───────────────────────────────────────────────────────────────
st.markdown(info_card("""
<strong>File format required</strong> — add column headers on the first row:
<ul>
  <li><code>ColumnA</code> — primary content column (used for filtering)</li>
  <li><code>ColumnB</code> — secondary column (used for MK detection)</li>
</ul>
"""), unsafe_allow_html=True)

# ── Logic ─────────────────────────────────────────────────────────────────────

def pajak_unit(file1):
    df = pd.read_excel(file1, header=0)

    pattern_mk = (
        r"seri faktur pajak|900|901|total ppn|dasar pengenaan pajak"
        r"|2021|2022|2023|2024"
        r"|^([1-9]|[1-9]\d|100)$"
    )

    filtered_df = df[
        df["ColumnA"].astype(str).str.strip().str.contains(pattern_mk, case=False, na=False)
    ]
    return filtered_df


# ── UI ─────────────────────────────────────────────────────────────────────────

file_pajak_unit = st.file_uploader("Choose an XLSX file", type=["xlsx"])

if file_pajak_unit is not None:
    with st.spinner("Filtering rows…"):
        unit = pajak_unit(file_pajak_unit)

    st.success(f"Done — {len(unit)} rows matched the filter criteria.")
    st.markdown(divider(), unsafe_allow_html=True)

    st.subheader("Filtered Results")
    st.dataframe(unit, use_container_width=True)

    st.markdown(divider(), unsafe_allow_html=True)

    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        unit.to_excel(writer, index=False, sheet_name="pajak_unit")

    st.download_button(
        "⬇ Download Faktur Pajak Unit XLSX",
        data=output.getvalue(),
        file_name="faktur_pajak_unit.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
