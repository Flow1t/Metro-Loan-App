import streamlit as st
import pandas as pd
import numpy as np
import re

st.set_page_config(page_title="Mutasi")

st.sidebar.header("Mutasi Bank Organizer")

def mutasi_organizer(file1):
    df = pd.read_excel("file1", index_col=0)

    df['Debit'] = np.where(df['Jenis Transaksi'] == 'DB', df['Mutasi'], 0)
    df['Kredit'] = np.where(df['Jenis Transaksi'] == 'CR', df['Mutasi'], 0)

    df1 = df1.drop(columns=['Mutasi', 'Jenis Transaksi', 'Cabang'])

    new_columns_order = [
        'Keterangan',
        'Debit',
        'Kredit',
        'Saldo'
    ]

    mutasi_final = df1.reindex(columns=new_columns_order, fill_value=0)
    return mutasi_final


def main():
    st.title("Mutasi Bank Organizer")
    st.write("Upload your Mutasi Bank file. The app will seperate the Debit and Credit automatically")

    file_mutasi = st.file_uploader("Choose an XLSX file", type=["xlsx"])

    if file_mutasi is not None:
        mutasi = mutasi_organizer(file_mutasi)

        st.success("Mutasi Bank File Generated")
        
        # Read the generated Excel file in binary mode
        with open(mutasi, "rb") as f:
            file_content = f.read()
        
        st.download_button("Download Mutasi Bank File", data=file_content, file_name="mutasi_bank.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

if __name__ == "__main__":
    main()