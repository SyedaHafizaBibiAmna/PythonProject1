import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Detox", layout="wide")

#custom css
st.markdown(
    """
    <style>
    .stApp{
    background-color :black;
    color : white
    }
    </style>
    """,
    unsafe_allow_html=True
)

# title and description

st.title("Data Detox Sterling Integrator")
st.write("Transform your files between CVS and Excel fromats with built-in data cleaning and visualization Creating The project for Quater 3!")


# file uploader
uploaded_file= st.file_uploader("Upload your File(accept CVS or Excel):", type=["cvs","xlsx"],accept_multiple_files=(True))

if uploaded_file:
    for file in uploaded_file:
        file_ext =os.path.splitext(file.name)[-1].lower()

        if file_ext == ".cvs":
            df= pd.read_cvs(file)
        elif file_ext =="xlsx":
            df=pd.read_excel(file)
        else:
            st.error(f"unsupported file type: {file_ext}")
            continue

        # file details
    st.write(" Preview the head of the DataFrame") 
    st.dataframe(df.head())

    # data cleaning options
    st.subheader("Data Cleaning Options")

    if st.checkbox(f"Clean Data for {file.name}"):
        col1, col2 = st.columns(2)

        with col1:
            if st.button(f"Remove duplicates from the file :{file.name}"):
                df.drop_duplicates(inplace=True)
                st.write("Duplicates removed!")

        with col1:
            if st.button(f"Fill missing values for {file.name}"):
                numeric_cols=df.select_dtypes(include=['number']).columns
                df[numeric_cols]=df[numeric_cols].fillna(df[numeric_cols].mean())
                st.write("Missing Values have been filled")
        st.subheader("Select Colums to Keep")
        columns= st.multiselect(f"Choose colums for {file.name}" , df.columns, default=df.columns)
        df=df[columns]



    #    data visualization

    st.subheader("Data Visualization")
    if st.checkbox(f"Show visualization for {file.name}"):
        st.bar_chart(df.select_dtypes(include='number').iloc[:,'2'])



        # conversation options

    st.subheader("Coversion Options")
    conversion_type= st.radio(f"Convert{file.name} to:" , ["CVS,Excel"], key=file.name)   
    if st.button(f"Convert{file.name}"):
        buffer= BytesIO()
        if conversion_type=="CSV":
            df.to.csv(buffer, index=False)
            file_name =file.name.replace(file_ext, ".csv")
            mime_type= "text/csv"

        elif conversion_type =="Excel" :
             df.to.excel(buffer, index=False)
             file_name =file.name.replace(file_ext, ".xlsx")
             mime_type= "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        buffer.seek(0)


        st.download_button(
            label=f"Download {file.name} as {conversion_type}",
            data=buffer,
            file_name=file_name,
            mime=mime_type
        )
st.success("All Files Processed Successfully!")


