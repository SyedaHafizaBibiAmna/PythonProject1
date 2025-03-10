import streamlit as st
import pandas as pd
import os
from io import BytesIO
import numpy as np
import openpyxl

st.set_page_config(page_title="Data Detox", layout="wide")

# Custom CSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: black;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description
st.title("Data Detox Sterling Integrator")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization. Creating the project for Quarter 3!")

# File uploader
uploaded_files = st.file_uploader("Upload your file (accepts CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        # Display file details
        st.write(f"### Preview of {file.name}")
        st.dataframe(df.head())  # ✅ FIXED: Now inside the loop, so `df` is always defined

        # Data cleaning options
        st.subheader("Data Cleaning Options")

        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates removed!")

            with col2:
                if st.button(f"Fill missing values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ Missing values have been filled!")

            # Column selection
            st.subheader("Select Columns to Keep")
            columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
            df = df[columns]

        # Data visualization
        st.subheader("Data Visualization")
        if st.checkbox(f"Show visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])  # ✅ FIXED: Corrected selection

        # Conversion options
        st.subheader("Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

    st.success("✅ All files processed successfully!")
    
    # Fun and Easy Data Analysis Section
    st.subheader("🎮 Fun Data Explorer")
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        # Read the file
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
            
        st.write(f"🎲 Fun Facts about {file.name}:")
        
        # Fun Statistics in colorful boxes
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info(f"📏 Longest Word in Column Names:\n{max(df.columns, key=len)}")
            
        with col2:
            total_cells = df.shape[0] * df.shape[1]
            st.success(f"🔢 Total Numbers in Dataset:\n{total_cells:,}")
            
        with col3:
            st.warning(f"📊 Number of Columns:\n{len(df.columns)}")
            
        # Combined Fun Data Explorer
        if st.button(f"🎯 Explore Data Magic for {file.name}"):
            # Get numeric columns
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                st.write("✨ Data Magic Results:")
                
                # Random Column Analysis
                random_col = np.random.choice(list(numeric_cols))
                st.info(f"""
                🎲 Random Column Analysis for '{random_col}':
                • Average: {df[random_col].mean():.2f}
                • Highest: {df[random_col].max():.2f}
                • Lowest: {df[random_col].min():.2f}
                • Unique Values: {df[random_col].nunique()}
                """)
                
                # Pattern Detection
                patterns = []
                for col in numeric_cols:
                    if df[col].is_monotonic_increasing:
                        patterns.append(f"📈 '{col}' shows an increasing trend!")
                    elif df[col].is_monotonic_decreasing:
                        patterns.append(f"📉 '{col}' shows a decreasing trend!")
                
                if patterns:
                    st.success("🔍 Found some interesting patterns:\n" + "\n".join(patterns))
                
                # Quick Story
                st.warning(f"""
                📖 Quick Data Story:
                This dataset has {df.shape[0]} rows and {df.shape[1]} columns.
                The most variable column is '{df[numeric_cols].std().idxmax()}'.
                Data completeness is {(1 - df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100:.1f}%
                """)
            else:
                st.warning("No numeric columns found for analysis! 🤔")
                
        st.markdown("---")
