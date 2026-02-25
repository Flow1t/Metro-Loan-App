import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from styles import SHARED_CSS, page_header, divider

st.set_page_config(page_title="Mutasi Bank MG – CSV", page_icon="📄", layout="wide")
st.markdown(SHARED_CSS, unsafe_allow_html=True)
st.markdown(page_header("Mutasi Bank MG", "CSV Organiser", "Upload a CSV bank mutation export and the app will automatically split Debit and Credit into separate columns."), unsafe_allow_html=True)

st.sidebar.markdown("### 📄 Mutasi Bank MG (CSV)")
st.sidebar.markdown("Split Debit and Credit from CSV bank mutation exports automatically.")

# ── Logic ─────────────────────────────────────────────────────────────────────

def mutasi_organizer(file1):
    df = pd.read_csv(file1, header=None)
    df = df[[0, 1, 2, 3, 4]]
    df.columns = ["Tanggal Transaksi", "Keterangan", "Cabang", "Jumlah", "Saldo"]

    df["Jumlah"] = df["Jumlah"].astype(str)
    df["Nominal"] = df["Jumlah"].str.replace(",", "").str.extract(r"([\d.]+)").astype(float)
    df["Jenis Transaksi"] = df["Jumlah"].str[-2:]

    df["Debit"] = np.where(df["Jenis Transaksi"] == "DB", df["Nominal"], 0)
    df["Kredit"] = np.where(df["Jenis Transaksi"] == "CR", df["Nominal"], 0)

    df = df.drop(columns=["Jumlah", "Nominal", "Jenis Transaksi"])
    df = df.reindex(columns=["Tanggal Transaksi", "Keterangan", "Cabang", "Debit", "Kredit", "Saldo"])
    return df


# ── UI ─────────────────────────────────────────────────────────────────────────

file_mutasi = st.file_uploader("Choose a CSV file", type=["csv"])

if file_mutasi is not None:
    with st.spinner("Processing…"):
        mutasi = mutasi_organizer(file_mutasi)

    st.success(f"Done — {len(mutasi)} transaction rows processed.")
    st.markdown(divider(), unsafe_allow_html=True)

    st.subheader("Preview")
    st.dataframe(mutasi, use_container_width=True)

    st.markdown(divider(), unsafe_allow_html=True)

    output = StringIO()
    mutasi.to_csv(output, index=False)
    new_file_name = file_mutasi.name.replace(".csv", "_processed.csv")

    st.download_button(
        "⬇ Download Processed CSV",
        data=output.getvalue(),
        file_name=new_file_name,
        mime="text/csv",
        use_container_width=False,
    )
