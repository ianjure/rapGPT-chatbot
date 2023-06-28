import json
import streamlit as st
from hugchat import hugchat
from hugchat.login import Login
from streamlit_lottie import *


#Resources
email = st.secrets['email']
passwd = st.secrets['passwd']


# Page Configuration
st.set_page_config (
    page_title = "RapGPT Chatbot",
    page_icon = ":speech_balloon:",
    initial_sidebar_state = "collapsed"
    )

hide_menu_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
st.markdown(hide_menu_style, unsafe_allow_html = True)

hide_streamlit_style = """
    <style>
    div[data-testid="stToolbar"] {
    visibility: hidden;
    height: 0%;
    position: fixed;
    }
    div[data-testid="stDecoration"] {
    visibility: hidden;
    height: 0%;
    position: fixed;
    }
    div[data-testid="stStatusWidget"] {
    visibility: hidden;
    height: 0%;
    position: fixed;
    }
    #MainMenu {
    visibility: hidden;
    height: 0%;
    }
    header {
    visibility: hidden;
    height: 0%;
    }
    footer {
    visibility: hidden;
    height: 0%;
    }
    </style>
    """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.markdown("""
    <style>
    .block-container {
    padding-top: 0rem;
    padding-bottom: 1rem;
    padding-left: 2rem;
    padding-right: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

#Adding Lottiefile
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# Log in to huggingface and grant authorization to huggingchat
sign = Login(email, passwd)
cookies = sign.login()

# Save cookies to usercookies/<email>.json
sign.saveCookies()

# Create a ChatBot
chatbot = hugchat.ChatBot(cookies=cookies.get_dict())  # or cookie_path="usercookies/<email>.json"

# Create a new conversation
id = chatbot.new_conversation()
chatbot.change_conversation(id)

lottie_anim = load_lottiefile('robot_anim.json')

col1, col2 = st.columns([70,25])
with col1:
    st.markdown('')
    st.markdown('')
    st.markdown('')
    st.title('RapGPT Chatbot')
with col2:
    st_lottie(lottie_anim, loop = True, quality = 'high')

cont = st.container()
with cont:
    st.chat_message("assistant").markdown('Yo! I am RapGPT. A chatbot with a rapper-like personality. Ask me anything homie!')
                                          
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # React to user input
    if prompt := st.chat_input("Wazzup Homie?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
    
        response = chatbot.chat(f'Answer this in a rap verse style using 1 to 2 sentences only: yo {prompt} homie')
    
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

#Developed by Ian Jure Macalisang
