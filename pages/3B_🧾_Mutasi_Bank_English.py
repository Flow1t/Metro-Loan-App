import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

st.set_page_config(page_title="Mutasi-English")

st.sidebar.header("Mutasi Bank Organizer - English")

def mutasi_organizer(file1):
    # read the uploaded file directly
    df = pd.read_excel(file1, header=0)

    # Add Debit and Kredit columns based on Jenis Transaksi
    df['Debit'] = np.where(df['Transcation Type'] == 'DB', df['Amount'], 0)
    df['Kredit'] = np.where(df['Transcation Type'] == 'CR', df['Amount'], 0)

    # Drop unneeded columns
    df = df.drop(columns=['Amount', 'Transaction Type', 'Branch'])

    # Reorder columns
    new_columns_order = ['Date','Description', 'Debit', 'Kredit', 'Balance']
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