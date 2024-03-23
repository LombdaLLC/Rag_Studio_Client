import streamlit as st
from src.aws_rag.aws_rag import ask_qa
import json
from src.core.StreamLit_Util import get_files_list, get_files_list_keys, get_models
import asyncio

def run_chain(query):
    st.session_state["chat"].add(False, ask_qa(query, st.session_state["selected_file"], st.session_state["access_token"], st.session_state["lombda_key"], st.session_state["openai_key"], st.session_state["selected_model"], "file",st.session_state["selected_file_chat_model"],2))

def on_input_change():
    if st.session_state["openai_key"] != "":
        #User input
        user_input = st.session_state.chat_input         
        st.session_state["chat"].add(True, user_input)           
        st.session_state.chat_input  = ""
        
        #LLM output
        run_chain(user_input)
    else:
        st.error("Missing open ai key")

def clear_chat():
    st.session_state["chat"].clear()
    
def main():
    st.set_page_config(
    page_title="Chat",
    page_icon="👋",
    )
    
    #UI   
    st.subheader("LLM Chat")
    
    if len(st.session_state["files_list"]) == 0:
        get_files_list()
        
    if st.button("Refresh files chat"):
        get_files_list()
        
    st.session_state["selected_file"] = st.selectbox("select file", get_files_list_keys(st.session_state["files_list"]))
    st.session_state["selected_model"] = st.selectbox("select model", get_models(st.session_state["selected_file"], st.session_state["files_list"] ))
    st.session_state["selected_file_chat_model"] = st.selectbox("select file chat model", ["gpt-3.5-turbo-0125","gpt-3.5-turbo-1106","gpt-3.5-turbo","gpt-3.5-turbo-instruct","gpt-4-0125-preview","gpt-4-turbo-preview","gpt-4-1106-preview","gpt-4","gpt-4-0613","gpt-4-32k","gpt-4-32k-0613"])
    chat_placeholder = st.empty() 

    with chat_placeholder.container(height=300): 
        st.session_state["chat"].update()
        
    with st.container():    
        st.text_input("User Input:", on_change=on_input_change, key="chat_input")
        
    st.button("Clear messages", on_click=clear_chat)
        
if __name__ == '__main__':
    if st.session_state["access_token"] != "":
        main()
    else:
        st.header("please sign in for full features")