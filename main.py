import os
import streamlit as st
from src.core.Chat_Utility import Chat_Manager
from streamlit_javascript import st_javascript
import gc
import pickle

from src.aws_rag.aws_rag import get_user_name, get_user_files
os.environ["TOKENIZERS_PARALLELISM"] = "true"

@st.cache_data
def get_access_token(url):
    token = ""
    if str(url).__contains__("id_token"):
        parameters = {}
        parm = url.split("#")[1]
        for pair in parm.split('&'):
            p = pair.split('=')
            parameters[p[0]] = p[1]
            
        token = parameters["access_token"]
        if len(token) > 40:
            print(f"reseting token = {token}")
            print(get_user_files(token))
            st.session_state["access_token"] = token
            st.session_state["user"] = get_user_name(parameters["access_token"])
    return token

def save_api_key(key):
    with open("data/unique_api_key.pkl", "wb") as f:
        openai_key = {"openai_key":key}
        f.write(pickle.dumps(openai_key))
        
def get_api_key():
    if os.path.exists("data/unique_api_key.pkl"):
        with open("data/unique_api_key.pkl", "rb") as f:
            return pickle.loads(f.read())["openai_key"]
    else:
        return ""

def main():
    #UI 
    st.set_page_config(
    page_title="Rag Studio Main",
    page_icon="👋",
    )
    
    st.title("🦙 Rag Studio")
    
    if 'user' not in st.session_state:
        st.session_state["up_result"] = ""
        st.session_state["user"] = "default"
        st.session_state["access_token"] = ""
        st.session_state["chat"] = Chat_Manager(st.session_state, "past")
        st.session_state["chatC"] = Chat_Manager(st.session_state, "pastC")
        st.session_state["lombda_key"] = ""
        st.session_state["openai_key"] = get_api_key()
        #st.session_state["local_ai"] = False
        #st.session_state["local_path"] = ""
        st.session_state["create_collection_name"] = "default"
        st.session_state["collection_list"] = []
        st.session_state["files_list"] = []
        
        
        
    url = st_javascript("await fetch('').then(r => window.parent.location.href)")
    get_access_token(url)
    
    st.subheader("Sign In") #Title
    
    user = st.session_state["user"] 
    st.subheader(f"Welcome: {user}") #Title
    
    URL_STRING = "https://ragstudio.auth.us-east-1.amazoncognito.com/oauth2/authorize?client_id=1687t8u3293rqmnaji7m60pdss&response_type=code&scope=aws.cognito.signin.user.admin+email+openid+user-s3-resource-scope-id%2Freadwrite&redirect_uri=https%3A%2F%2Fragstudio.streamlit.app%2F"
    st.markdown(
    f'<a href="{URL_STRING}" style="display: inline-block; padding: 12px 20px; background-color: #4CAF50; color: white; text-align: center; text-decoration: none; font-size: 16px; border-radius: 4px;" target="_self">Sign In Here</a>',
    unsafe_allow_html=True)
    
    #st.session_state["lombda_key"] = st.text_input("Lombda api key", value= st.session_state["lombda_key"], type="password")
    
    st.session_state["openai_key"] = st.text_input("OpenAI api key", value=st.session_state["openai_key"], type="password")
    #st.session_state["local_ai"] = st.checkbox('Use Local AI')
    #st.session_state["local_path"] = st.text_input("Local api path", value=st.session_state["local_path"])
    
    if st.button("Update Local Key?"):
        save_api_key(st.session_state["openai_key"])
        
if __name__ == '__main__':
    main()