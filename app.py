from model import BotModel
import streamlit as st
import os
from dotenv import load_dotenv

st.set_page_config(
    page_title="Open AI Chat Completion App with Streamlit",
    page_icon="🎉"
)

st.title("Open AI Chat Completion App with Streamlit")
USER_AVATAR = "👤"
BOT_AVATAR = "🤖"

load_dotenv()

if "bot" not in st.session_state: 
    st.session_state.bot = BotModel("My Chatbot")
    # st.write(st.session_state.bot)

# Delete Messages
with st.sidebar.success("Side Bar"):
    if st.button("Delete Chat History"):
        st.session_state.bot.delete_chat_history()

# Displaying the messages in the session of both user and model
for message in st.session_state.bot.get_messages():
    avatar = USER_AVATAR if message['role'] == 'user' else BOT_AVATAR
    with st.chat_message(message["role"] , avatar=avatar):
        st.markdown(message['content']) 

# Main Interface
if prompt := st.chat_input("How can I Help you?"):

    with st.chat_message("user" , avatar=USER_AVATAR):
        st.markdown(prompt)

    with st.chat_message("assistant" , avatar=BOT_AVATAR):
        message_placeholder = st.empty()

        full_response = ""

        for response in st.session_state.bot.send_message({"role": "user" , "content":prompt }):
            full_response += response.choices[0].delta.content or ""
            message_placeholder.markdown(full_response + "|")

        message_placeholder.markdown(full_response)
    
    st.session_state.bot.messages.append({"role":"assistant","content":full_response})

st.session_state.bot.save_chat_history() 