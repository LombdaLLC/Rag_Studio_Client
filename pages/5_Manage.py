import streamlit as st
from src.aws_rag.aws_rag import delete_user_files
import json
import pandas as pd
from src.core.StreamLit_Util import get_collections_list, get_files_list, get_files_list_keys, get_models

@st.cache_data
def create_dataframes(files_list):
    files = get_files_list_keys(files_list)
    data = []
    for file in files:
        data.append({"delete": False, "file_name": file, "model": get_models(file, files_list)})
    return data 

def delete_user_data(df, db_type):
    for row in df.values:
        if row[0]:
            rslt = delete_user_files(st.session_state["access_token"], db_type, row[1])

def main():
    st.set_page_config(
    page_title="Create Collection",
    page_icon="👋",)
    
    #UI
    st.header("Update or Create a new Collection")
    
    st.header("Manage Files")
    if st.button("Refresh files"):
        get_files_list()
        
    if len(st.session_state["files_list"]) == 0:
        get_files_list()
        
    data = create_dataframes(st.session_state["files_list"])
    df = pd.DataFrame(data)
    edited_df_files = st.data_editor(
    df,
    disabled=["file_name"],
    hide_index=True,
)
    if st.button("delete files"):
        delete_user_data(edited_df_files, "file")


    st.header("Manage Collections")
    if st.button("Refresh collections"):
        get_collections_list()
        
    if len(st.session_state["collection_list"]) == 0:
        get_collections_list()
    
    data2 = create_dataframes(st.session_state["collection_list"])
    df = pd.DataFrame(data2)
    edited_df_collections = st.data_editor(
    df,
    disabled=["file_name"],
    hide_index=True,
)
    
    if st.button("delete collections"):
        delete_user_data(edited_df_collections, "collection")
    
if __name__ == '__main__':
    if st.session_state["access_token"] != "":
        main()
    else:
        st.header("please sign in for full features")