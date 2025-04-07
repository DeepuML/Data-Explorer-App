import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
from scipy import stats
import io

# App config
st.set_page_config(page_title="Pro Data Explorer", layout="wide")

def main():
    st.title("📊 Advanced Data Explorer App")
    st.sidebar.title("📁 Upload Your Dataset")

    upload_file = st.sidebar.file_uploader("Upload your file", type=['csv', 'xlsx'])

    if upload_file is not None:
        try:
            if upload_file.name.endswith('.csv'):
                data = pd.read_csv(upload_file)
            else:
                data = pd.read_excel(upload_file)

            st.sidebar.success("✅ File uploaded successfully")

            # ------------------------------
            # 📄 BASIC EXPLORATION
            # ------------------------------
            st.subheader("🔍 Dataset Preview")
            st.dataframe(data.head())

            st.markdown("### 📊 Data Info")
            st.write("Shape:", data.shape)
            st.write("Columns:", data.columns.tolist())
            st.write("Data Types:")
            st.write(data.dtypes)
            st.write("Missing Values:")
            st.write(data.isnull().sum())

            st.markdown("### 📈 Statistical Summary")
            st.write(data.describe())

            # ------------------------------
            # 🎛 CLEANING TOOL
            # ------------------------------
            st.sidebar.header("🧹 Data Cleaning")
            if st.sidebar.checkbox("Drop columns"):
                drop_cols = st.sidebar.multiselect("Select columns to drop", data.columns)
                data.drop(columns=drop_cols, inplace=True)
                st.success(f"Dropped columns: {drop_cols}")

            if st.sidebar.checkbox("Fill Missing Values"):
                fill_method = st.sidebar.radio("Fill method", ("Mean", "Median", "Mode"))
                for col in data.select_dtypes(include=[np.number]):
                    if fill_method == "Mean":
                        data[col].fillna(data[col].mean(), inplace=True)
                    elif fill_method == "Median":
                        data[col].fillna(data[col].median(), inplace=True)
                    elif fill_method == "Mode":
                        data[col].fillna(data[col].mode()[0], inplace=True)
                st.success(f"Filled missing values using {fill_method}.")

            # ------------------------------
            # 🚨 OUTLIER DETECTION
            # ------------------------------
            st.subheader("📉 Outlier Detection (Z-score)")
            num_col = st.selectbox("Select numeric column for outlier check", data.select_dtypes(include=np.number).columns)
            z_scores = np.abs(stats.zscore(data[num_col]))
            outliers = data[z_scores > 3]
            st.write(f"🔎 Found {outliers.shape[0]} outliers in `{num_col}` column.")
            st.dataframe(outliers)

            # ------------------------------
            # 📋 CUSTOM QUERY TOOL
            # ------------------------------
            st.subheader("🧠 Query Your Data")
            query = st.text_input("Write your query using pandas syntax (e.g., data[data['Age'] > 30])")
            if query:
                try:
                    filtered = eval(query)
                    st.write(filtered)
                except Exception as e:
                    st.error(f"Error: {e}")

            # ------------------------------
            # 📊 CORRELATION HEATMAP
            # ------------------------------
            st.subheader("📌 Correlation Matrix")
            if st.checkbox("Show Heatmap"):
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.heatmap(data.select_dtypes(include=np.number).corr(), annot=True, cmap="coolwarm", ax=ax)
                st.pyplot(fig)

            # ------------------------------
            # 🧾 PROFILE REPORT
            # ------------------------------
            st.subheader("📋 Generate EDA Report")
            if st.button("Generate Profile Report"):
                profile = ProfileReport(data, explorative=True)
                st_profile_report(profile)

            # ------------------------------
            # 📥 DOWNLOAD
            # ------------------------------
            st.subheader("⬇️ Download Cleaned Data")
            buffer = io.BytesIO()
            data.to_csv(buffer, index=False)
            st.download_button("Download CSV", data=buffer.getvalue(), file_name="cleaned_data.csv", mime="text/csv")

        except Exception as e:
            st.error(f"🚨 Error: {e}")

if __name__ == "__main__":
    main()
