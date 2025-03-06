import streamlit as st
import pandas as pd
import re

# Function to parse loan details with extra columns
def parse_loan_details(lines):
    data = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # Match lines that start with a number (the main row)
        if re.match(r"^\s*\d+\s+", line):
            # Extract the 12 main fields (loan details)
            match = re.match(
                r"(\d+)\s+([A-Z0-9]+)\s+-\s+(\d{1,2}/\d{1,2}/\d{4})\s+(\d{1,2}/\d{1,2}/\d{4})\s+(\d{1,2}/\d{1,2}/\d{4})\s+([A-Z]+)\s+([\d,]+\.\d{2})\s+([\d.]+)\s+([\d,]+\.\d{2})\s+([\d,]+\.\d{2})\s+([\d,]+\.\d{2})\s+([\d,]+\.\d{2})",
                line
            )
            if match:
                main_fields = list(match.groups())
                # Clean numeric fields: convert Principal and next 5 fields to float
                main_fields[6:12] = [float(x.replace(",", "")) for x in main_fields[6:12]]
                # Default values for extra fields
                chasis = ""
                mesin = ""
                status = ""
                # Check if next line exists and does not start with a number,
                # which would indicate extra fields.
                if i + 1 < len(lines) and not re.match(r"^\s*\d+\s+", lines[i+1]):
                    extra_line = lines[i+1].strip()
                    # Split extra line by two or more spaces
                    extra_fields = re.split(r"\s{2,}", extra_line)
                    # Insert extra fields:
                    # First field for Chasis, second for Mesin, third for Status.
                    if len(extra_fields) >= 1:
                        chasis = extra_fields[0]
                    if len(extra_fields) >= 2:
                        mesin = extra_fields[1]
                    if len(extra_fields) >= 3:
                        status = extra_fields[2]
                    i += 1  # Skip extra line
                # Construct the row with new column order:
                # No., No Kontrak, Chasis, Mesin, Tgl Kontrak, Tgl Valuta, Mature Date, CCY,
                # Principal (IDR), Int(%), Bunga Berjalan, Bunga sd JT, Kewajiban Berjalan, Kewajiban JT,
                # Warna (forced empty), Status.
                row = [
                    main_fields[0],  # No.
                    main_fields[1],  # No Kontrak
                    chasis,          # Chasis from extra line
                    mesin,           # Mesin from extra line
                    main_fields[2],  # Tgl Kontrak
                    main_fields[3],  # Tgl Valuta
                    main_fields[4],  # Mature Date
                    main_fields[5],  # CCY
                    main_fields[6],  # Principal (IDR)
                    main_fields[7],  # Int(%)
                    main_fields[8],  # Bunga Berjalan
                    main_fields[9],  # Bunga sd JT
                    main_fields[10], # Kewajiban Berjalan
                    main_fields[11], # Kewajiban JT
                    "",              # Warna (forced empty)
                    status           # Status from extra field
                ]
                data.append(row)
        i += 1
    return data

# Function to parse subtotals (unchanged)
def parse_subtotals(lines):
    subtotals = []
    for line in lines:
        if "Sub Total per Tanggal" in line:
            match = re.match(
                r"Sub Total per Tanggal (\d{1,2}/\d{1,2}/\d{4})\s+:\s+([\d,]+\.\d{2})\s+([\d,]+\.\d{2})\s+([\d,]+\.\d{2})\s+([\d,]+\.\d{2})\s+([\d,]+\.\d{2})",
                line.strip()
            )
            if match:
                row = list(match.groups())
                row[1:] = [float(x.replace(",", "")) for x in row[1:]]
                subtotals.append(row)
    return subtotals

def main():
    st.title("Loan TXT File Parser")
    st.write("Upload your loan TXT file. The app will generate CSV files for loan details and subtotals.")

    uploaded_file = st.file_uploader("Choose a TXT file", type=["txt"])
    if uploaded_file is not None:
        file_content = uploaded_file.read().decode("utf-8")
        lines = file_content.splitlines()

        # Extract loan data and subtotals using the parsing functions
        loan_data = parse_loan_details(lines)
        subtotal_data = parse_subtotals(lines)

        # Define column headers with extra columns in the specified order
        loan_columns = [
            "No.", "No Kontrak", "Chasis", "Mesin", "Tgl Kontrak", "Tgl Valuta", "Mature Date", 
            "CCY", "Principal (IDR)", "Int(%)", "Bunga Berjalan", "Bunga sd JT", 
            "Kewajiban Berjalan", "Kewajiban JT", "Warna", "Status"
        ]
        subtotal_columns = [
            "Tanggal", "Principal (IDR)", "Bunga Berjalan", 
            "Bunga sd JT", "Kewajiban Berjalan", "Kewajiban JT"
        ]

        df_loans = pd.DataFrame(loan_data, columns=loan_columns)
        df_subtotals = pd.DataFrame(subtotal_data, columns=subtotal_columns)

        st.success("File parsed successfully!")
        st.subheader("Loan Details")
        st.dataframe(df_loans)
        st.subheader("Subtotals")
        st.dataframe(df_subtotals)

        # Provide download buttons for the CSV files
        csv_loans = df_loans.to_csv(index=False).encode("utf-8")
        csv_subtotals = df_subtotals.to_csv(index=False).encode("utf-8")

        st.download_button("Download Loan Details CSV", csv_loans, "loan_details.csv", "text/csv")
        st.download_button("Download Subtotals CSV", csv_subtotals, "subtotals.csv", "text/csv")

if __name__ == "__main__":
    main()