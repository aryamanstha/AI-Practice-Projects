import streamlit as st
from db import init_db,save_message,load_messages,get_all_conversation_ids,delete_conversations
import uuid
from langchain_anthropic import ChatAnthropic
import os
from dotenv import load_dotenv
from tavily import TavilyClient
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
model=ChatAnthropic(
    api_key=os.getenv("ANT_API_KEY"),
    model="claude-3-7-sonnet-latest",   
    temperature=0.5,
)

st.set_page_config(page_title="Weather App", layout="wide")
st.title("Weather App")

init_db()

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = str(uuid.uuid4())

if "messages" not in st.session_state:
        st.session_state.messages = []

def get_response(user_input):
    search = tavily.search(query=user_input, search_depth="advanced", max_results=5)
    snippets = [message['content'] for message in search['results']]
    context = "\n\n".join(snippets)
    prompt=f"""
    You are a helpful weather assistant. Use the following real-time data to answer questions accurately:\n\n
    "{context}"
    """
    response = model.invoke(prompt)
    return response.content
    
messages = load_messages(st.session_state.conversation_id) or []
st.session_state.messages = messages 
for role, content in messages:
    with st.chat_message(role):
        st.markdown(content)
        
user_input = st.chat_input("Ask about the weather in any city...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    save_message(st.session_state.conversation_id, "user", user_input)

    with st.spinner("Thinking..."):
        response = get_response(user_input)
        with st.chat_message("assistant"):
            st.markdown(response)
        save_message(st.session_state.conversation_id, "assistant", response)
    
    
with st.sidebar:
    st.header("⚙️ Controls")
    if st.button("New Conversation"):
        st.session_state.conversation_id = str(uuid.uuid4())
        st.rerun()

    st.markdown(f"Conversation ID: `{st.session_state.conversation_id}`")
    
    st.header("All Conversation IDs")
    all_conversation_ids = get_all_conversation_ids()
    for conv_id in all_conversation_ids:
        # st.write(conv_id)
        if st.button(f"{conv_id}", key=f"load_{conv_id}"):  
            st.session_state.conversation_id = conv_id
            st.session_state.messages = load_messages(conv_id) or []
            st.rerun()
    if st.button("Delete All Conversations"):
        with st.spinner("Deleting all conversations..."):
            delete_conversations()
            st.success("All conversations deleted!", icon="✅")
    