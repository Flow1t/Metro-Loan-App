import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO

st.set_page_config(page_title="Mutasi")

st.sidebar.header("Mutasi Bank Organizer - MG")

def mutasi_organizer(file1):
    df = pd.read_csv(file1, header=None)  # no header, read as raw data

    # Keep only necessary columns: col 0 (Tanggal), col 1 (Keterangan), col 3 (Jumlah), col 4 (Saldo)
    df = df[[0, 1, 2, 3, 4]]
    df.columns = ['Tanggal Transaksi', 'Keterangan', 'Cabang', 'Jumlah', 'Saldo']

    # Convert 'Jumlah' to string
    df['Jumlah'] = df['Jumlah'].astype(str)

    # Extract numeric value and transaction type
    df['Nominal'] = df['Jumlah'].str.replace(',', '').str.extract(r'([\d.]+)').astype(float)
    df['Jenis Transaksi'] = df['Jumlah'].str[-2:]

    # Create Debit and Kredit columns based on 'Jenis Transaksi'
    df['Debit'] = np.where(df['Jenis Transaksi'] == 'DB', df['Nominal'], 0)
    df['Kredit'] = np.where(df['Jenis Transaksi'] == 'CR', df['Nominal'], 0)

    # Drop 'Jumlah', 'Nominal', 'Jenis Transaksi'
    df = df.drop(columns=['Jumlah', 'Nominal', 'Jenis Transaksi'])

    # Final column order
    new_columns_order = ['Tanggal Transaksi', 'Keterangan', 'Cabang', 'Debit', 'Kredit', 'Saldo']
    df = df.reindex(columns=new_columns_order)

    return df

def main():
    st.title("Mutasi Bank Organizer - MG")
    st.write("Upload your Mutasi Bank CSV file. The app will separate the Debit and Credit automatically.")

    file_mutasi = st.file_uploader("Choose a CSV file", type=["csv"])

    if file_mutasi is not None:
        mutasi = mutasi_organizer(file_mutasi)

        st.success("Mutasi Bank File Generated")

        # Convert DataFrame to CSV in memory
        output = StringIO()
        mutasi.to_csv(output, index=False)
        processed_data = output.getvalue()

        # Set download file name based on uploaded file's name
        original_file_name = file_mutasi.name
        new_file_name = original_file_name.replace(".csv", "_processed.csv")

        # Download button
        st.download_button(
            label="Download Processed Mutasi Bank CSV",
            data=processed_data,
            file_name=new_file_name,
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
