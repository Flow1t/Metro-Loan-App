import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Pencairan")

st.sidebar.header("Pencairan TXT file Parser")

# Function to parse loan details with extra columns
def parse_loan_details(lines):
    data = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # Match lines starting with a number
        if re.match(r"^\s*\d+\s+", line):
            # Extract main fields using a flexible regex
            match = re.match(
                r"(\d+)\s+(.+?)\s+-\s+([A-Z]+)\s+([A-Z0-9]+)\s+([A-Z0-9]+)\s+(\d{1,2}/\d{1,2}/\d{4})\s+(\d{1,2}/\d{1,2}/\d{4})\s+([\d,.]*\.\d{2})\s+([\d,.]*\.\d{2})\s+([A-Z0-9]+)\s+([A-Z0-9]+)\s+(N\/A)",
                line
            )
            if match:
                # Extract the 13 main fields
                main_fields = list(match.groups())
                # Clean numeric values for "Nilai Cair" dan "Nilai Cair + Bunga"
                main_fields[8:9] = [float(x.replace(",", "")) for x in main_fields[8:9]]
                # Check if next line exists and does not start with a number
                if i + 1 < len(lines) and not re.match(r"^\s*\d+\s+", lines[i+1]):
                    extra_line = lines[i+1].strip()
                    # Split by two or more spaces
                    extra_fields = re.split(r"\s{2,}", extra_line)
                    i += 1
                # Construct the final row.
                # New column order:
                # NO., NAMA CABANG DEBITUR, KD.EXTERNAL, CAB DEBITUR, NO.GROUPING, NO. KONTRAK, TGL.KONTRAK,  TGL.VALUTA, NILAI CAIR, NILAI CAIR+BUNGA, CHASIS, MESIN, TYPE
                row = [
                    main_fields[0],            # No.
                    main_fields[1],            # Nama Cabang Debitur
                    "",                        # KD. External
                    main_fields[2],            # Cab Debitur
                    main_fields[3],            # No. Grouping
                    main_fields[4],            # No. Kontrak
                    main_fields[5],            # Tgl. Kontrak
                    main_fields[6],            # Tgl. Valuta
                    main_fields[7],            # Nilai Cair
                    main_fields[8],            # Nilai Cair + Bunga
                    main_fields[9],           # Chasis
                    main_fields[10],           # Mesin
                    main_fields[11]            # Type
                ]
                data.append(row)
        i += 1
    return data


#app
def main():
    st.title("Pencarian TXT File Parser")
    st.write("Upload your Pencarian.txt file. The app will extract the details, then generate downloadable CSV files.")

    uploaded_file = st.file_uploader("Choose a TXT file", type = ["txt"])
    if uploaded_file is not None:
        file_content = uploaded_file.read().decode("utf-8")
        lines = file_content.splitlines()

        # Extract loan details subtotals
        pencairan_data = parse_loan_details(lines)

        # Define column headers for Pencairan data
        loan_columns = [
            "No.", "NAMA CABANG DEBITUR", "KD EXTERNAL", "CAB DEBITUR", "NO. GROUPING", "NO. KONTRAK", "TGL. KONTRAK", "TGL. VALUTA", "NILAI CAIR", "NILAI CAIR+BUNGA", "CHASIS", "MESIN", 
            "TYPE"
        ]

        # Define new column headers with reordering
        # Create DataFrames
        df_pencairan = pd.DataFrame(pencairan_data, columns=loan_columns)

        st.success("File parsed successfully")
        st.subheader("Pencairan Details")
        st.dataframe(df_pencairan)

        # Provide download buttons for Excel files
        csv_pencairan = df_pencairan.to_csv(index=False).encode("utf-8")

        st.download_button("Download Pencairan CSV", csv_pencairan, "pencairan.csv", "text/csv")

if __name__ == "__main__":
    main()