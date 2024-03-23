import streamlit as st
from src.aws_rag.aws_rag import get_collections, ask_qa
import json
from src.core.StreamLit_Util import get_collections_list, get_files_list, get_files_list_keys, get_models

def run_chain(query):
    return ask_qa(query, st.session_state["selected_collection"], st.session_state["access_token"], st.session_state["lombda_key"], st.session_state["openai_key"], st.session_state["selected_collection_model"], "collection", st.session_state["selected_collection_chat_model"], 2)

def on_input_change():
    #User input
    if st.session_state["openai_key"] != "":
        user_input = st.session_state.chat_inputC         
        st.session_state["chatC"].add(True, user_input)           
        st.session_state.chat_inputC  = ""
        
        #LLM output
        out_step_rsp = run_chain(user_input)  
        st.session_state["chatC"].add(False, out_step_rsp)
    else:
        st.error("Missing open ai key")

def clear_chat():
    st.session_state["chatC"].clear()
    
def main():
    st.set_page_config(
    page_title="Chat Collection",
    page_icon="👋",
    )
    
    #UI   
    st.subheader("LLM Chat")
    
    if len(st.session_state["collection_list"]) == 0:
        get_collections_list()
        
    if st.button("Refresh collections"):
        get_collections_list()
        
    if len(st.session_state["collection_list"]) != 0:
        st.session_state["selected_collection"] = st.selectbox("select collection", get_files_list_keys(st.session_state["collection_list"]))
        st.session_state["selected_collection_model"] = st.selectbox("select collection model", get_models(st.session_state["selected_collection"], st.session_state["collection_list"]))
        st.session_state["selected_collection_chat_model"] = st.selectbox("select chat model", ["gpt-3.5-turbo-0125","gpt-3.5-turbo-1106","gpt-3.5-turbo","gpt-3.5-turbo-instruct","gpt-4-0125-preview","gpt-4-turbo-preview","gpt-4-1106-preview","gpt-4","gpt-4-0613","gpt-4-32k","gpt-4-32k-0613"])
        chat_placeholder = st.empty() 

        with chat_placeholder.container(height=300): 
            st.session_state["chatC"].update()
        
        with st.container():    
            text = st.text_input("User CInput:", on_change=on_input_change, key="chat_inputC")
            
        st.button("Clear messages C", on_click=clear_chat)
        
if __name__ == '__main__':
    if st.session_state["access_token"] != "":
        main()
    else:
        st.header("please sign in for full features")