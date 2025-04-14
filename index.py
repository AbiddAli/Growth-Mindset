import streamlit as st
import pandas as pd
import os
from io import BytesIO

# --- Page Configuration ---
st.set_page_config(
    page_title="📈 Growth Dashboard",
    page_icon="📊",
    layout="wide",
)

# --- Custom Styling ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f8f9fa;
        color: #1c1c1c;
        font-family: 'Segoe UI', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Title Section ---
st.title("📊 Growth Dashboard Integrator")
st.caption("Built by **Abid Ali**")
st.markdown("Easily upload, clean, visualize, and download your growth data.")

# --- File Upload ---
uploaded_files = st.file_uploader(
    "📁 Upload one or more CSV or Excel files", 
    type=["csv", "xlsx"], 
    accept_multiple_files=True
)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        # Load the file
        try:
            if file_ext == ".csv":
                df = pd.read_csv(file)
            elif file_ext == ".xlsx":
                df = pd.read_excel(file)
            else:
                st.error(f"❌ Unsupported file format: {file_ext}")
                continue
        except Exception as e:
            st.error(f"🚫 Failed to read file {file.name}: {e}")
            continue

        # File Info Section
        st.markdown("---")
        st.header(f"📂 File: `{file.name}`")
        st.subheader("🔍 Preview")
        st.dataframe(df.head(), use_container_width=True)

        # Data Cleaning
        with st.expander("🧼 Data Cleaning Options"):
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"🧹 Remove duplicates in `{file.name}`"):
                    before = len(df)
                    df.drop_duplicates(inplace=True)
                    after = len(df)
                    st.success(f"✅ Removed {before - after} duplicate rows.")
            with col2:
                if st.button(f"🩹 Fill missing values in `{file.name}`"):
                    numeric_cols = df.select_dtypes(include=["number"]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✅ Missing numeric values filled with column averages.")

        # Column Selection
        with st.expander("📌 Select Columns to Visualize"):
            selected_cols = st.multiselect(
                "Choose columns to include in visualization",
                df.columns,
                default=df.columns.tolist()
            )
            df = df[selected_cols]

        # Visualization
        with st.expander("📈 Data Visualization"):
            if not df.select_dtypes(include=["number"]).empty:
                st.bar_chart(df.select_dtypes(include=["number"]).iloc[:, :2])
            else:
                st.warning("⚠️ No numeric columns available for visualization.")

        # File Conversion
        st.subheader("📤 Download Processed File")
        conversion_type = st.radio("Choose export format:", ("CSV", "Excel"), key=file.name)

        if st.button(f"⬇️ Download `{file.name}` as {conversion_type}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mimetype = "text/csv"
            else:
                df.to_excel(buffer, index=False, engine='openpyxl')
                file_name = file.name.replace(file_ext, ".xlsx")
                mimetype = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            st.download_button(
                label=f"📥 Click to download `{file_name}`",
                data=buffer,
                file_name=file_name,
                mime=mimetype,
            )


