import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

st.set_page_config(page_title="Faktur Pajak Unit")

st.sidebar.header("Faktur Pajak Unit")

def pajak_unit(file1):
    df = pd.read_excel(file1, header=0)

    # Print column names to verify
    print(df.columns)

    # Use the correct column name
    column_name = "ColumnA"  # Update this with the actual column name

    mask_mk = df['ColumnB'].astype(str).str.startswith('MK')
    mask_non_mk = ~mask_mk

    pattern_mk = r"seri faktur pajak|900|901|total ppn|dasar pengenaan pajak|2022|2021|2023|2024|^(1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29|30|31|32|33|34|35|36|37|38|39|40|41|42|43|44|45|46|47|48|49|50|51|52|53|54|55|56|57|58|59|60|61|62|63|64|65|66|67|68|69|70|71|72|73|74|75|76|77|78|79|80|81|82|83|84|85|86|87|88|89|90|91|92|93|94|95|96|97|98|99|100)$"
    pattern_non_mk = r"seri faktur pajak|900|901|total ppn|dasar pengenaan pajak"

    # Keep rows where the column contains "seri faktur pajak" or any value with "901"
    filtered_df = df[
        #(mask_mk & df[column_name].astype(str).str.strip().str.contains(pattern_mk, case=False, na=False)) |
        (df[column_name].astype(str).str.strip().str.contains(pattern_mk, case=False, na=False))
    ]

    return filtered_df


def main():
    st.title("Faktur Pajak Unit Organizer")
    st.write("Upload your Faktur Pajak file. Add column name on the first row as follow:")
    st.markdown(
        """
        - First Column: ColumnA
        - Second Column: ColumnB
        """
    )

    file_pajak_unit = st.file_uploader("Choose an XLSX file", type=["xlsx"])

    if file_pajak_unit is not None:
        unit = pajak_unit(file_pajak_unit)

        st.success("Faktur Pajak File Generated")

        # Convert DataFrame to Excel in memory
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            unit.to_excel(writer, index=False, sheet_name='pajak_unit')
        processed_data = output.getvalue()

        # Download button
        st.download_button(
            "Download Faktur Pajak Unit File",
            data=processed_data,
            file_name="faktur_pajak_unit.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

if __name__ == "__main__":
    main()