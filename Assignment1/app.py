# import streamlit as st
# import pandas as pd
# import os
# from io import BytesIO

# st.set_page_config(page_title="Data Detox", layout="wide")

# #custom css
# st.markdown(
#     """
#     <style>
#     .stApp{
#     background-color :black;
#     color : white
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # title and description

# st.title("Data Detox Sterling Integrator")
# st.write("Transform your files between CVS and Excel fromats with built-in data cleaning and visualization Creating The project for Quater 3!")


# # file uploader
# uploaded_file= st.file_uploader("Upload your File(accept CVS or Excel):", type=["cvs","xlsx"],accept_multiple_files=(True))

# if uploaded_file:
#     for file in uploaded_file:
#         file_ext =os.path.splitext(file.name)[-1].lower()

#         if file_ext == ".cvs":
#             df= pd.read_cvs(file)
#         elif file_ext =="xlsx":
#             df=pd.read_excel(file)
#         else:
#             st.error(f"unsupported file type: {file_ext}")
#             continue

#         # file details
#     st.write(" Preview the head of the DataFrame") 
#     st.dataframe(df.head())

#     # data cleaning options
#     st.subheader("Data Cleaning Options")

#     if st.checkbox(f"Clean Data for {file.name}"):
#         col1, col2 = st.columns(2)

#         with col1:
#             if st.button(f"Remove duplicates from the file :{file.name}"):
#                 df.drop_duplicates(inplace=True)
#                 st.write("Duplicates removed!")

#         with col1:
#             if st.button(f"Fill missing values for {file.name}"):
#                 numeric_cols=df.select_dtypes(include=['number']).columns
#                 df[numeric_cols]=df[numeric_cols].fillna(df[numeric_cols].mean())
#                 st.write("Missing Values have been filled")
#         st.subheader("Select Colums to Keep")
#         columns= st.multiselect(f"Choose colums for {file.name}" , df.columns, default=df.columns)
#         df=df[columns]



#     #    data visualization

#     st.subheader("Data Visualization")
#     if st.checkbox(f"Show visualization for {file.name}"):
#         st.bar_chart(df.select_dtypes(include='number').iloc[:,'2'])



#         # conversation options

#     st.subheader("Coversion Options")
#     conversion_type= st.radio(f"Convert{file.name} to:" , ["CVS,Excel"], key=file.name)   
#     if st.button(f"Convert{file.name}"):
#         buffer= BytesIO()
#         if conversion_type=="CSV":
#             df.to.csv(buffer, index=False)
#             file_name =file.name.replace(file_ext, ".csv")
#             mime_type= "text/csv"

#         elif conversion_type =="Excel" :
#              df.to.excel(buffer, index=False)
#              file_name =file.name.replace(file_ext, ".xlsx")
#              mime_type= "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#         buffer.seek(0)


#         st.download_button(
#             label=f"Download {file.name} as {conversion_type}",
#             data=buffer,
#             file_name=file_name,
#             mime=mime_type
#         )
# st.success("All Files Processed Successfully!")


import streamlit as st
import pandas as pd
import os
from io import BytesIO

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
    # Add an innovative data insights section
    st.subheader("🔍 Smart Data Insights")
    if st.checkbox("Generate Automated Insights"):
        for file in uploaded_files:
            file_ext = os.path.splitext(file.name)[-1].lower()
            
            # Read the file
            if file_ext == ".csv":
                df = pd.read_csv(file)
            elif file_ext == ".xlsx":
                df = pd.read_excel(file)
                
            st.write(f"📊 Insights for {file.name}:")
            
            # Statistical overview
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                st.write("Key Statistics:")
                col1, col2 = st.columns(2)
                with col1:
                    if len(numeric_cols) >= 2:
                        st.info(f"• Strongest correlation: {df[numeric_cols].corr().unstack().sort_values(ascending=False)[1:2].index[0]}")
                    st.info(f"• Most variable column: {df[numeric_cols].std().idxmax()}")
                with col2:
                    st.info(f"• Data completeness: {(1 - df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100:.1f}%")
                    st.info(f"• Unique values ratio: {(df.nunique().sum() / (df.shape[0] * df.shape[1])) * 100:.1f}%")

            # Anomaly detection
            if len(numeric_cols) > 0:
                st.write("🔍 Potential Anomalies:")
                try:
                    for col in numeric_cols:
                        Q1 = df[col].quantile(0.25)
                        Q3 = df[col].quantile(0.75)
                        IQR = Q3 - Q1
                        outliers = df[(df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))][col]
                        if len(outliers) > 0:
                            st.warning(f"Found {len(outliers)} potential outliers in {col}")
                except Exception as e:
                    st.error(f"Could not analyze outliers: {str(e)}")

            st.markdown("---")

    # Add export options for insights
    if st.button("Export Insights Report"):
        report = BytesIO()
        with pd.ExcelWriter(report, engine='xlsxwriter') as writer:
            for file in uploaded_files:
                file_ext = os.path.splitext(file.name)[-1].lower()
                
                # Read the file again
                if file_ext == ".csv":
                    df = pd.read_csv(file)
                elif file_ext == ".xlsx":
                    df = pd.read_excel(file)
                
                # Basic statistics
                df.describe().to_excel(writer, sheet_name=f'{file.name[:28]}_stats')
                # Correlation matrix
                numeric_cols = df.select_dtypes(include=['number']).columns
                if len(numeric_cols) > 0:
                    df[numeric_cols].corr().to_excel(writer, sheet_name=f'{file.name[:28]}_corr')

        report.seek(0)
        st.download_button(
            label="📥 Download Complete Insights Report",
            data=report,
            file_name="data_insights_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
