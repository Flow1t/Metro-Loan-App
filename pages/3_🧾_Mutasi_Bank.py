import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

st.set_page_config(page_title="Mutasi")

st.sidebar.header("Mutasi Bank Organizer")

def mutasi_organizer(file1):
    # read the uploaded file directly
    df = pd.read_excel(file1, index_col=0)

    # Add Debit and Kredit columns based on Jenis Transaksi
    df['Debit'] = np.where(df['Jenis Transaksi'] == 'DB', df['Mutasi'], 0)
    df['Kredit'] = np.where(df['Jenis Transaksi'] == 'CR', df['Mutasi'], 0)

    # Drop unneeded columns
    df = df.drop(columns=['Mutasi', 'Jenis Transaksi', 'Cabang'])

    # Reorder columns
    new_columns_order = ['Keterangan', 'Debit', 'Kredit', 'Saldo']
    mutasi_final = df.reindex(columns=new_columns_order, fill_value=0)

    return mutasi_final


def main():
    st.title("Mutasi Bank Organizer")
    st.write("Upload your Mutasi Bank file. The app will separate the Debit and Credit automatically.")

    file_mutasi = st.file_uploader("Choose an XLSX file", type=["xlsx"])

    if file_mutasi is not None:
        mutasi = mutasi_organizer(file_mutasi)

        st.success("Mutasi Bank File Generated")

        # Convert DataFrame to Excel in memory
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            mutasi.to_excel(writer, index=False, sheet_name='Mutasi')
        processed_data = output.getvalue()

        # Download button
        st.download_button(
            "Download Mutasi Bank File",
            data=processed_data,
            file_name="mutasi_bank.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

if __name__ == "__main__":
    main()