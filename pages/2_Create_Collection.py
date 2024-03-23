import streamlit as st
from src.aws_rag.aws_rag import get_user_files, create_collection
import json
import pandas as pd
from src.core.StreamLit_Util import get_collections_list, get_files_list, get_files_list_keys, get_models



# @st.cache_data
# def get_file_models(f):
#     for i, file in enumerate(st.session_state["files_list"]):
#         key = [key for key in file][0]
#         if key == f:
#             return st.session_state["files_list"][i][key]
#     return []

@st.cache_data
def create_dataframes(files_list):
    files = get_files_list_keys(files_list)
    data = []
    for file in files:
        data.append({"include": False, "file_name": file, "model": get_models(file, files_list)})
    return data   

def create_new_collection(df, collection, model):
    sources = []
    for row in df.values:
        if row[0]:
            sources.append(row[1])
    print(sources)
    rslt = create_collection(st.session_state["access_token"], st.session_state["lombda_key"], collection, sources, model)
    print(rslt)
        
def main():
    st.set_page_config(
    page_title="Create Collection",
    page_icon="👋",
)
    
    #UI
    st.header("Update or Create a new Collection")
    st.session_state["create_collection_name"] = st.text_input("collection name", value= st.session_state["create_collection_name"], type="default")
    
    get_files_list()
        
    data = create_dataframes(st.session_state["files_list"])
    df = pd.DataFrame(data)
    edited_df = st.data_editor(
                df,
                disabled=["file_name"],
                hide_index=True,
            )
    
    embedding = st.selectbox("collection model", ["text-embedding-3-small", "text-embedding-3-large"])
    
    if st.button("Create Collection"):
        create_new_collection(edited_df, st.session_state["create_collection_name"], embedding)
    
if __name__ == '__main__':
    if st.session_state["access_token"] != "":
        main()
    else:
        st.header("please sign in for full features")