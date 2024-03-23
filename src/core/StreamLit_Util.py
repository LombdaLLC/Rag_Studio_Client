import urllib.request, urllib.error, urllib.parse
import base64
import requests as rs
import streamlit as st
import pandas as pd
import os
from src.aws_rag.aws_rag import get_user_files, get_collections, delete_user_files


def get_collections_list():
    clist = get_collections(st.session_state["access_token"])
    if isinstance(clist, list):
        st.session_state["collection_list"] = clist
        

def get_files_list():
    flist = get_user_files(st.session_state["access_token"])
    if isinstance(flist, list):
        st.session_state["files_list"] = flist

def get_files_list_keys(file_list):
    file_keys = []
    for file in file_list:
        file_keys.append([key for key in file][0])
    return file_keys

def get_models(f, lst):
    for i, file in enumerate(lst):
        key = [key for key in file][0]
        if key == f:
            print(f"{f},     {lst},    {i},      {key}")
            return lst[i][key]
    return []



def Universal_Displayer(filepath):
    file_name, file_extension = os.path.splitext(filepath)
    if file_extension == ".pdf":
        with open(filepath, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
        # Displaying File
        st.markdown(pdf_display, unsafe_allow_html=True)
    elif file_extension == ".csv":
        df = pd.read_csv(filepath)  # read a CSV file inside the 'data" folder next to 'app.py'
        st.write(df)  # visualize my dataframe in the Streamlit app
    elif file_extension == ".xls" or file_extension == ".xlsx":
        df = pd.read_excel(filepath)  # will work for Excel files
        st.write(df)  # visualize my dataframe in the Streamlit app
    elif file_extension in [".png", ".jpg", ".jpeg"]:
        st.image(filepath, caption=filepath.split("/")[-1]) 
    elif file_extension == ".html":
        with open(filepath, "rb") as f:
            html_string = f.read().decode('utf-8')
        st.markdown(html_string, unsafe_allow_html=False) 
    elif file_extension == ".txt":
        with open(filepath, "r") as f:
            _string = f.read().decode('utf-8')
        st.markdown(_string, unsafe_allow_html=True)
