import streamlit as st
from PIL import Image
from src.core.StreamLit_Util import Universal_Displayer
from os import listdir
from os.path import isfile, join  
import os
import shutil
import pickle
from src.aws_rag.aws_rag import upload_file_to_s3, get_access_url, get_collections
import json
import uuid


def upload_files(uploaded_files, access_key, openai_api_key, model):
    if len(uploaded_files) > 0:
        for uploaded_file in uploaded_files:
            file_name, file_extension = os.path.splitext(uploaded_file.name)
            save_file = uploaded_file.name
            if file_extension.lower() in [".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".ico", ".tga", ".gif", ".ppm", ".webp", ".psd"]:
                Image.open(uploaded_file).convert("RGB").save(f"./data/{save_file}")                                                                                 
            else:
                with open(f"./data/{save_file}", "wb") as binary_file:
                    binary_file.write(uploaded_file.read())  
                
                presignedurl = get_access_url(save_file, access_key, openai_api_key, model)
                print(presignedurl)
                return upload_file_to_s3(presignedurl, f"./data/{save_file}")
            
def main():
    st.set_page_config(
    page_title="Import Files",
    page_icon="👋",
)
    #UI
    st.header("Upload data")
    #["png", "jpg", "jpeg", "pdf","pst","msg","csv","txt","xlsx","xls","html"]
    uploaded_files = st.file_uploader("Upload pdfs with selectable text", type=["pdf"], accept_multiple_files=True)
    
    embedding = st.selectbox("model", ["text-embedding-3-small", "text-embedding-3-large", "text-embedding-ada-002"])
    
    #collections = get_collections_list(st.session_state["access_token"])
    #print(collections)
    #collection = st.selectbox("collection name", collections)
    if st.button("Upload") and (uploaded_files):
        if st.session_state["openai_key"] != "":
            with st.spinner("Uploading.."):
                st.session_state["up_result"] = upload_files(uploaded_files, st.session_state["access_token"], st.session_state["openai_key"], embedding) #upload file to silver
        else:
            st.error("Open AI key is missing on home page.")
            
    st.write(st.session_state["up_result"])
    
if __name__ == '__main__':
    if st.session_state["access_token"] != "":
        main()
    else:
        st.header("please sign in for full features")