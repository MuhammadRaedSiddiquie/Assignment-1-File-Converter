import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Python File Converter 📂", page_icon=":material/file_present:")
st.title("File Converter")
st.subheader("Upload and Convert Files")
st.write("Upload CSV or Excel files and convert them to your desired format.")

# File uploader for multiple files
files = st.file_uploader("Upload file", type=["csv", "xlsx"], accept_multiple_files=True)

if files:
    for file in files:
        ext = file.name.split(".")[-1]
        # Read the file based on its extension
        df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)

        st.subheader(f"{file.name} - Preview")
        st.dataframe(df.head())  # Display the first few rows of the file

        # File conversion options
        format_choice = st.radio(f"Convert {file.name} to:", ["csv", "xlsx"], key=file.name)

        # Button to trigger file conversion and download
        if st.button(f"Download {file.name} as {format_choice}"):
            output = BytesIO()
            if format_choice == "csv":
                df.to_csv(output, index=False)
                mime = "text/csv"
                new_name = file.name.replace(ext, "csv")
            else:
                df.to_excel(output, index=False, engine="openpyxl")
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                new_name = file.name.replace(ext, "xlsx")

            output.seek(0)
            st.download_button("Download file", file_name=new_name, data=output, mime=mime)
            st.success("File downloaded successfully")