from streamlit_chat import message

#Control streamlit-chat  
class Msg_Buf:
    def __init__(self, user, msg):
        self.user = user
        self.msg = msg

class Chat_Manager:
    def __init__(self, session_state, key):
        self.key = key
        self.session_state = session_state
        self.session_state[self.key] = []
        
    def clear(self):
        del self.session_state[self.key][:]
    
    def add(self, is_user, message):
        self.session_state[self.key].append(Msg_Buf(is_user, message))
        
    def update(self):
        if len(self.session_state[self.key]) > 0:
            for i in range(len(self.session_state[self.key])):                
                message(str(self.session_state[self.key][i].msg).strip(), is_user=self.session_state[self.key][i].user, key=f"{i}_user-{self.key}", allow_html=True) 
                
