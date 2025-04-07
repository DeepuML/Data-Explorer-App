import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns

def main():
    st.title("📊 Data Explorer App")
    st.sidebar.title("📁 Upload Your Dataset")

    upload_file = st.sidebar.file_uploader("Upload your file", type=['csv', 'xlsx'])

    if upload_file is not None:
        try:
            # Check file type and read accordingly
            if upload_file.name.endswith('.csv'):
                data = pd.read_csv(upload_file)
            else:
                data = pd.read_excel(upload_file)

            st.sidebar.success("✅ File uploaded successfully")

            st.subheader("🔍 Preview of the Data")
            st.dataframe(data.head())

            st.subheader("📌 Data Overview")
            st.write("➡️ Shape of the data:", data.shape)
            st.write("➡️ Columns in the dataset:")
            st.write(data.columns.tolist())
            st.write("➡️ Missing values in each column:")
            st.write(data.isnull().sum())

            st.subheader("📈 Statistical Summary")
            st.write(data.describe())

        except Exception as e:
            st.error(f"🚨 An error occurred: {e}")

if __name__ == "__main__":
    main()
