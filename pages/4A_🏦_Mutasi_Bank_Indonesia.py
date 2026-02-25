import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from styles import SHARED_CSS, page_header, divider

st.set_page_config(page_title="Mutasi Bank – Indonesia", page_icon="🏦", layout="wide")
st.markdown(SHARED_CSS, unsafe_allow_html=True)
st.markdown(page_header("Mutasi Bank", "Indonesia Version", "Upload an XLSX bank mutation file with Indonesian column headers. Debit and Credit will be split automatically."), unsafe_allow_html=True)

st.sidebar.markdown("### 🏦 Mutasi Bank (Indonesia)")
st.sidebar.markdown("Reorganise XLSX mutations with Indonesian column format.")

# ── Logic ─────────────────────────────────────────────────────────────────────

def mutasi_organizer(file1):
    df = pd.read_excel(file1, header=0)
    df["Debit"] = np.where(df["Jenis Transaksi"] == "DB", df["Mutasi"], 0)
    df["Kredit"] = np.where(df["Jenis Transaksi"] == "CR", df["Mutasi"], 0)
    df = df.drop(columns=["Mutasi", "Jenis Transaksi", "Cabang"])
    return df.reindex(columns=["Tanggal", "Keterangan", "Debit", "Kredit", "Saldo"], fill_value=0)


# ── UI ─────────────────────────────────────────────────────────────────────────

file_mutasi = st.file_uploader("Choose an XLSX file", type=["xlsx"])

if file_mutasi is not None:
    with st.spinner("Processing…"):
        mutasi = mutasi_organizer(file_mutasi)

    st.success(f"Done — {len(mutasi)} rows processed.")
    st.markdown(divider(), unsafe_allow_html=True)

    st.subheader("Preview")
    st.dataframe(mutasi, use_container_width=True)

    st.markdown(divider(), unsafe_allow_html=True)

    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        mutasi.to_excel(writer, index=False, sheet_name="Mutasi")

    st.download_button(
        "⬇ Download Mutasi Bank XLSX",
        data=output.getvalue(),
        file_name=file_mutasi.name,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
